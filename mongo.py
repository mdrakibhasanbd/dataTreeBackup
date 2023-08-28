import pymongo

# Connect to the MongoDB database
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["device"]
collections = mydb.data1
collections1 = mydb.counters
# collections = mydb.data1.find({"rootId":1})
# collections = mydb.data1.delete_many({"rootId":7})
# collections = mydb.data1.find({"_id":{ "$eq":7 }},
#                                      {"$set":{ "icon":"user" }}
#                                      )

# data = collections.find().count()

PON = [{
  "_id": 1,
  "rootId": None,
  "name": "Olt",
  "addedName": "Olt",
  "type": "green",
  "level": "purple",
  "icon": "static/image/olt.png"
},{
  "_id": 2,
  "rootId": 1,
  "name": "pon-1",
  "addedName": "pon-1",
  "type": "grey",
  "level": "purple",
  "icon": "static/image/pon.png",
  "nodetype": "pon",
  "searchable": None,
  "value": None
},{
  "_id": 3,
  "rootId": 1,
  "name": "pon-2",
  "addedName": "pon-2",
  "type": "grey",
  "level": "purple",
  "icon": "static/image/pon.png",
  "nodetype": "pon",
  "searchable": None,
  "value": None
},{
  "_id": 4,
  "rootId": 1,
  "name": "pon-3",
  "addedName": "pon-3",
  "type": "grey",
  "level": "purple",
  "icon": "static/image/pon.png",
  "nodetype": "pon"
},{
  "_id": 5,
  "rootId": 1,
  "name": "pon-4",
  "addedName": "pon-4",
  "type": "grey",
  "level": "purple",
  "icon": "static/image/pon.png",
  "nodetype": "pon"
}
]
userData =   [{
  "_id": 1,
  "rootId": None,
  "name": "Olt",
  "addedName": "Olt",
  "type": "green",
  "level": "purple",
  "icon": "static/image/olt.png"
},{
  "_id": 2,
  "rootId": 1,
  "name": "pon-1",
  "addedName": "pon-1",
  "type": "grey",
  "level": "purple",
  "icon": "static/image/pon.png",
  "nodetype": "pon",
  "searchable": None,
  "value": None
},{
  "_id": 3,
  "rootId": 1,
  "name": "pon-2",
  "addedName": "pon-2",
  "type": "grey",
  "level": "purple",
  "icon": "static/image/pon.png",
  "nodetype": "pon",
  "searchable": None,
  "value": None
},{
  "_id": 4,
  "rootId": 1,
  "name": "pon-3",
  "addedName": "pon-3",
  "type": "grey",
  "level": "purple",
  "icon": "static/image/pon.png",
  "nodetype": "pon"
},{
  "_id": 5,
  "rootId": 1,
  "name": "pon-4",
  "addedName": "pon-4",
  "type": "grey",
  "level": "purple",
  "icon": "static/image/pon.png",
  "nodetype": "pon"
},{
  "_id": 6,
  "rootId": 2,
  "name": "PLC-1",
  "addedName": "PLC-1",
  "level": "Blue",
  "value": None,
  "nodetype": "firstPlc",
  "icon": "static/image/splitter.png",
  "searchable": "YES"
},{
  "_id": 7,
  "rootId": 6,
  "name": "PORT-1",
  "addedName": "PORT-1",
  "level": "blue",
  "value": 8,
  "nodetype": "core"
},{
  "_id": 8,
  "rootId": 6,
  "name": "PORT-2",
  "addedName": "PORT-2",
  "level": "orange",
  "value": 8,
  "nodetype": "core"
},{
  "_id": 9,
  "rootId": 6,
  "name": "PORT-3",
  "addedName": "PORT-3",
  "level": "green",
  "value": 8,
  "nodetype": "core"
},{
  "_id": 10,
  "rootId": 6,
  "name": "PORT-4",
  "addedName": "PORT-4",
  "level": "brown",
  "value": 8,
  "nodetype": "core"
},{
  "_id": 11,
  "rootId": 6,
  "name": "PORT-5",
  "addedName": "PORT-5",
  "level": "grey",
  "value": 8,
  "nodetype": "core"
},{
  "_id": 12,
  "rootId": 6,
  "name": "PORT-6",
  "addedName": "PORT-6",
  "level": "white",
  "value": 8,
  "nodetype": "core"
},{
  "_id": 13,
  "rootId": 6,
  "name": "PORT-7",
  "addedName": "PORT-7",
  "level": "red",
  "value": 8,
  "nodetype": "core"
},{
  "_id": 14,
  "rootId": 6,
  "name": "PORT-8",
  "addedName": "PORT-8",
  "level": "black",
  "value": 8,
  "nodetype": "core"
},{
  "_id": 15,
  "rootId": 3,
  "name": "PLC-2",
  "addedName": "PLC-2",
  "level": "Orange",
  "value": None,
  "nodetype": "firstPlc",
  "icon": "static/image/splitter.png",
  "searchable": "YES"
},{
  "_id": 16,
  "rootId": 15,
  "name": "PORT-1",
  "addedName": "PORT-1",
  "level": "blue",
  "value": 8,
  "nodetype": "core"
},{
  "_id": 17,
  "rootId": 15,
  "name": "PORT-2",
  "addedName": "PORT-2",
  "level": "orange",
  "value": 8,
  "nodetype": "core"
},{
  "_id": 18,
  "rootId": 15,
  "name": "PORT-3",
  "addedName": "PORT-3",
  "level": "green",
  "value": 8,
  "nodetype": "core"
},{
  "_id": 19,
  "rootId": 15,
  "name": "PORT-4",
  "addedName": "PORT-4",
  "level": "brown",
  "value": 8,
  "nodetype": "core"
},{
  "_id": 20,
  "rootId": 15,
  "name": "PORT-5",
  "addedName": "PORT-5",
  "level": "grey",
  "value": 8,
  "nodetype": "core"
},{
  "_id": 21,
  "rootId": 15,
  "name": "PORT-6",
  "addedName": "PORT-6",
  "level": "white",
  "value": 8,
  "nodetype": "core"
},{
  "_id": 22,
  "rootId": 15,
  "name": "PORT-7",
  "addedName": "PORT-7",
  "level": "red",
  "value": 8,
  "nodetype": "core"
},{
  "_id": 23,
  "rootId": 15,
  "name": "PORT-8",
  "addedName": "PORT-8",
  "level": "black",
  "value": 8,
  "nodetype": "core"
},{
  "_id": 24,
  "rootId": 7,
  "name": "ceo",
  "addedName": "ceo",
  "value": 8,
  "searchable": "YES",
  "type": "red",
  "icon": "static/image/router.png",
  "level": "blue",
  "nodetype": "user"
},{
  "_id": 25,
  "rootId": 8,
  "name": "mhp-ataurrahman@224",
  "addedName": "mhp-ataurrahman@224",
  "value": 8,
  "searchable": "YES",
  "type": "red",
  "icon": "static/image/router.png",
  "level": "orange",
  "nodetype": "user"
},{
  "_id": 26,
  "rootId": 9,
  "name": "mhp-sowkothome@319",
  "addedName": "mhp-sowkothome@319",
  "value": 8,
  "searchable": "YES",
  "type": "red",
  "icon": "static/image/router.png",
  "level": "green",
  "nodetype": "user"
},{
  "_id": 27,
  "rootId": 10,
  "name": "mhp-babukaka2@3",
  "addedName": "mhp-babukaka2@3",
  "value": 8,
  "searchable": "YES",
  "type": "red",
  "icon": "static/image/router.png",
  "level": "brown",
  "nodetype": "user"
}]
mydb.drop_collection(collections)
mydb.drop_collection(collections1)
# collections.insert_many(userData)
collections.insert_many(PON)