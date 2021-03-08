from api.v1 import api_v1
from flask import jsonify
from models.users import User
from flask import request
from models.auth.session import Session

@api_v1.route('/sessions', methods=['POST', 'PUT'], strict_slashes=False)
def login_or_authenticate():
    if request.method == 'POST':
        f = request.form
        email, password = f.get('email'), f.get('password')

        response = {
            'status': 'error',
            'message': 'incomplete form'
            }

        # verify user completed the form
        if not email or not password:
            return jsonify(response), 400
        
        # verify user exists with that email
        user_dict_list = User.get_by_attr('email', email)
        if not user_dict_list or len(user_dict_list) == 0:
            response['message'] = 'email not found'
            return jsonify(response), 400
        user_dict = user_dict_list[0].to_dict()

        # verify password is correct
        user = User(**user_dict)
        if not user.validate_password(password):
            response['message'] = 'incorrect password'
            return jsonify(response), 400
        del user_dict['password']
        
        # create a session
        session = Session(**{
            'user_id': user.id
            })
        sess_id = session.id
        del session 

        return jsonify({
            'status': 'OK',
            'message': 'login successful',
            'user': user_dict,
            'id': sess_id
            }), 200
    if request.method == 'PUT':
        from datetime import datetime
        import requests
        from helpers import build_url
        # get session id passed in a cookie
        cookie = request.cookies.get('session')
        session_dict = Session.sessions.get(cookie)
        if session_dict:
            created_at = Session.sessions[cookie].get('created_at')
        # check if it matches existing session, and ensure not expired
        if not session_dict or Session.expired(cookie, created_at):
            if session_dict:
                session_obj = Session(**session_dict)
                session_obj.delete()
                del Session.sessions[cookie]
            # return error message if invalid or expired
            return jsonify({
                'status': 'error',
                'message': 'session invalid or expired'
                }), 404
        else:
            # update timestamp of session
            session_dict['created_at'] = datetime.utcnow()
            session_obj = Session(**session_dict)
            response = requests.get(build_url(f'/api/users/{session_obj.user_id}')).json()
            user = response.get('user')
            session_obj.delete()
            return jsonify({
                'status': 'OK',
                'message': 'session updated',
                'user': user
                }), 200
