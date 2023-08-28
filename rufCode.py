@app.route('/mikrotikSyncClient/<string:router_id>', methods=['GET'])
def clientSync(router_id):
    device = "A1_ACR"

    print(router_id)

    secretClients = routerApi.routerdata(
        routerName=device, pppoeSecret="pppoeSecretClient")

    print(secretClients)
    selectRouter = mongo.db.mikrotik.find_one({'_id': ObjectId(router_id)})
    print("ra", selectRouter["_id"])

    data = []
    for secretClient in secretClients:
        # print(secretClient)

        data.append({

            "selectRouter": selectRouter["_id"],  # Convert ObjectId to string
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

    # Exclude the _id field from the inserted documents
    mongo.db.pppoeUsers.insert_many(data, ordered=False)

    pipeline = [
        {
            '$lookup': {
                'from': 'mikrotik',
                'localField': 'selectRouter',
                'foreignField': '_id',
                'as': 'routerName'
            }
        },
        {
            '$replaceRoot': {
                'newRoot': {
                    '$mergeObjects': [
                        {'$arrayElemAt': ['$routerName', 0]},
                        '$$ROOT'
                    ]
                }
            }
        },
        {
            '$project': {
                '_id': 0,  # Exclude other fields you want to hide
                'mikrotikUserName': 0,  # Exclude other fields you want to hide
                'mikrotikIp': 0,  # Exclude other fields you want to hide
                'mikrotikPort': 0,  # Exclude other fields you want to hide
                'mikrotikPassword': 0,  # Exclude other fields you want to hide
                'mikrotikDeviceId': 0,  # Exclude other fields you want to hide
                'routerName': 0,  # Exclude other fields you want to hide
                'selectRouter': 0,  # Exclude other fields you want to hide
            }
        }
    ]
    docData = []
    # Exclude the _id field from the results
    # tableDatas = mongo.db.mikrotik.find_one(ObjectId(router_id))
    # print(tableDatas)

    result = mongo.db.pppoeUsers.aggregate(pipeline)
    for doc in result:
        docData.append(doc)
        print(doc)
    print(docData)

    return jsonify(docData)
