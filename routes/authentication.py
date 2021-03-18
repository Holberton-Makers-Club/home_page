from api import all_projects

from flask import Blueprint, render_template, request, url_for, g, redirect, make_response
import requests
from helpers import build_url, fully_private_route, admin_required
from routes.users import display_user_with_projects

auth_routes = Blueprint("auth", __name__, url_prefix="/auth")



@auth_routes.route('/login', methods=['GET'], strict_slashes=False)
def login_page():
    """ login page """
    from models.auth import Auth
    current_user = Auth.get_current_user()
    data = {
        'current_user': current_user,
        'full_view': request.full_view,
    }
    return render_template('login.html', data=data)

@auth_routes.route('/login', methods=['POST'], strict_slashes=False)
def login_form_submit():
    """ login form """
    return start_session(request)


def start_session(r):
    response = requests.post(build_url('api/sessions'), data=r.form).json()
    if not response or response.get('status') == 'error':
        data = {
            'msg': response.get('message')
        }
        return render_template('login.html', data=data)
    user = response.get('user')
    data = display_user_with_projects(r, user)
    data['msg'] = response.get('message')
    data['current_user'] = data.get('user')
    res = make_response(render_template('profile.html', data=data))
    res.set_cookie('session', response.get('id'))
    return res



@auth_routes.route('/logout', methods=['GET'], strict_slashes=False)
def logout():
    """ logout route redirects to login page """
    from models.auth.session import Session
    from models.auth import Auth
    current_user = Auth.get_current_user()
    data = {
        'current_user': current_user,
        'full_view': request.full_view,
    }
    cookie = request.cookies.get('session')
    if not cookie:
        return render_template('login.html', data=data)
    matching_session = Session.get_by_id(cookie)
    if not matching_session:
        return render_template('login.html', data=data)
    Session.delete_by_id(cookie)
    del Session.sessions[cookie]
    # delete request to api/sessions/<request.cookies>
    # data dict with current_user = user
    # make response with data
    # return response
    return render_template('login.html', data=data)

@auth_routes.route('/register', methods=['POST'], strict_slashes=False)
def register():
    """ about us page """
    # post request to api/users to create new one
    response = requests.post(build_url('api/users'), data=request.form).json()
    if response.get('status') == 'error':
        data = {
            'msg': response.get('message')
        }
        return render_template('login.html', data=data)
    return start_session(request)
    # post to api/sessions
    # using user id from that, get user from /users
    # data dict with current_user = user
    # make response for profile.html with data
    # set cookie on response
    # return response
    from models.auth import Auth
    current_user = Auth.get_current_user()
    data = {
        'current_user': current_user,
        'full_view': request.full_view
    }
    return render_template('login.html', data=data)