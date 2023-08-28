import json
from typing import Iterator
from flask import jsonify
from bson import json_util
import pymongo
# from bson import ObjectId
import routeros_api
import routerApi
import liveBandwidth
from flask import Flask, render_template, request, redirect, flash, Response, stream_with_context
from flask_cors import CORS

# from flask_caching import Cache


app = Flask(__name__)
app.secret_key = 'your-secret-key-goes-here'

cors = CORS(app)

# client = pymongo.MongoClient('mongodb://localhost:27017/')
client = pymongo.MongoClient('mongodb://192.168.100.2:27017/')
db = client['device']
collections = db['data1']
# Create a separate collection to store the latest ID value
id_collection = db["counters"]
mydb = client['RealTimeTraffic']
mycol = mydb.device.find()
collection = mydb.device.find_one({'_id': 2})
routerCollection = db["routers"]
oltCollection = db["olt"]


def routerdata() -> Iterator[str]:
    try:
        connection = routeros_api.RouterOsApiPool(collection['address'],
                                                  port=int(collection['port']),
                                                  username=collection['name'],
                                                  password=collection['password'],
                                                  plaintext_login=True
                                                  )
        # print((connection))
        api = connection.get_api()
        # list_address =  api.get_resource('/ip/firewall/address-list')
        list_address = api.get_resource('/ppp/active')
        routerDatas = list_address.get()
        routeros_api.RouterOsApiPool.disconnect(connection)

        # print(routerDatas)
        return routerDatas
    except ConnectionError as ce:
        print("Connection error occurred: {}".format(str(ce)))
    # Additional handling for connection errors

    except TimeoutError as te:
        print("Timeout error occurred: {}".format(str(te)))
        # Additional handling for timeout errors

    except Exception as unreachable:

        print("An unexpected error occurred: {}".format(str(unreachable)))
        # Additional handling for other unexpected errors


def get_next_sequence_value(sequence_name):
    sequence_document = id_collection.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=pymongo.ReturnDocument.AFTER
    )
    return sequence_document["sequence_value"]


@app.route('/', methods=['GET', 'POST'])
def home():
    routerFind = routerCollection.find()
    routerNames = routerCollection.find()
    oltdatasCollection = db["olts"]
    oltdatas = oltdatasCollection.find()
    #
    # for oltdata in oltdatas:
    #     print(oltdata)

    # olts = oltCollection.find({"nodetype": "olt"})
    return render_template("device.html", routers=routerFind, routerNames=routerNames, olts=oltdatas)


@app.route("/olt", methods=['GET', "POST"])
def olt():
    oltdatasCollection = db["olts"]
    olts = oltdatasCollection.find()
    result = []
    for olt in olts:
        result.append({
            "_id": str(olt["_id"]),
            "name": olt["name"],
            "addedName": olt["addedName"],
            "routerName": olt["routerName"],
            "devicePort": olt["devicePort"],
            "deviceType": olt["deviceType"]
        })
    return jsonify(result)


@app.route("/olt/<string:name>", methods=['GET', "POST"])
def olts(name):
    olts = oltCollection.find({"name": name})
    result = []
    for olt in olts:
        result.append({
            "_id": olt["_id"],
            "name": olt["name"],
            "addedName": olt["addedName"],
            "routerName": olt["routerName"],
            "devicePort": olt["devicePort"],
            "deviceType": olt["deviceType"]
        })
    return result


@app.route("/router", methods=['GET', "POST"])
def router():
    routerNames = routerCollection.find()
    result = []
    for routername in routerNames:
        result.append({
            "name": routername["name"],
            "host": routername["host"],
            "port": routername["port"],
        })
    return result


@app.route('/addMikrotik', methods=['GET', 'POST'])
def addMikrotik():
    if request.method == "POST":
        name = request.form.get("name")
        userName = request.form.get("userName")
        host = request.form.get("host")
        port = int(request.form.get("port"))
        password = request.form.get("password")
        routerCollection.insert_one({
            "name": name,
            "userName": userName,
            "host": host,
            "port": port,
            "password": password

        })

        # print(name, host, port, password)
    return {"data": "success"}


