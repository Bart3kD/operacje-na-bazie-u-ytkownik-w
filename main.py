from flask import Flask,request,jsonify,json
from functions import get_data, find_first_free_id, insert_user, update_user

app = Flask(__name__)


@app.route("/users", methods=['GET'])
def get_users():
    return jsonify(get_data())

@app.route("/users/<int:user_id>", methods=['GET'])
def get_user_by_id(user_id):
    return get_data(user_id)

@app.route("/users",methods=['POST'])
def add_users():
    insert_user(request.json)
    return "Success", 201

@app.route('/users/<int:user_id>', methods=['PATCH'])
def patch_user(user_id):
    return update_user(user_id)
