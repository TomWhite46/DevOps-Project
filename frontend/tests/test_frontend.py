import unittest
from flask_testing import TestCase
from flask import url_for, jsonify
import requests
import requests_mock


from application import app
from os import getenv

class TestBase(TestCase):
    def create_app(self):
        config_name = 'testing'
        return app
    
class TestViews(TestBase):
    def test_backend_response(self):
        with requests_mock.Mocker() as mock:
            mock.get('http://backend:5001/backend', json={"test": "test"})
            response = self.client.get(url_for('get_users'))
            self.assertEqual(response.status_code, 200)
