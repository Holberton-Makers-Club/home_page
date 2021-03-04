from api.v1 import api_v1
from models.storage.firestore_client import FirestoreClient
from flask import jsonify
import requests
from helpers import build_url


@api_v1.route('/tech', methods=['GET'], strict_slashes=False)
def all_tech():
    db = FirestoreClient()
    techs = db.get_by_class('Tech')
    if len(techs) == 0:
        return jsonify({'Status': 'error', 'tech': []}), 400
    return jsonify({'Status': 'OK', 'tech': techs}), 200

@api_v1.route('/tech/<id>', methods=['GET'], strict_slashes=False)
def tech_by_id(id):
    r = requests.get(build_url('api/tech')).json()
    if r.get('status') == 'error':
        return jsonify({'Status': 'error', 'tech': {}}), 400
    techs = r.get('tech')
    for item in techs:
        if item.get("id") == id:
            return jsonify({'Status': 'OK', 'tech': item}), 200
    return jsonify({'Status': 'error', 'tech': {}}), 400
