from api.v1 import api_v1
from models.storage.firestore_client import FirestoreClient
from flask import jsonify
import requests
from helpers import build_url

@api_v1.route('/members', methods=['GET'], strict_slashes=False)
def all_members():
    db = FirestoreClient()
    members = db.get_all_by_class('Member')
    if len(members) == 0:
        return jsonify({'Status': 'error', 'members': []}), 400
    return jsonify({'Status': 'OK', 'members': members}), 200

@api_v1.route('/members/<id>', methods=['GET'], strict_slashes=False)
def member_by_id(id):
    r = requests.get(build_url('api/members')).json()
    if r.get('status') == 'error':
        return jsonify({'Status': 'error', 'members': {}}), 400
    members = r.get('members')
    for item in members:
        if item.get("id") == id:
            return jsonify({'Status': 'OK', 'member': item}), 200
    return jsonify({'Status': 'error', 'members': {}}), 400
