from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from bson.json_util import dumps  # bson.json_util is helpful for handling BSON types

from bson.objectid import ObjectId
import routerApi
from bson import ObjectId
import json
import threading
import asyncio

app = Flask(__name__)
# Change this to your preferred secret key
app.config['JWT_SECRET_KEY'] = 'Bangla321@@'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 30  # 30 minutes (in seconds)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 60  # 24 hours (in seconds)
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/your_database'  # Change the URI to your MongoDB connection string
# Change the URI to your MongoDB connection string
app.config['MONGO_URI'] = 'mongodb://192.168.100.2:27017/your_database'
app.config['MONGO_URI_2'] = 'mongodb://192.168.100.2:27017/RealTimeTraffic'
jwt = JWTManager(app)
mongo = PyMongo(app)
# Initialize the second PyMongo instance
mongo2 = PyMongo(app, uri='mongodb://192.168.100.2:27017/RealTimeTraffic')
# CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})


# decoder class, convert ObjectId object to string
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    firstName = data['firstName']
    lastName = data['lastName']
    role = "user"  # Include role in the registration data

    existing_user = mongo.db.users.find_one({'username': username})
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400

    # Get the current maximum user_id from the users collection
    max_user_id = mongo.db.users.find_one(sort=[('id', -1)])['id']
    new_user_id = max_user_id + 1 if max_user_id else 1

    hashed_password = generate_password_hash(password)
    new_user = {
        'id': new_user_id,  # Auto-incremented id field
        'username': username,
        'password': hashed_password,
        'firstName': firstName,
        'lastName': lastName,
        'role': role
    }

    mongo.db.users.insert_one(new_user)

    return jsonify({'message': 'User registered successfully'})


# Login endpoint


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    device = request.headers
    print(data)
    print(device)
    username = data['username']
    password = data['password']

    user = mongo.db.users.find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        # Include role in the response
        return jsonify(identity=username, access_token=access_token, refresh_token=refresh_token, role=user['role'])

    return jsonify({'error': 'Invalid username or password'}), 401


@app.route('/refreshToken', methods=['POST'])
@jwt_required()  # Protect the /refresh endpoint with jwt_required decorator
def refresh():
    data = request.json
    # print(data)
    refresh_token = data.get('refresh_token')

    if not refresh_token:
        return jsonify({'error': 'Refresh token is missing'}), 400

    try:
        # Add debugging statements
        # print("Received refresh token:", refresh_token)

        identity = get_jwt_identity()
        # print("Identity from refresh token:", identity)

        new_access_token = create_access_token(identity=identity)
        new_refresh_token = create_access_token(identity=identity)
        return jsonify({'access_token': new_access_token, 'refresh_token': new_refresh_token}), 200
    except Exception as e:
        # Add debugging statements
        print("Exception occurred during token refresh:", e)
        return jsonify({'error': 'Invalid refresh token'}), 401


# Protected endpoint accessible only to users with the 'admin' role
@app.route('/admin', methods=['GET'])
@jwt_required()
def admin_route():
    current_user = get_jwt_identity()
    user = mongo.db.users.find_one({'username': current_user})
    if user and user['role'] == 'admin':
        return jsonify({'message': f'Hello, {current_user}! You accessed the admin route.'})
    else:
        return jsonify({'error': 'Unauthorized access'}), 403


@app.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    current_user = get_jwt_identity()
    print(current_user)
    # user = mongo.db.users.find_one({'_id': ObjectId(current_user)})
    user = mongo.db.users.find_one({'username': current_user})
    print(user)

    if user and user['role'] == 'admin':
        users = list(mongo.db.users.find())  # Query all user documents
        user_data = []

        for user in users:
            user_data.append({
                'id': user['id'],
                'username': user['username'],
                'role': user['role'],
                'firstName': user['firstName'],
                'lastName': user['lastName']
                # Include other user properties as needed
            })

        return jsonify(user_data)

    else:
        return jsonify({'error': 'Unauthorized access'}), 403

    return jsonify({'error': 'Unprocessable Entity'}), 422


