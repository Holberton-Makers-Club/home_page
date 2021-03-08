import unittest
import requests
from flask import url_for
from helpers import build_url

class TestAPI(unittest.TestCase):
    def test_get_all_projects_status(self):
        r = requests.get(build_url('/api/projects')).json()
        self.assertEqual(r.get('status'), 'OK')

    def test_get_project_by_name(self):
        r = requests.get(build_url('/api/projects/name/cheese')).json()
        self.assertEqual(r.get('status'), 'OK')

    def test_get_all_members_status(self):
        r = requests.get(build_url('/api/members')).json()
        self.assertEqual(r.get('status'), 'OK')

if __name__ == "main":
    unittest.main()