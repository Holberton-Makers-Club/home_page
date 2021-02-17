#!/usr/bin/python3
import unittest
from models.storage.firestore_client import FirestoreClient
from models.projects import Project

'''DOCSTRING'''


class testFirestore(unittest.TestCase):
    def setUp(self):
        self.firestore_client = FirestoreClient()
        self.project = Project()
    
    def test_connection(self):
         self.assertTrue(self.firestore_client.connected())

    def test_get_all_by_class_type(self):
        self.assertEquals(type(self.firestore_client.get_all_by_class('Project')), list)

    def test_get_all_by_class_len(self):
        self.assertTrue(len(self.firestore_client.get_all_by_class('Project')) > 0)

if __name__ == "__main__":
    unittest.main()