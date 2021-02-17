from api.v1 import api_v1
from models.storage.firestore_client import FirestoreClient
from flask import jsonify
import requests
from helpers import build_url

@api_v1.route('/projects', methods=['GET'], strict_slashes=False)
def all_projects():
    db = FirestoreClient()
    projects = db.get_all_by_class('Project')
    if len(projects) == 0:
        return jsonify({'Status': 'error', 'projects': []}), 400
    return jsonify({'Status': 'OK', 'projects': projects}), 200

@api_v1.route('/projects/nam/<name>', methods=['GET'], strict_slashes=False)
def project_by_name(name):
    r = requests.get(build_url('api/projects')).json()
    if r.get('status') == 'error':
        return jsonify({'Status': 'error', 'projects': {}}), 400
    projects = r.get('projects')
    for item in projects:
        if item.name == name:
            return jsonify({'Status': 'OK', 'projects': item}), 200
    return jsonify({'Status': 'error', 'projects': {}}), 400