@app.route('/addOlt', methods=['GET', 'POST'])
def addOlt():
    if request.method == "POST":
        oltName = request.form.get("oltName")
        routerName = request.form.get("routerName")
        deviceType = request.form.get("deviceType")
        linkColour = "grey"
        devicePort = int(request.form.get("devicePort"))

        colour = {2: [linkColour, linkColour],
                  4: [linkColour, linkColour, linkColour, linkColour],
                  8: [linkColour, linkColour, linkColour, linkColour, linkColour, linkColour, linkColour, linkColour],
                  16: [linkColour, linkColour, linkColour, linkColour, linkColour, linkColour, linkColour, linkColour,
                       linkColour, linkColour, linkColour, linkColour, linkColour, linkColour, linkColour, linkColour]}

        Port = {2: ["PON-1", "PON-2"],
                4: ["PON-1", "PON-2", "PON-3", "PON-4", ],
                8: ["PON-1", "PON-2", "PON-3", "PON-4", "PON-5", "PON-6", "PON-7", "PON-8"],
                16: ["PON-1", "PON-2", "PON-3", "PON-4", "PON-5", "PON-6", "PON-7", "PON-8",
                     "PON-9", "PON-10", "PON-11", "PON-12", "PON-13", "PON-14", "PON-15", "PON-16"]}

        # select the document you want to update
        # myquery = {"_id": nodeId}
        # myquery = collections.find_one(myquery)
        # nodetype = myquery["nodetype"]
        # ponname = myquery["addedName"]
        # print(nodetype)

        oltCollections = db[oltName]

        oltCollectiondbs = db["olts"]

        oltCollectiondbs.insert_one(
            {
                "rootId": None,
                "name": oltName,
                "addedName": oltName,
                "routerName": routerName,
                "devicePort": devicePort,
                "deviceType": deviceType,
                "level": None,
                "value": None,
                "nodetype": "olt",
                "icon": "static/image/olt.png",
                "searchable": None
            }
        )

        oltCollections.insert_one(
            {
                # "_id": get_next_sequence_value("my_collection_id"),
                "id": get_next_sequence_value("my_collection_id"),
                "rootId": None,
                "name": oltName,
                "addedName": oltName,
                "level": None,
                "value": None,
                "nodetype": "olt",
                "icon": "static/image/olt.png",
                "searchable": None
            }
        )
        datafind = {"nodetype": "olt"}
        myquery = oltCollections.find_one(datafind)
        parrentNodeId = myquery["id"]
        # print(parrentNodeId)
        for i, (item1, item2) in enumerate(zip(colour[devicePort], Port[devicePort])):
            oltCollections.insert_one(
                {
                    # "_id": get_next_sequence_value("my_collection_id"),
                    "id": get_next_sequence_value("my_collection_id"),
                    "rootId": parrentNodeId,
                    "name": item2,
                    "addedName": item2,
                    "level": item1,
                    "value": None,
                    "icon": "static/image/pon.png",
                    "nodetype": "pon",
                    "searchable": None
                }
            )

    return redirect("/treemap")


@app.route("/treemap", methods=['GET', 'POST'])
def treemap():
    message = "offline"
    db_total_client = 0
    onlineClient = 0
    offlineClient = 0

    if request.method == "POST":
        routerName = request.form.get("routerName")
        # print(routerName)
        routerNameFind = routerCollection.find_one({'name': routerName})
        connection = routeros_api.RouterOsApiPool(
            routerNameFind['host'],
            port=int(routerNameFind['port']),
            username=routerNameFind['userName'],
            password=routerNameFind['password'],
            plaintext_login=True
        )

        try:
            api = connection.get_api()
            response = api.get_resource('/system/resource').get()
            routerActiveClients = api.get_resource('/ppp/active').get()
            numberOfClient = len(routerActiveClients)
            clientPppoENames = [routerActiveClient['name']
                                for routerActiveClient in routerActiveClients]
            onlineClient = oltCollection.count_documents(
                {"name": {"$in": clientPppoENames}})
            query = {"nodetype": "user"}
            db_total_client = oltCollection.count_documents(query)
            offlineClient = db_total_client - onlineClient

            if response:
                message = "online"
            else:
                message = "No response received from the device."

        except routeros_api.exceptions.RouterOsApiConnectionError as e:
            message = "Failed to connect to the RouterOS device: " + str(e)

        except Exception as e:
            message = "An error occurred: " + str(e)

        finally:
            connection.disconnect()

    return render_template('oltmap.html', message=message, total=db_total_client, online=onlineClient,
                           offline=offlineClient)


@app.route("/<string:oltName>/<string:routerName>", methods=['GET', 'POST'])
# @app.route("/tree",  methods=['GET', 'POST'])

