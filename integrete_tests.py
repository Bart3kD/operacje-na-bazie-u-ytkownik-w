import unittest
import json
from flask import Flask
from flask.testing import FlaskClient
from main import app

class AppIntegrationTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_get_users(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsInstance(data, list)

    def test_get_user_by_id(self):
        response = self.app.get('/users/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsInstance(data, list)
        self.assertEqual(data[0]['id'], 1)

    def test_add_user(self):
        new_user = {"name": "John", "lastname": "Doe"}
        response = self.app.post('/users', json=new_user)
        self.assertEqual(response.status_code, 201)

    def test_change_user(self):
        updated_user_data = {"name": "UpdatedJohn", "lastname": "UpdatedDoe"}
        response = self.app.patch('/users/1', json=updated_user_data)
        self.assertEqual(response.status_code, 204)

    def test_edit_user(self):
        updated_user_data = {"name": "UpdatedJohn", "lastname": "UpdatedDoe"}
        response = self.app.put('/users/1', json=updated_user_data)
        self.assertEqual(response.status_code, 204)

    def test_remove_user(self):
        response = self.app.delete('/users/1')
        self.assertEqual(response.status_code, 204)



if __name__ == '__main__':
    unittest.main()
