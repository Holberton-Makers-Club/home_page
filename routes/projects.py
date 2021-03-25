from api import all_projects

from flask import Blueprint, render_template, request, url_for, g, redirect, make_response
import requests
from helpers import build_url, fully_private_route, admin_required, set_data_and_current_user
from routes.users import display_user_with_projects

project_routes = Blueprint("projects", __name__, url_prefix="/projects")



@project_routes.route('/submit_project', methods=['GET'], strict_slashes=False)
@fully_private_route
def submit_project_page():
    data, current_user = set_data_and_current_user()
    return render_template('submit_project.html', data=data)


@project_routes.route('/', methods=['POST'], strict_slashes=False)
def submit_project():
    data, current_user = set_data_and_current_user()
    r = requests.post(build_url("api/projects"), data=request.form).json()
    if r.get('status') == 'error':
        data['msg'] = 'Failed to create new project.'
        return render_template('submit_project.html', data=data)
    project_id = r.get('project').get('id')
    response = requests.put(build_url(f'api/projects/{project_id}'), data={'interested': current_user.get("id")}).json()
    return redirect(url_for('dash.dashboard'))

@project_routes.route('/edit', methods=['GET', 'POST'], strict_slashes=False)
def edit_project():
    data, current_user = set_data_and_current_user()
    data["api_url"] = build_url('api/')
    data["roles"] = ['role1', 'role2', 'role3', 'role4']
    r = requests.get(build_url('api/projects')).json()
    projects = r.get('projects')
    return render_template('edit_project.html', data=data, projects=projects)

@project_routes.route('/<id>', methods=['POST'], strict_slashes=False)
def modify_project(id):
    data, current_user = set_data_and_current_user()
    r = requests.put(build_url(f"api/projects/{id}"), data=request.form).json()
    print(r)
    if r.get('status') == 'error':
        data['error'] = f'PUT api/projects/{id} failed'
        print('ERROR')
        return render_template('error.html', data=data)
    return redirect(url_for('dash.dashboard'))

@project_routes.route('/', methods=['GET'], strict_slashes=False)
def projects():
    """ projects page """
    data, current_user = set_data_and_current_user()
    r = requests.get(build_url('api/projects')).json()
    projects = r.get('projects')
    for project in projects:
        contributors = []
        if project.get('contributors'):
            for user_id in project.get("contributors"):
                r = requests.get(build_url(f"api/users/{str(user_id)}")).json()
                user_obj = ''
                if r.get('Status') == 'OK':
                    user_obj = r.get('user')
                    contributors.append(user_obj)
            project["contributors"] = contributors
        tech_list = []
        if project.get('tech'):
            for tech_id in project.get("tech"):
                r = requests.get(build_url(f"api/tech/{str(tech_id)}")).json()
                tech_obj = ''
                if r.get('Status') == 'OK':
                    tech_obj = r.get('tech')
                    tech_list.append(tech_obj)
            project["tech"] = tech_list
    return render_template('gallery.html', projects=projects, data=data)



@project_routes.route('/search', methods=['POST'], strict_slashes=False)
def search():
    ''' search projects '''
    data, current_user = set_data_and_current_user()
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
    return render_template('gallery.html', projects=matches, msg=msg, data=data)

@project_routes.route('/assign_roles', methods=['GET', 'POST'], strict_slashes=False)
def assign_roles():
    data, current_user = set_data_and_current_user()
    data["api_url"] = build_url('api/')
    data["roles"] = ['Role1', 'Role2', 'Role3', 'Role4']
    r = requests.get(build_url('api/projects')).json()
    projects, active = r.get("projects"), None
    r = requests.get(build_url('api/users')).json()
    data["users"] = r.get('users')    
    for project in projects:
        if project["active"]:
            active = project
            break

    if "127.0.0.1" in data["api_url"]:
        active = projects[0]

    return render_template('assign_roles.html', data=data, project=active)