def tree(oltName, routerName):
    data = []
    dataUpdateCollection = db[oltName]
    dataUpdateFind = dataUpdateCollection.find({"nodetype": "user"})
    treeDataFind = dataUpdateCollection.find()

    routerClient = routerApi.routerdata(routerName=routerName, pppoeActive="pppoeActiveClient")
    if routerClient == "Database Router Data Not Found":
        return jsonify({'message': "Router Not Found"})

    elif routerClient == "Invalid username or password.":
        return jsonify({'message': "Invalid username or password."})

    elif routerClient == "Failed to connect to the RouterOS device: [Errno 111] Connection refused":
        return jsonify({'message': "Connection refused"})

    # if routerClient == "Invalid username or password.":
    #      return jsonify({'message': routerClient})

    online = {"type": "#00ff00"}
    offline = {"type": "red"}
    for updatedata in dataUpdateFind:
        dataUpdateCollection.update_one(updatedata, {"$set": offline}, upsert=True)

    if routerClient:
        for routerData in routerClient:
            dbDatas1 = dataUpdateCollection.find(
                {"name": routerData["name"]}, projection={"rootId": 1})
            for dbData in dbDatas1:
                dataUpdateCollection.update_one(dbData, {"$set": online}, upsert=True)

    # Rest of the code remains the same

    for i in treeDataFind:
        i['_id'] = str(i['_id'])
        data.append(i)
    # id_mapping = {}
    # for i, el in enumerate(data):
    #     id_mapping[el['id']] = i
    #
    # root = None
    # for el in data:
    #     if el['rootId'] is None:
    #         root = el
    #         continue
    #     parent_el = data[id_mapping[el['rootId']]]
    #     parent_el['children'] = parent_el.get('children', []) + [el]
    id_mapping = {}
    root = None

    for el in data:
        id_mapping[el['id']] = el
        if el['rootId'] is None:
            root = el
        else:
            parent_el = id_mapping.get(el['rootId'])
            if parent_el:
                parent_el.setdefault('children', []).append(el)

    # Remove the unnecessary data list and the second loop for building the tree structure

    return jsonify(root)


@app.route("/addPlcNode", methods=['GET', 'POST'])
def addPlcNode():
    if request.method == "POST":
        dadtas = {'addPlcName': 'Test Node', 'addPlcId': '166', 'addPlcFiberCode': '1564', 'addPlcCore': '8',
                  'addPlcCoreColour': 'Green', 'addPlcTbc': '258', 'addPlcLat': '6464', 'addPlcLong': '654646',
                  'addPlcComment': 'at'}

        data = request.get_json()
        print(data)
        nodeName = request.json.get("addPlcName")
        nodeColour = request.json.get("addPlcCoreColour")
        nodeCore = int(request.json.get("addPlcCore"))
        nodeId = int(request.json.get("addPlcId"))
        collectionName = request.json.get("oltName")
        oltCollection = db[collectionName]

        # print(nodeName)
        # print(nodeColour)
        # print(type(nodeId))
        # print(nodeId)

        # Create a function to generate the next ID value

        colour = {2: ['blue', 'orange'],
                  4: ['blue', 'orange', 'green', 'brown'],
                  8: ['blue', 'orange', 'green', 'brown', 'grey', 'white', 'red', 'black'],
                  16: ['blue', 'orange', 'g reen', 'brown', 'grey', 'white', 'red', 'black',
                       'blue', 'orange', 'green', 'brown', 'grey', 'white', 'red', 'black']}

        Port = {2: ["PORT-1", "PORT-2"],
                4: ["PORT-1", "PORT-2", "PORT-3", "PORT-4", ],
                8: ["PORT-1", "PORT-2", "PORT-3", "PORT-4", "PORT-5", "PORT-6", "PORT-7", "PORT-8"],
                16: ["PORT-1", "PORT-2", "PORT-3", "PORT-4", "PORT-5", "PORT-6", "PORT-7", "PORT-8",
                     "PORT-9", "PORT-10", "PORT-11", "PORT-12", "PORT-13", "PORT-14", "PORT-15", "PORT-16"]}

        # select the document you want to update
        myquery = {"id": nodeId}
        myquery = oltCollection.find_one(myquery)
        nodetype = myquery["nodetype"]
        ponname = myquery["addedName"]
        print(nodetype)
        if nodetype == "pon":
            print("ponSplitter")

            # set the new field value using $set
            ponValue = {"name": ponname, "icon": "static/image/pon.png",
                        "value": None, "searchable": None}

            oltCollection.update_one(myquery, {"$set": ponValue}, upsert=True)
            oltCollection.insert_one(
                {
                    "id": get_next_sequence_value("my_collection_id"),
                    "rootId": nodeId,
                    "name": nodeName,
                    "addedName": nodeName,
                    "level": nodeColour,
                    "value": None,
                    "nodetype": "firstPlc",
                    "icon": "static/image/splitter.png",
                    "searchable": "YES"
                }
            )
            datafind = {"name": nodeName}
            myquery = oltCollection.find_one(datafind)
            parrentNodeId = myquery["id"]
            print(parrentNodeId)
            for i, (item1, item2) in enumerate(zip(colour[nodeCore], Port[nodeCore])):
                oltCollection.insert_one(
                    {
                        "id": get_next_sequence_value("my_collection_id"),
                        "rootId": parrentNodeId,
                        "name": item2,
                        "addedName": item2,
                        "level": item1,
                        "value": 8,
                        "nodetype": "core"
                    }
                )

        elif nodetype == "core":
            print("coreSplitter")
            # set the new field value using $set
            splitterValue = {"name": nodeName, "icon": "static/image/splitter.png",
                             "value": None, "nodetype": "splitter", "searchable": "YES"}

            oltCollection.update_one(
                myquery, {"$set": splitterValue}, upsert=True)

            for i, (item1, item2) in enumerate(zip(colour[nodeCore], Port[nodeCore])):
                oltCollection.insert_one(
                    {
                        "id": get_next_sequence_value("my_collection_id"),
                        "rootId": nodeId,
                        "name": item2,
                        "addedName": item2,
                        "level": item1,
                        "value": 8,
                        "nodetype": "core"
                    }
                )

    return {"message": "success"}


