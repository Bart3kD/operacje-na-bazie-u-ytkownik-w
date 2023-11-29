import json
from main import app
from unittest.mock import mock_open, patch
from functions import load_json, get_data, find_first_free_id, insert_user, update_user, delete_user, update_or_create_user



def test_load_json() -> None:
    with patch('builtins.open', new_callable=mock_open, read_data='[{"id": 1, "name": "John", "lastname": "Doe"}]'):
        data = load_json()
        assert data == [{"id": 1, "name": "John", "lastname": "Doe"}]



def test_get_data_all_users() -> None:
    with patch('functions.load_json', return_value=[{"id": 1, "name": "John", "lastname": "Doe"}, {"id": 2, "name": "Jane", "lastname": "Smith"}]):
        data = get_data()
        assert data == [{"id": 1, "name": "John", "lastname": "Doe"}, {"id": 2, "name": "Jane", "lastname": "Smith"}]



def test_get_data_single_user() -> None:
    with patch('functions.load_json', return_value=[{"id": 1, "name": "John", "lastname": "Doe"}, {"id": 2, "name": "Jane", "lastname": "Smith"}]):
        user_id = 1
        data = get_data(user_id)
        assert data == [{"id": 1, "name": "John", "lastname": "Doe"}]



def test_find_first_free_id() -> None:
    with patch('functions.load_json', return_value=[{"id": 1}, {"id": 3}, {"id": 5}]):
        first_free_id = find_first_free_id()
        assert first_free_id == 2



def test_insert_user() -> None:
    request_data = {'json': {'name': 'John', 'lastname': 'Doe'}}

    with app.test_request_context('/users', json=request_data['json']):
        with patch('functions.load_json', return_value=[]):
            with patch('functions.find_first_free_id', return_value=1):
                response = insert_user(request_data['json'])
                assert response[1] == 201




def test_update_user() -> None:
    user_id = 1
    updated_name = 'UpdatedName'
    request_data = {'json': {'name': updated_name}}
    
    with app.test_request_context(f'/users/{user_id}', json=request_data['json']):
        with patch('functions.load_json', return_value=[{"id": 1, "name": "John", "lastname": "Doe"}]):
            response = update_user(user_id)
            assert response[1] == 204



def test_delete_user() -> None:
    user_id = 1
    
    with app.test_request_context(f'/users/{user_id}'):
        with patch('functions.load_json', return_value=[{"id": 1, "name": "John", "lastname": "Doe"}]):
            response = delete_user(user_id)
            assert response[1] == 204

def test_update_or_create_user() -> None:
    user_id = 1
    updated_name = 'UpdatedName'
    updated_lastname = 'UpdatedLastName'
    request_data = {'json': {'name': updated_name, 'lastname': updated_lastname}}

    with app.test_request_context(f'/users/{user_id}', json=request_data['json']):
        with patch('functions.load_json', return_value=[{"id": 1, "name": "John", "lastname": "Doe"}]):
            with patch('functions.find_first_free_id', return_value=2):
                with patch('functions.save_json') as mock_save_json:
                    response = update_or_create_user(user_id)
                    assert response[1] == 204

    mock_save_json.assert_called_once_with([{"id": 1, "name": "UpdatedName", "lastname": "UpdatedLastName"}])

