from api.v1 import api_v1
from models.storage.firestore_client import FirestoreClient
from flask import jsonify
import requests
from helpers import build_url
from models.users import User

@api_v1.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    users = User.get_by_class()
    if len(users) == 0:
        return jsonify({'Status': 'error', 'users': []}), 400
    return jsonify({'Status': 'OK', 'users': users}), 200

@api_v1.route('/users/<id>', methods=['GET'], strict_slashes=False)
def user_by_id(id):
    user = User.get_by_id(id)
    if not user:
        return jsonify({'Status': 'error'}), 400
    return jsonify({'Status': 'OK', 'user': user}), 200