@app.route("/addUserNode", methods=['GET', 'POST'])
def addUserNode():
    if request.method == "POST":
        data = request.get_json()
        print(data)
        nodeName = request.json.get("addUserName")
        nodeId = int(request.json.get("addUserId"))
        collectionName = request.json.get("oltName")
        oltCollection = db[collectionName]
        print(nodeName)
        print(type(nodeId))
        print(nodeId)
        datafind = {"id": nodeId}
        myquery = oltCollection.find_one(datafind)
        userCoreColour = myquery["level"]
        print(userCoreColour)
        myquery = {"id": nodeId}
        # set the new field value using $set
        userValue = {"name": nodeName, "icon": "static/image/router.png",
                     "value": 8, "nodetype": "user", "searchable": "YES", "type": "red", }

        oltCollection.update_one(
            myquery, {"$set": userValue}, upsert=True)

    return {"message": "success"}


@app.route('/check', methods=['POST'])
# @cache.cached()
def check_document():
    value = request.form['name']
    query = {'name': value}
    result = collections.find_one(query)
    if result:

        message = "<span style='color:red;'>Name already exists!</span>"

        return message
    else:
        message = "Name Available"

        return message


@app.route("/renameNode", methods=['GET', 'POST'])
def node_rename():
    if request.method == "POST":
        nodeName = request.json.get("newName")
        nodeId = int(request.json.get("renameId"))
        myquery = {"id": nodeId}
        collectionName = request.json.get("oltName")
        oltCollection = db[collectionName]

        # set the new field value using $set
        newValue = {"name": nodeName, "type": "red"}
        oltCollection.update_one(myquery, {"$set": newValue}, upsert=True)

    return {"message": "success"}


@app.route('/remove', methods=['POST'])
def delete_item():
    data = request.get_json()
    print(data)
    removeId = int(request.json.get("removeId"))
    collectionName = request.json.get("oltName")
    oltCollection = db[collectionName]

    # select the document you want to update
    datafind = {"id": removeId}
    deleteNodefind = {'rootId': removeId}
    myquery = oltCollection.find_one(datafind)
    oldName = myquery["addedName"]
    nodetype = myquery["nodetype"]

    if nodetype == "user":
        print(nodetype)
        # collections.delete_one(datafind)
        newValue = {"name": oldName, "value": 8, "searchable": None,
                    "type": None, "icon": None, "nodetype": "core"}
        oltCollection.update_one(myquery, {"$set": newValue}, upsert=True)

    elif nodetype == "firstPlc":
        oltCollection.delete_one(datafind)
        oltCollection.delete_many(deleteNodefind)

        # return {"mes":"notdeleableNode"}
    elif nodetype == "olt":
        return {"mes": "notdeleteableOltNode"}
    elif nodetype == "core":
        return {"mes": "notdeleableCoreNode"}
    elif nodetype == "pon":
        return {"mes": "notdeleablePonNode"}
    else:
        # set the new field value using $set
        newValue = {"name": oldName, "value": 8, "searchable": None,
                    "type": None, "icon": None, "nodetype": "core"}
        oltCollection.update_one(myquery, {"$set": newValue}, upsert=True)

        # # your code to delete the item from MongoDB here
        # collections.update_many(deleteNodefind, {"$set": deleteNodeValue}, upsert=True)
        oltCollection.delete_many(deleteNodefind)

    return ({"message": "200"})
    # return redirect('/')


@app.route("/chart-data/<string:routerName>/<string:pppoeClient>", methods=['GET'])
def chart_data(routerName=None, pppoeClient=None) -> Response:
    device = routerName
    pppoeClient = pppoeClient
    response = Response(stream_with_context(liveBandwidth.livetraffic(routerName=routerName, pppoeClient=pppoeClient)),
                        mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
    # app.run(debug=True)
