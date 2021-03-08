from api.v1 import api_v1
from flask import jsonify
from models.users import User
from flask import request
from models.auth.session import Session

@api_v1.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    print(request.cookies)
    user_session = request.cookies.get('session')
    print(user_session, 'request cookie')
    matching_session = Session.get_by_id(user_session)
    print('session get by id', matching_session)
    response = {
        'status': 'error',
        'message': 'logout failed'
    }
    if not matching_session:
        return jsonify(response), 400
    session = Session(**matching_session)
    session.delete()
    del Session.sessions[user_session]
    response['message'] = 'logout successful'
    return jsonify(response), 200