from api.v1 import api_v1
from models.storage.firestore_client import FirestoreClient
from flask import jsonify, request
import requests
from helpers import build_url
from models.projects import Project

@api_v1.route('/projects', methods=['GET', 'POST'], strict_slashes=False)
def all_projects():
    if request.method == 'POST':
        from models.auth import Auth
        current_user = Auth.get_current_user()
        f = request.form
        name = f.get('name')
        if Project.get_by_attr('name', name):
            return jsonify({'status': 'error', 'project': ''}), 400
        data = {
            'name': f.get('name'),
            'call_to_action': f.get('call_to_action'),
            'feature_backlog': f.get('feature_backlog'),
            'minimal_version': f.get('minimal_version'),
            'stretch_goals': f.get('stretch_goals')
        }
        new_project = Project(**data)
        new_project.save()
        return jsonify({'status': 'OK', 'project': new_project.to_dict()}), 200
    projects = Project.get_by_class()
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


@api_v1.route('/projects/<id>', methods=['PUT'], strict_slashes=False)
def update_project_by_id(id):
    project = Project.get_by_id(id)
    if not project:
        return jsonify({
            'status': 'error',
            'message': 'project could not be updated'
            }), 400
    f = request.form
    project = Project(**project)
    interested = f.get('interested')
    not_interested = f.get('not-interested')
    if f.get('owner'):
        owner_name, owner_id = f.get('owner').split(':')
        project.owner_name = owner_name
        project.owner_id = owner_id
    if not interested in project.interested:
        project.interested.append(interested)
    if not_interested in project.interested:
        project.interested.remove(not_interested)
    project.save()
    return jsonify({
        'status': 'OK', 'project': project.to_dict()
        }), 200