from datetime import datetime
import time
from typing import Iterator
import routeros_api
import json
# import pymongo
import routerApi
routerFindCollection = routerApi.mycol

# def datas(routerName=None, pppoeClient=None) -> Iterator[str]:
# def liveBandwidth(routerName=None, pppoeClient=None, **kwargs) :
#
#     # """
#     # :param routerName= database deviceName field data:
#     # :param pppoeClient = pppoeAcitveClient:
#     # :return: pppoeAcitveClient, ping result
#     # """
#     print(routerName)
#     if kwargs:
#         unknown_params = ', '.join(kwargs.keys())
#         return None, f"Unknown parameter received: {unknown_params}"
#
#     collection = routerFindCollection.find_one({'deviceName': routerName})
#     if collection is None:
#         return "Database Router Data Not Found"
#     try:
#         connection = routeros_api.RouterOsApiPool(collection["address"],
#                                                   port=int(collection["port"]),
#                                                   username=collection["name"],
#                                                   password=collection["password"],
#                                                   plaintext_login=True
#                                                   )
#         api = connection.get_api()
#         interface = api.get_resource('/interface')
#         data = "0.sfp-sfpplus1"
#         while True:
#             stats = interface.call(
#                 'monitor-traffic', {'interface': data, 'once': ''})
#             rx_bytes = int(stats[0]['rx-bits-per-second'])
#             tx_bytes = int(stats[0]['tx-bits-per-second'])
#             # rxbitToMbps = round(rx_bytes/1000)
#             rxbitToMbps = rx_bytes / 1000000
#             txbitToMbps = tx_bytes / 1000000
#             print(round(rxbitToMbps))
#             print(round(txbitToMbps))
#
#             jso_data = json.dumps(
#                 {
#                     "time": datetime.now().strftime("%H:%M:%S"),
#                     "rx_speed": round(rxbitToMbps),
#                     "tx_speed": round(txbitToMbps)
#                 }
#             )
#             # print(jso_data)
#             yield f"data:{jso_data}\n\n"
#             time.sleep(2)
#     except routeros_api.exceptions.RouterOsApiConnectionError as e:
#             message = "Failed to connect to the RouterOS device: " + str(e)
#             print(message)
#             return message
#     except routeros_api.exceptions.RouterOsApiCommunicationError as e:
#         if "invalid user name or password" in str(e):
#             message = "Invalid username or password."
#             # print(message)
#         else:
#             message = "An error occurred during communication: " + str(e)
#             print(message)
#         return message
#
#     except Exception as e:
#         message = "An error occurred: " + str(e)
#         print(message)
#         return None, message
#
#     finally:
#         if connection:
#             connection.disconnect()
# device = "A1_ACR"
# data_generator = liveBandwidth(routerName=device)
# for data in data_generator:
#     print(data)
def livetraffic(routerName=None, pppoeClient=None, **kwargs) -> Iterator[str]:
    if kwargs:
        unknown_params = ', '.join(kwargs.keys())
        yield f"Unknown parameter received: {unknown_params}"
        return

    collection = routerFindCollection.find_one({'deviceName': routerName})
    if collection is None:
        yield "Database Router Data Not Found"
        return

    try:
        connection = routeros_api.RouterOsApiPool(
            collection["address"],
            port=int(collection["port"]),
            username=collection["name"],
            password=collection["password"],
            plaintext_login=True
        )
        api = connection.get_api()
        interface = api.get_resource('/interface')
        print(interface)
        interfaceData = f'<pppoe-{pppoeClient}>'
        while True:
            stats = interface.call('monitor-traffic', {'interface': interfaceData, 'once': ''})
            rx_bytes = int(stats[0]['rx-bits-per-second'])
            tx_bytes = int(stats[0]['tx-bits-per-second'])
            rx_speed = rx_bytes / 1000
            tx_speed = tx_bytes / 1000

            jso_data = json.dumps({
                "time": datetime.now().strftime("%H:%M:%S"),
                "rx_speed": round(rx_speed),
                "tx_speed": round(tx_speed)
            })

            yield f"data:{jso_data}\n\n"
            time.sleep(2)

    except routeros_api.exceptions.RouterOsApiConnectionError as e:
        yield f"Failed to connect to the RouterOS device: {e}"

    except routeros_api.exceptions.RouterOsApiCommunicationError as e:
        if "invalid user name or password" in str(e):
            yield "Invalid username or password."
        else:
            yield f"An error occurred during communication: {e}"

    except Exception as e:
        yield f"An error occurred: {e}"

    finally:
        if connection:
            connection.disconnect()


# device = "A1_ACR"
#
# data_generator = livetraffic(routerName=device,pppoeClient=None)
# for data in data_generator:
#     print(data)