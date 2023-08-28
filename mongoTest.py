from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
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

# Retrieve documents from collection
finds = mongo.db.pppoeUsers.find()
device = "A1_ACR"
secretClients = routerApi.routerdata(routerName=device, pppoeSecret="pppoeSecretClient")
# Print retrieved documents

userOnlinedata = []
for document in finds:
    pppoe_username = document["pppoeUserName"]
    for secret_client in secretClients:
        if secret_client["name"] == pppoe_username:
            # Perform your update operation here
            # For example, update a field in the document
            document["status"] = "online"
            userOnlinedata.append(document)

print(userOnlinedata)
