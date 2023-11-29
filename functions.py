import json
from flask import request, jsonify


def load_json():

    document = open('data.json')
    
    data = json.load(document)

    document.close()

    return data


def save_json(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=2)



def get_data(id: int = 0):

    data = load_json()

    if id:
        if id not in [user["id"] for user in data]:
            return jsonify({"error": f"User with ID {id} not found"}), 404

        return [user for user in data if user["id"] == id]
    else:
        return data



def find_first_free_id() -> int:

    data = load_json()

    taken_ids = [item["id"] for item in data]

    first_free_id = next(i for i in range(1, max(taken_ids) + 2) if i not in taken_ids)


    return first_free_id


def insert_user(user_data):
    if not user_data or "name" not in user_data or "lastname" not in user_data:
        return jsonify({"error": "Invalid request body"}), 400

    users = load_json()

    new_user_id = find_first_free_id()

    new_user = {
        "id": new_user_id,
        "name": user_data["name"],
        "lastname": user_data["lastname"]
    }

    users.append(new_user)

    save_json(users)

    return '', 201


def update_user(user_id: int = 0):
    if not user_id:
        return jsonify({"error": "Id is required"}), 400

    users = load_json()

    user = next((u for u in users if u['id'] == user_id), None)

    if user is None:
        return jsonify({"error": "User not found"}), 400

    if not request.json:
        return jsonify({"error": "Request body is empty or in the wrong format"}), 400

    for key, value in request.json.items():
        if key in ["name", "lastname"]:
            user[key] = value
        else:
            return jsonify({"error": f"Invalid field: {key}"}), 400

    return '', 204


def delete_user(user_id: int = 0):
    if user_id:

        users = load_json()
        user = next((u for u in users if u['id'] == user_id), None)

        if user is None:
            return jsonify({"error": "User not found"}), 400
        
        users = [u for u in users if u.get('id') != user_id]

        return '', 204

    return jsonify({"error": "User doesn't exist"}), 400


def update_or_create_user(user_id: int = 0):
    users = load_json()

    user = next((u for u in users if u['id'] == user_id), None)

    if user is None:
        new_user_id = find_first_free_id()
        new_user = {
            "id": new_user_id,
            "name": request.json.get("name", ""),
            "lastname": request.json.get("lastname", "")
        }
        users.append(new_user)
    else:
        if not request.json:
            return jsonify({"error": "Request body is empty or in the wrong format"}), 400

        for key, value in request.json.items():
            if key in ["name", "lastname"]:
                user[key] = value
            else:
                return jsonify({"error": f"Invalid field: {key}"}), 400

    save_json(users)

    return '', 204
