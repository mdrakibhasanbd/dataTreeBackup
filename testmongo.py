from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['device']
collection = db['data1']

@app.route('/')
def index():
    return render_template('rename.html')

@app.route('/delete/<string:item_id>', methods=['POST'])
def delete_item(item_id):
    print(item_id)

    # your code here


    # result = collection.delete_one({'_id': item_id})


if __name__ == '__main__':
    app.run(debug=True)

