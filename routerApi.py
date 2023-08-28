import routeros_api
import pymongo
from typing import Iterator

client = pymongo.MongoClient('mongodb://192.168.100.2:27017/')
# db = client['device']
mydb = client['RealTimeTraffic']
mycol = mydb.device


def routerdata(routerName=None, pings=None, pppoeActive=None, pppoeSecret=None, pppoeProfile=None, **kwargs):
    """
    :param routerName= database deviceName field data:
    :param pings = Host ip:
    :param pppoeAcitve = pppoeAcitveClient:
    :param pppoeSecret = pppoeSecretClient:
    :return: pppoeAcitveClient, pppoeSecretClient, ping result
    """
    if kwargs:
        unknown_params = ', '.join(kwargs.keys())
        return None, f"Unknown parameter received: {unknown_params}"

    collection = mycol.find_one({'deviceName': routerName})
    if collection is None:
        return "Database Router Data Not Found"

    try:
        connection = routeros_api.RouterOsApiPool(
            collection['address'],
            port=int(collection['port']),
            username=collection['name'],
            password=collection['password'],
            plaintext_login=True
        )
        api = connection.get_api()

        # Retrieve /ppp/active data
        if pppoeActive == 'pppoeActiveClient':
            listClient = api.get_resource('/ppp/active')
            pppoeAcitveClient = listClient.get()
            return pppoeAcitveClient

        if pppoeSecret == 'pppoeSecretClient':
            secretClient = api.get_resource('/ppp/secret')
            pppoeSecretClient = secretClient.get()
            return pppoeSecretClient

        if pppoeProfile == 'pppoeProfile':
            listProfile = api.get_resource('/ppp/profile')
            pppoeProfile = listProfile.get()
            return pppoeProfile

        if pings:
            ping = api.get_binary_resource('/').call('ping', {'address': pings.encode(), 'count': b'1',
                                                              'interval': b'.1'})  # this ip i got from example
            return ping

        return "Use the correct parameters to call the function otherwise check doc string"

    except routeros_api.exceptions.RouterOsApiConnectionError as e:
        message = "Failed to connect to the RouterOS device: " + str(e)
        print(message)
        return message

    except routeros_api.exceptions.RouterOsApiCommunicationError as e:
        if "invalid user name or password" in str(e):
            message = "Invalid username or password."
            # print(message)
        else:
            message = "An error occurred during communication: " + str(e)
            print(message)
        return message

    except Exception as e:
        message = "An error occurred: " + str(e)
        print(message)
        return None, message

    finally:
        if connection:
            connection.disconnect()


device = "A1_ACR"

# data = routerdata(routerName=device, pppoeActive="pppoeAcitveClient")

# routerClient = routerdata(routerName=device,pppoeActive="pppoeActiveClient", )
routerClient = routerdata(routerName=device, pppoeProfile="pppoeProfile")

# print(routerClient)

# data = []
#
# for i in routerClient:
#     data.append({
#         "packageName": i["name"],
#     })
#
# print(data)
