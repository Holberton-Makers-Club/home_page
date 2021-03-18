from api import all_projects

from flask import Blueprint, render_template, request, url_for, g, redirect, make_response
import requests
from helpers import build_url, fully_private_route, admin_required

user_routes = Blueprint("users", __name__, url_prefix="/users")


@user_routes.route('/', methods=['GET'], strict_slashes=False)
def users():
    """ users page """
    from models.auth import Auth
    current_user = Auth.get_current_user()
    data = {
        'current_user': current_user,
        'full_view': request.full_view
    }
    r = requests.get(build_url('api/users')).json()
    users = r.get('users')   
    if users:
        for user in users:
            tech_list = []
            if user.get('tech'):
                for tech_id in user.get("tech"):
                    r = requests.get(build_url(f"api/tech/{str(tech_id)}")).json()
                    tech_obj = ''
                    if r.get('Status') == 'OK':
                        tech_obj = r.get('tech')
                        tech_list.append(tech_obj)
                user["tech"] = tech_list
    return render_template('users.html', users=users if users else '', data=data)

@user_routes.route('/<id>/delete', methods=['POST'], strict_slashes=False)
def delete_account(id):
    response = requests.delete(build_url(f'api/users/{id}')).json()
    data = {
        'msg': response.get('message')
    }
    res = make_response(render_template('login.html', data=data))
    res.set_cookie('session', '')
    return res

@user_routes.route('/<id>', methods=['GET', 'POST'], strict_slashes=False)
def user_profile(id):
    """ profile page """
    from models.auth import Auth
    if not id == request.current_user:
        r = requests.get(build_url(f"api/users/{str(id)}")).json()
        user = r.get('user')
    else:
        user = Auth.get_current_user()
    data = display_user_with_projects(request, user)
    if request.method == 'GET':
        if request.current_user:
            r = requests.get(build_url('/api/quotes')).json()
            import random
            data['quote'] = random.choice(r.get('quotes'))        
        return render_template('profile.html', data=data)
    # UPDATE users profile
    if request.method == 'POST':
        response = requests.put(build_url(f'api/users/{id}'), data=request.form).json()
        if response.get('status') == 'error':
            data['msg'] = response.get('message')
            return render_template('profile.html', data=data)
        # do the update here
        return redirect(url_for('landing.user_profile', id=id))

def display_user_with_projects(request, user):
    from models.auth import Auth
    current_user = Auth.get_current_user()
    
    full_view = request.full_view
    tech_list = []
    if user and user.get('tech'):
        for tech_id in user.get("tech"):
            r = requests.get(build_url(f"api/tech/{str(tech_id)}")).json()
            tech_obj = ''
            if r.get('Status') == 'OK':
                tech_obj = r.get('tech')
                tech_list.append(tech_obj)
        user["tech"] = tech_list
    proj_list = []
    if user.get('projects'):
        for proj_id in user.get("projects"):
            r = requests.get(build_url(f"api/projects/{str(proj_id)}")).json()
            proj_obj = ''
            if r.get('Status') == 'OK':
                proj_obj = r.get('project')
                proj_list.append(proj_obj)
        user["projects"] = proj_list
    if current_user and current_user.get('id') == user.get('id'):
        current_user = user
    else:
        current_user = None
    data = {
        'user': user,
        'current_user': current_user,
        'full_view': full_view
    }
    return data


