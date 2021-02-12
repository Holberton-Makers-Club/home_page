from API import api_v1
from storage.firestore_client import FirestoreClient
from flask import jsonify
import requests

@api_v1.route('/projects', methods=['GET'], strict_slashes=False)
def all_projects():
    db = FirestoreClient()
    projects = db.get_all_by_class('Project')
    if len(projects) == 0:
        return jsonify({'Status': 'error', 'projects': []}), 400
    return jsonify({'Status': 'OK', 'projects': projects}), 200

@api_v1.route('projects/name/<str: name>', methods=['GET'], strict_slashes=False)
def project_by_name(name):
    r = requests.get('127.0.0.1:8080/api/projects/').json()
    if r.get('status') == 'error':
        return jsonify({'Status': 'error', 'projects': {}}), 400
    projects = r.get('projects')
    for item in projects:
        if item.name == name:
            return jsonify({'Status': 'OK', 'projects': item}), 200
    return jsonify({'Status': 'error', 'projects': {}}), 400