@app.route('/users/<string:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def user_detail(id):
    current_user = get_jwt_identity()
    user = mongo.db.users.find_one({'username': current_user})

    if not user or user['role'] != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 403

    target_user = mongo.db.users.find_one({'id': int(id)})

    if not target_user:
        return jsonify({'error': 'User not found'}), 404

    if request.method == 'GET':
        # Remove the MongoDB ObjectId field since it's not JSON serializable
        target_user.pop('_id', None)
        return jsonify(target_user)

    elif request.method == 'PUT':
        # Assuming you have a JSON payload with user data to update in the request body
        data = request.get_json()

        # Update the target_user dictionary with the new data
        target_user.update(data)

        # Update the user document in the database
        mongo.db.users.update_one({'id': int(id)}, {'$set': target_user})

        return jsonify({'message': 'User updated successfully'})

    elif request.method == 'DELETE':
        # Delete the user document from the database
        mongo.db.users.delete_one({'id': int(id)})

        return jsonify({'message': 'User deleted successfully'})

    return jsonify({'error': 'Unprocessable Entity'}), 422


@app.route('/tableData', methods=['GET'])
def tableData1():
    # tableDatas = mongo.db.tableData.find()
    # Exclude the _id field from the results
    tableDatas = mongo.db.userData.find({}, {"_id": 0})
    data = []  # Convert the MongoDB cursor to a list

    for tableData in tableDatas:
        data.append(tableData)
    # print(tableData)
    datas = list(tableDatas)
    return jsonify(data)

    # @app.route('/pppoeUsers', methods=['GET'])
    # def tableData():
    # # Retrieve data from the pppoeUsers collection excluding the _id field
    # pipeline = [
    #     {
    #         '$lookup': {
    #             'from': 'mikrotik',
    #             'localField': 'selectRouter',
    #             'foreignField': '_id',
    #             'as': 'routerName'
    #         }
    #     },
    #     {
    #         '$replaceRoot': {
    #             'newRoot': {
    #                 '$mergeObjects': [
    #                     {'$arrayElemAt': ['$routerName', 0]},
    #                     '$$ROOT'
    #                 ]
    #             }
    #         }
    #     },
    #     {
    #         '$project': {
    #             # '_id': 0,  # Exclude other fields you want to hide
    #             'mikrotikUserName': 0,  # Exclude other fields you want to hide
    #             'mikrotikIp': 0,  # Exclude other fields you want to hide
    #             'mikrotikPort': 0,  # Exclude other fields you want to hide
    #             'mikrotikPassword': 0,  # Exclude other fields you want to hide
    #             'mikrotikDeviceId': 0,  # Exclude other fields you want to hide
    #             'routerName': 0,  # Exclude other fields you want to hide
    #             'selectRouter': 0,  # Exclude other fields you want to hide
    #         }
    #     }
    # ]
    # # projection = {"_id": 0}
    # # tableDatas = list(mongo.db.pppoeUsers.aggregate(pipeline))
    # tableDatas = list(mongo.db.pppoeUsers.find())
    # print(tableDatas)
    # finds = mongo.db.pppoeUsers.find()
    # device = "A1_ACR"
    # secretClients = routerApi.routerdata(routerName=device, pppoeSecret="pppoeSecretClient")
    # userOnlinedata = []
    # for document in finds:
    #     pppoe_username = document["pppoeUserName"]
    #     for secret_client in secretClients:
    #         if secret_client["name"] != pppoe_username:
    #             # Perform your update operation here
    #             # For example, update a field in the document
    #             document["status"] = "online"
    #             userOnlinedata.append(document)
    #
    # # print(userOnlinedata)
    # return json.dumps(userOnlinedata, cls=JSONEncoder)


# @app.route('/pppoeUsers', methods=['GET'])
# def tableData():
#     finds = mongo.db.pppoeUsers.find()
#     device = "A1_ACR"
#     secretClients = routerApi.routerdata(routerName=device, pppoeActive="pppoeActiveClient")
#
#     online_user_data = []
#
#     for document in finds:
#         pppoe_username = document["pppoeUserName"]
#         if any(secret_client["name"] == pppoe_username for secret_client in secretClients):
#             document["status"] = "online"
#         else:
#             document["status"] = "offline"
#         online_user_data.append(document)
#
#     return json.dumps(online_user_data, cls=JSONEncoder)


async def fetch_secret_clients(device):
    device = "A1_ACR"
    return routerApi.routerdata(routerName=device, pppoeActive="pppoeActiveClient")


async def process_documents(finds, secret_clients):
    online_user_data = []

    for document in finds:
        pppoe_username = document["pppoeUserName"]
        if any(secret_client["name"] == pppoe_username for secret_client in secret_clients):
            document["status"] = "online"
        else:
            document["status"] = "offline"
        online_user_data.append(document)

    return online_user_data


@app.route('/pppoeUsers', methods=['GET'])
async def tableData():
    finds = mongo.db.pppoeUsers.find()
    device = "A1_ACR"

    secret_clients = await fetch_secret_clients(device)
    online_user_data = await process_documents(finds, secret_clients)

    return json.dumps(online_user_data, cls=JSONEncoder)


@app.route('/addPPPoEuser', methods=['POST'])
def addPPPoEuser():
    data = request.json
    print(data)
    selectRouter = data.get('selectRouter')
    selectPackage = data.get('selectPackage')
    pppoeUserName = data.get('pppoeUserName')
    pppoePassword = data.get('pppoePassword')
    selectZone = data.get('selectZone')
    selectSubZone = data.get('selectSubZone')
    userName = data.get('userName')
    userMobile = data.get('userMobile')
    userEmail = data.get('userEmail')
    userHouse = data.get('userHouse')
    userRoad = data.get('userRoad')
    userAddress = data.get('userAddress')
    userDistrict = data.get('userDistrict')
    userDivision = data.get('userDivision')
    userThana = data.get('userThana')
    userNiDNumber = data.get('userNiDNumber')
    userCableType = data.get('userCableType')
    userOnuMac = data.get('userOnuMac')
    userRouterMacAddress = data.get('userRouterMacAddress')
    userRequireCable = data.get('userRequireCable')
    usertypeOfConnectivity = data.get('usertypeOfConnectivity')
    userBillingType = data.get('userBillingType')
    userMonthlyBill = data.get('userMonthlyBill')
    userConnectionDate = data.get('userConnectionDate')
    userBillingCycle = data.get('userBillingCycle')
    userReferenceName = data.get('userReferenceName')
    userReferenceMobile = data.get('userReferenceMobile')
    userBillingsMobile = data.get('userBillingsMobile')
    userAutomaticConnectionOff = data.get('userAutomaticConnectionOff')

    mongo.db.pppoeUsers.insert_one({
        "selectRouter": selectRouter,
        "selectPackage": selectPackage,
        "pppoeUserName": pppoeUserName,
        "pppoePassword": pppoePassword,

        "selectZone": selectZone,
        "selectSubZone": selectSubZone,
        "userName": userName,
        "userMobile": userMobile,
        "userEmail": userEmail,
        "userHouse": userHouse,
        "userRoad": userRoad,
        "userAddress": userAddress,
        "userDistrict": userDistrict,
        "userDivision": userDivision,
        "userThana": userThana,
        "userNiDNumber": userNiDNumber,
        "userCableType": userCableType,
        "userOnuMac": userOnuMac,
        "userRouterMacAddress": userRouterMacAddress,
        "userRequireCable": userRequireCable,
        "usertypeOfConnectivity": usertypeOfConnectivity,
        "userBillingType": userBillingType,
        "userMonthlyBill": userMonthlyBill,
        "userConnectionDate": userConnectionDate,
        "userBillingCycle": userBillingCycle,
        "userReferenceName": userReferenceName,
        "userReferenceMobile": userReferenceMobile,
        "userBillingsMobile": userBillingsMobile,
        "userAutomaticConnectionOff": userAutomaticConnectionOff
    })

    response = {'message': 'Data received and stored in MongoDB'}
    return jsonify(response)


@app.route('/removePPPoEuser/<string:package_id>', methods=['DELETE'])
def removePPPoEuser(package_id):
    try:
        print(package_id)
        mongo.db.pppoeUsers.delete_one({'_id': ObjectId(package_id)})
        return jsonify({'message': 'Device removed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/mikrotik', methods=['GET'])
def networkDevices():
    tableDatas = mongo.db.mikrotik.find()  # Exclude the _id field from the results
    print(tableDatas)
    mikrotikData = []  # Convert the MongoDB cursor to a list

    for tableData in tableDatas:
        print(tableData)
        mikrotikData.append(tableData)
        # data.append({
        #     "_id": str(tableData["_id"]),
        #     "mikrotikName": tableData["mikrotikName"],
        #     "mikrotikUserName": tableData["mikrotikUserName"],
        #     "mikrotikIp": tableData["mikrotikIp"],
        #     "mikrotikPort": tableData["mikrotikPort"],
        #     "mikrotikPassword": tableData["mikrotikPassword"],
        # })
        # print(data)

    return json.dumps(mikrotikData, cls=JSONEncoder)

    # return jsonify(data)


@app.route('/addMikrotik', methods=['POST'])
def addMikrotik():
    data = request.json
    print(data)

    mikrotikName = data.get('mikrotikName')
    mikrotikUserName = data.get('mikrotikUserName')
    mikrotikIp = data.get('mikrotikIp')
    mikrotikPort = data.get('mikrotikPort')
    mikrotikPassword = data.get('mikrotikPassword')
    mikrotikHashedPassword = generate_password_hash(mikrotikPassword)

    mongo.db.mikrotik.insert_one({
        "mikrotikName": mikrotikName,
        "mikrotikUserName": mikrotikUserName,
        "mikrotikIp": mikrotikIp,
        "mikrotikPort": mikrotikPort,
        "mikrotikPassword": mikrotikHashedPassword,
        "sequence": 0,
        "id": 1,

    })

    response = {'message': 'Data received and stored in MongoDB'}
    return jsonify(response)


@app.route("/updateMikrotik/<string:device_id>", methods=["PUT"])
def update_mikrotik(device_id):
    try:
        device = mongo.db.mikrotik.find_one({'_id': ObjectId(device_id)})
        if not device:
            return jsonify({"error": "Device not found"}), 404

        updated_data = request.json  # Assuming you're sending JSON data in the request body
        mongo.db.mikrotik.update_one(
            {'_id': ObjectId(device_id)}, {"$set": updated_data})
        return jsonify({"message": "Device updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/removeMikrotik/<string:device_id>', methods=['DELETE'])
def remove_device(device_id):
    try:
        mongo.db.mikrotik.delete_one({'_id': ObjectId(device_id)})
        return jsonify({'message': 'Device removed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def document_exists(collection, query):
    return collection.find_one(query) is not None


def insert_documents(collection, documents):
    if documents:
        collection.insert_many(documents, ordered=False)


@app.route('/mikrotikSyncClient/<string:router_id>', methods=['GET'])
def clientSync(router_id):
    device = "A1_ACR"
    secretClients = routerApi.routerdata(routerName=device, pppoeSecret="pppoeSecretClient")

    findRouter = mongo.db.mikrotik.find_one({'_id': ObjectId(router_id)})

    def get_next_sequence_value(sequence_name):
        sequence_document = mongo.db.mikrotik.find_one_and_update(
            {'_id': ObjectId(router_id)},
            {"$inc": {"id": 1}},
            upsert=True,
        )
        return sequence_document["id"]

    # Check if documents exist and insert if not
    secretClientData = []
    for secretClient in secretClients:
        if not document_exists(mongo.db.pppoeUsers, {"pppoeUserName": secretClient["name"]}):
            user_id = get_next_sequence_value(0)  # Get the next user ID
            # print("userId", user_id)
            secretClientData.append({
                "id": user_id,
                "selectRouter": findRouter["_id"],  # Convert ObjectId to string
                "selectPackage": secretClient["profile"],
                "pppoeUserName": secretClient["name"],
                "pppoePassword": secretClient["password"],
                "service": secretClient["service"],
                # "status": secretClient["disabled"],
                "status": "offline",
                "last-logged-out": secretClient["last-logged-out"],
                "selectZone": "",
                "selectSubZone": None,
                "userName": None,
                "userMobile": None,
                "userEmail": None,
                "userHouse": None,
                "userRoad": None,
                "userAddress": None,
                "userDistrict": None,
                "userDivision": None,
                "userThana": None,
                "userNiDNumber": None,
                "userCableType": None,
                "userOnuMac": None,
                "userRouterMacAddress": secretClient["caller-id"],
                "userRequireCable": None,
                "usertypeOfConnectivity": None,
                "userBillingType": None,
                "userMonthlyBill": None,
                "userConnectionDate": None,
                "userBillingCycle": None,
                "userReferenceName": None,
                "userReferenceMobile": None,
                "userBillingsMobile": None,
                "userAutomaticConnectionOff": None
            })
    insert_documents(mongo.db.pppoeUsers, secretClientData)

    # Aggregation pipeline
    mikrotikSyncClientPipeline = [
        {
            '$lookup': {
                'from': 'mikrotik',
                'localField': 'selectRouter',
                'foreignField': '_id',
                'as': 'routerName'
            }
        },
    ]

    syncData = list(mongo.db.pppoeUsers.aggregate(mikrotikSyncClientPipeline))

    # return jsonify(syncData)
    return json.dumps(syncData, cls=JSONEncoder)


# @app.route('/packageSync', methods=['GET'])
@app.route('/mikrotikSyncPackage/<string:router_id>', methods=['GET'])
def packageSync(router_id):
    print(router_id)
    device = "A1_ACR"
    findRouter = mongo.db.mikrotik.find_one({'_id': ObjectId(router_id)})

    syncPackages = routerApi.routerdata(routerName=device, pppoeProfile="pppoeProfile")
    filtered_packages = [package for package in syncPackages if
                         package.get("name") not in {"default", "default-encryption"}]
    print(type(filtered_packages))
    # print(syncPackages)

    jsons = json.dumps(filtered_packages, indent=4)

    syncPackageData = []
    for syncPackage in filtered_packages:
        if not document_exists(mongo.db.pppoePackage, {"package": syncPackage["name"]}):
            syncPackageData.append({
                "package": syncPackage["name"],
                "rate": 0,
                "Name": None,
                "routerOwner": findRouter["_id"],  # Convert ObjectId to string

            })

    insert_documents(mongo.db.pppoePackage, syncPackageData)

    mikrotikSyncPackagePipeline = [
        {
            '$lookup': {
                'from': 'mikrotik',
                'localField': 'routerOwner',
                'foreignField': '_id',
                'as': 'routerName'
            }
        },
        {
            '$project': {
                'routerOwner': 0,
                "routerName": 0
            }
        }
    ]
    # syncData = list(mongo.db.pppoePackage.find())
    syncDatas = list(mongo.db.pppoePackage.aggregate(mikrotikSyncPackagePipeline))
    # print(syncData)

    return json.dumps(syncDatas, cls=JSONEncoder)


@app.route('/mikrotikPackage/<string:router_id>', methods=['GET'])
def package(router_id):
    print(router_id)
    device = "A1_ACR"
    findRouter = mongo.db.pppoePackage.find({'routerOwner': ObjectId(router_id)})
    print(findRouter)

    mikrotikSyncPackagePipeline = [
        {
            '$lookup': {
                'from': 'mikrotik',
                'localField': 'routerOwner',
                'foreignField': '_id',
                'as': 'routerName'
            }
        },
        {
            '$project': {
                'routerOwner': 0,
                "routerName": 0
            }
        }
    ]
    # syncData = list(mongo.db.pppoePackage.find())
    # syncDatas = list(mongo.db.pppoePackage.aggregate(mikrotikSyncPackagePipeline))
    syncDatas = list(findRouter)
    # print(syncData)

    return json.dumps(syncDatas, cls=JSONEncoder)


@app.route("/updateSyncPackage/<string:device_id>", methods=["PUT"])
def update_package(device_id):
    try:
        device = mongo.db.pppoePackage.find_one({'_id': ObjectId(device_id)})
        print(device)

        if not device:
            return jsonify({"error": "Device not found"}), 404

        updated_data = request.json  # Assuming you're sending JSON data in the request body
        selectRouter = updated_data.get('selectRouter')
        print(selectRouter)
        mongo.db.pppoePackage.update_one(
            {'_id': ObjectId(device_id)}, {"$set": updated_data})
        return jsonify({"message": "Device updated successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.route('/removeSyncPackage/<string:package_id>', methods=['DELETE'])
def removeSyncPackage(package_id):
    try:
        print(package_id)
        mongo.db.pppoePackage.delete_one({'_id': ObjectId(package_id)})
        return jsonify({'message': 'Device removed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5005)
