from api.v1 import api_v1
from models.storage.firestore_client import FirestoreClient
from flask import jsonify, request
import requests
from models.users import User

@api_v1.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    print('in here')
    users = User.get_by_class()
    if len(users) == 0:
        return jsonify({'status': 'error', 'users': []}), 400
    return jsonify({'status': 'OK', 'users': users}), 200

@api_v1.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    f = request.form
    email = f.get('email')
    if User.get_by_attr('email', email):
        return jsonify({'status': 'error', 'user': ''}), 400
    data = {
        'firstname': f.get('firstname'),
        'lastname': f.get('lastname'),
        'email': email,
        'password': f.get('password')
    }
    print(data)
    new_user = User(**data)
    new_user.save()
    return jsonify({'status': 'OK', 'user': new_user.to_dict()}), 200

@api_v1.route('/users/<id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(id):
    user = User.get_by_id(id)
    if not user:
        return jsonify({'status': 'error'}), 400
    return jsonify({'status': 'OK', 'user': user}), 200

@api_v1.route('/users/<id>', methods=['PUT'], strict_slashes=False)
def update_user_by_id(id):
    user = User.get_by_id(id)
    if not user:
        return jsonify({
            'status': 'error',
            'message': 'user could not be updated'
            }), 400
    f = request.form
    user = User(**user)
    if f.get('firstname'):
        user.firstname = f.get('firstname')
    if f.get('lastname'):
        user.lastname = f.get('lastname')
    if f.get('title'):
        user.title = f.get('title')
    if f.get('bio'):
        user.bio = f.get('bio')
    if f.get('github'):
        user.github = f.get('github')
    if f.get('linkedin'):
        user.linkedin = f.get('linkedin')
    email = f.get('email')
    password = f.get('password')
    if email:
        user.email = email
    if password:
        user.password = password
    user.save()
    return jsonify({
        'status': 'OK', 'user': user.to_dict()
        }), 200