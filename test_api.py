import unittest
import requests
from flask import url_for

class TestAPI(unittest.TestCase):
    def test_get_all_projects_status(self):
        r = requests.get('127.0.0.1:8080/api/projects').json()
        self.assertEqual(r.get('status'), 'OK')

    def test_get_project_by_name(self):
        r = requests.get('127.0.0.1:8080/api/projects/name/cheese').json()
        self.assertEqual(r.get('status'), 'OK')
