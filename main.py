from flask import Flask,request,jsonify
from functions import get_data, insert_user, update_user, delete_user, update_or_create_user

app = Flask(__name__)


@app.get("/users")
def get_users():
    return jsonify(get_data())

@app.get("/users/<int:user_id>")
def get_user_by_id(user_id):
    return get_data(user_id)

@app.post("/users")
def add_users():
    insert_user(request.json)
    return "Success", 201

@app.patch('/users/<int:user_id>')
def change_user(user_id):
    return update_user(user_id)

@app.put("/users/<int:user_id>")
def edit_users(user_id):
    return update_or_create_user(user_id)


@app.delete('/users/<int:user_id>')
def remove_user(user_id):
    return delete_user(user_id)
