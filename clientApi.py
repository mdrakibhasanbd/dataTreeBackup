from quart import Quart, jsonify
import asyncio
import motor.motor_asyncio
import json
from bson.objectid import ObjectId
import routerApi

app = Quart(__name__)


@app.route('/mikrotikSyncClient/<string:router_id>', methods=['GET'])
async def clientSync(router_id):
    device = "A1_ACR"
    secretClients = routerApi.routerdata(routerName=device, pppoeSecret="pppoeSecretClient")

    findRouter = await mongo_db.mikrotik.find_one({'_id': ObjectId(router_id)})

    def get_next_sequence_value(sequence_name):
        sequence_document = mongo_db.mikrotik.find_one_and_update(
            {'_id': ObjectId(router_id)},
            {"$inc": {"id": 1}},
            upsert=True,
        )
        return sequence_document["id"]

    # ... (other code)

    # Check if documents exist and insert if not
    # ... (other code)

    secretClientData = []
    for secretClient in secretClients:
        if not document_exists(mongo.db.pppoeUsers, {"pppoeUserName": secretClient["name"]}):
            user_id = get_next_sequence_value(0)  # Get the next user ID
            secretClientData.append({
                "id": user_id,
                "selectRouter": findRouter["_id"],  # Convert ObjectId to string
                "selectPackage": secretClient["profile"],
                "pppoeUserName": secretClient["name"],
                "pppoePassword": secretClient["password"],
                "service": secretClient["service"],
                "status": secretClient["disabled"],
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

    await insert_documents_async(mongo_db.pppoeUsers, secretClientData)

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

    syncData = []
    async for document in mongo_db.pppoeUsers.aggregate(mikrotikSyncClientPipeline):
        syncData.append(document)

    return jsonify(syncData)


if __name__ == '__main__':
    mongo_client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')
    mongo_db = mongo_client['your_database_name']
    app.run(debug=True, port=5001, host='0.0.0.0')
