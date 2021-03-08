from api import all_projects

from flask import Blueprint, render_template, request, url_for, g, redirect, make_response
import requests
from helpers import build_url, login_required, admin_required

landing = Blueprint("landing", __name__, url_prefix="")


@landing.route('/', methods=['GET'], strict_slashes=False)
def index():
    """ about us page """
    from models.auth import Auth
    current_user = Auth.get_current_user()
    data = {
        'current_user': current_user,
        'full_view': request.full_view
    }
    if request.current_user:
        return redirect(url_for('landing.dashboard'))
    return render_template('index.html', data=data)



@landing.route('/some', methods=['GET'], strict_slashes=False)
@admin_required
def some():
    from models.auth import Auth
    current_user = Auth.get_current_user()
    data = {
        'current_user': current_user,
        'full_view': request.full_view
    }
    return render_template('dashboard.html', data=data)




@landing.route('/login', methods=['GET'], strict_slashes=False)
def login_page():
    """ login page """
    from models.auth import Auth
    current_user = Auth.get_current_user()
    data = {
        'current_user': current_user,
        'full_view': request.full_view,
    }
    return render_template('login.html', data=data)

@landing.route('/login', methods=['POST'], strict_slashes=False)
def login_form_submit():
    """ login form """
    return start_session(request)


def start_session(r):
    response = requests.post(build_url('api/sessions'), data=r.form).json()
    print(r.form)
    print(response)
    if not response or response.get('status') == 'error':
        data = {
            'msg': response.get('message')
        }
        return render_template('login.html', data=data)
    user = response.get('user')
    print(user)
    data = display_user_with_projects(r, user)
    data['msg'] = response.get('message')
    data['current_user'] = data.get('user')
    res = make_response(render_template('profile.html', data=data))
    res.set_cookie('session', response.get('id'))
    return res



# post request to api/sessions
# using user id from that, get user from /users
# data dict with current_user = user
# make response for profile.html with data
# set cookie on response
# return response

@landing.route('/logout', methods=['GET'], strict_slashes=False)
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

@landing.route('/register', methods=['POST'], strict_slashes=False)
def register():
    """ about us page """
    # post request to api/users to create new one
    response = requests.post(build_url('api/users'), data=request.form).json()
    if response.get('status') == 'error':
        data = {
            'msg': response.get('message')
        }
        return render_template('login.html', data=data)
    print('user created')
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


@landing.route('/dash', methods=['GET'], strict_slashes=False)
@login_required
def dashboard():
    from models.auth import Auth
    current_user = Auth.get_current_user()
    data = {
        'current_user': current_user,
        'full_view': request.full_view
    }
    return render_template('dashboard.html', data=data)




@landing.route('/projects', methods=['GET'], strict_slashes=False)
def projects():
    """ projects page """
    from models.auth import Auth
    current_user = Auth.get_current_user()
    data = {
        'current_user': current_user,
        'full_view': request.full_view
    }
    r = requests.get(build_url('api/projects')).json()
    projects = r.get('projects')
    for project in projects:
        contributors = []
        for user_id in project.get("contributors"):
            r = requests.get(build_url(f"api/users/{str(user_id)}")).json()
            user_obj = ''
            if r.get('Status') == 'OK':
                user_obj = r.get('user')
                contributors.append(user_obj)
        project["contributors"] = contributors
        tech_list = []
        for tech_id in project.get("tech"):
            r = requests.get(build_url(f"api/tech/{str(tech_id)}")).json()
            tech_obj = ''
            if r.get('Status') == 'OK':
                tech_obj = r.get('tech')
                tech_list.append(tech_obj)
        project["tech"] = tech_list
    return render_template('projects.html', projects=projects, data=data)

@landing.route('/users', methods=['GET'], strict_slashes=False)
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

@landing.route('/users/<id>/delete', methods=['POST'], strict_slashes=False)
def delete_account(id):
    from models.auth import Auth
    current_user = Auth.get_current_user()
    data = {
        'current_user': current_user,
        'full_view': request.full_view,
        'msg': 'Account Deleted',
        'user': ''
    }
    return render_template('profile.html', data=data)

@landing.route('/users/<id>', methods=['GET', 'POST'], strict_slashes=False)
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




@landing.route('/projects/search', methods=['POST'], strict_slashes=False)
def search():
    ''' search projects '''
    from models.auth import Auth
    current_user = Auth.get_current_user()
    data = {
        'current_user': current_user,
        'full_view': request.full_view
    }
    query = str(request.form.get('searchBar')).lower()
    r = requests.get(build_url('api/projects')).json()
    projects = r.get('projects')
    matches = []
    for project in projects:
        if query == project.get('name').lower() or query in project.get('name').lower():
            matches.append(project)
            continue
        if project not in matches:
            for user in project.get('users'):
                if query == user.lower() or query in user.lower():
                    matches.append(project)
                    break
            if project not in matches:
                for tech in project.get('technologies'):
                    if query == tech.lower() or query in tech.lower():
                        matches.append(project)
                        break
    msg = None
    if len(matches) == 0:
        matches = projects
        msg = f'{query} not found'
    # pub_data, auth_data, my_auth_data, my_role_auth_data
    return render_template('projects.html', projects=matches, msg=msg, data=data)
