from flask import Flask, request, jsonify, Response
from flask_pymongo import pymongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
app = Flask(__name__)
CONNECTION_STRING = "mongodb+srv://bjavier9:Shelvykrs1995@syra-uoyzo.gcp.mongodb.net/test?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('lana')
# user_colection = pymongo.collection.Collection(db, 'user')


@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    db.users.delete_one({'id': ObjectId(id)})
    response = jsonify({'message': 'user '+id+' was deleted successfully'})
    return Response(response, mimetype='application/json')


@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    if username and password and email:
        hashed_password = generate_password_hash(password)
        db.users.update_one({'_id': ObjectId(id)}, {'$set': {
            'username': username, 'password': hashed_password, "email": email
        }})
    response = jsonify({'message': 'user '+id+' was updated successfully'})
    return Response(response, mimetype='application/json')


@app.route('/user', methods=['POST'])
def create_user():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    if username and password and email:
        hashed_password = generate_password_hash(password)
        id = db.users.insert(
            {'username': username, 'password': hashed_password, "email": email})
        response = {
            'id': str(id),
            'username': username,
            'password': password
        }
        return response
    else:
        return {'message': 'no papa no paso '}


@app.route('/users',  methods=['GET'])
def get_users():
    users = users = db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')


@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = db.users.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype='application/json')


@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resource Not Found '+request.url,
        'status': 404
    })
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True)
