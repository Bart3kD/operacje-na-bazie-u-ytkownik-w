import json
from flask import request, jsonify


def load_json():
    document = open('data.json')
    data = json.load(document)
    document.close()
    return data

def get_data(id: int = 0):
    data = load_json()
    if id:
        return [user for user in data if user["id"] == id]
    else:
        return data
    
def find_first_free_id() -> int:
    data = load_json()
    taken_ids = [item["id"] for item in data]
    first_free_id = next(i for i in range(1, max(taken_ids) + 2) if i not in taken_ids)
    return first_free_id

def update_user(user_id: int = 0):

    if user_id:

        users = load_json()
        user = next((u for u in users if u['id'] == user_id), None)

        if user is None:
            return jsonify({"error": "User not found"}), 404

        if not request.json:
            return jsonify({"error": "Request body is empty or in the wrong format"}), 400

        for key, value in request.json.items():
            if key in ["name", "lastname"]:
                user[key] = value
            else:
                return jsonify({"error": f"Invalid field: {key}"}), 400

        return '', 204
    
    return jsonify({"error": "Id is requied"}), 400
