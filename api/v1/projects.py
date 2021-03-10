from api.v1 import api_v1
from models.storage.firestore_client import FirestoreClient
from flask import jsonify
import requests
from helpers import build_url
from models.projects import Project

@api_v1.route('/projects', methods=['GET'], strict_slashes=False)
def all_projects():
    projects = Project.get_by_class()
    print(projects)
    if len(projects) == 0:
        return jsonify({'status': 'error', 'projects': []}), 400
    return jsonify({'status': 'OK', 'projects': projects}), 200

@api_v1.route('/projects/name/<name>', methods=['GET'], strict_slashes=False)
def project_by_name(name):
    r = requests.get(build_url('api/projects')).json()
    if r.get('status') == 'error':
        return jsonify({'status': 'error', 'projects': {}}), 400
    projects = r.get('projects')
    for item in projects:
        if item.name == name:
            return jsonify({'status': 'OK', 'projects': item}), 200
    return jsonify({'status': 'error', 'projects': {}}), 400

@api_v1.route('/projects/<id>', methods=['GET'], strict_slashes=False)
def project_by_id(id):
    r = requests.get(build_url('api/projects')).json()
    if r.get('status') == 'error':
        return jsonify({'status': 'error', 'project': {}}), 400
    projects = r.get('projects')
    for project in projects:
        if project.get("id") == id:
            return jsonify({'status': 'OK', 'project': project}), 200
    return jsonify({'status': 'error', 'project': {}}), 400
