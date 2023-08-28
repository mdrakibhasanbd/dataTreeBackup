from pymongo import MongoClient
import json

# Connect to the MongoDB server
client = MongoClient('mongodb://localhost:27017/')

# Access the database and collection
db = client['mongodbVSCodePlaygroundDB']
collection = db['sales']

# Define the aggregation pipeline
pipeline = [
    {
        '$lookup': {
            'from': 'users',
            'localField': 'parrent_id',
            'foreignField': '_id',
            'as': 'router'
        }
    },
    {
        '$match': {
            'router': {'$ne': []}
        }
    }
]

# Execute the aggregation query
result = collection.aggregate(pipeline)

data =[]
# Access the "name" field within the "router" array
for document in result:
    router_name = document['router'][0]
    data.append(router_name)


# Convert data to JSON format
json_data = json.dumps(data)
print(json_data)

# Close the MongoDB connection
client.close()
