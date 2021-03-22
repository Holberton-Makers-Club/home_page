from api import all_projects

from flask import Blueprint, render_template, request, url_for, g, redirect, make_response
import requests
from helpers import build_url, fully_private_route, admin_required, set_data_and_current_user
from routes.users import display_user_with_projects
from models.projects import Project

dashboard_routes = Blueprint("dash", __name__, url_prefix="/dash")


def trigger_current_project(data):
    """ if wednesday, count up interest in each project and trigger the one with the most """
    from datetime import datetime
    if not datetime.today().strftime('%A') == 'Wednesday':
        data['load_buttons'] = True
        return data
    data['load_buttons'] = False
    projects = data['projects']
    most_participants = 0
    current_project = None
    for project_dict in projects:
        project = Project(**project_dict)
        # make sure there's only one current project by resetting them all to inactive
        project.active = False
        
        project.save()
        data, project_dict = fill_and_count_participants(data, project_dict)
        if project_dict.get('participant_count') > most_participants:
            if hasattr(project, 'contributors'):
                project.contributors = []            
            most_participants = project_dict.get('participant_count')
            project.contributors = project_dict['participants']
            project.active = True
            project.save()    
            data['current_project'] = project_dict                

    return data

def fill_and_count_participants(data, project_dict):
    count = 0
    for user_id in project_dict.get('interested'):
        project_dict['participants'] = []
        if user_id:
            r = requests.get(build_url(f'api/users/{user_id}')).json()
            if not r.get('status') == 'OK':
                    data['msg'] = 'api/users/<id> encountered an error'
            else:
                if 'user' in r and 'password' in r['user']:
                    del r['user']['password']                
                project_dict['participants'].append(r.get('user'))
                count += 1
    project_dict['participant_count'] = count
    return data, project_dict
                
    


@dashboard_routes.route('/', methods=['GET'], strict_slashes=False)
@fully_private_route
def dashboard():
    from datetime import datetime
    data, current_user = set_data_and_current_user()
    projects = requests.get(build_url('api/projects')).json().get('projects')
    data['projects'] = projects
    data = trigger_current_project(data)
    if data.get('load_buttons'):
        projects_list = []
        for project_dict in projects:
            print(project_dict.get('participant_count'), '*****')
            data, project_dict = fill_and_count_participants(data, project_dict)
            projects_list.append(project_dict)
            if project_dict.get('active'):
                if not project_dict.get('contributors'):
                    project_dict['contributors'] = project_dict['participants']
                data['current_project'] = project_dict
        data['projects'] = projects_list
            
    if current_user.get('staff'):
        r = requests.get(build_url(f"api/users")).json()
        if not r.get('status') == 'OK':
            data['msg'] = 'api/users encountered an error'
        data['users'] = r.get('users')
    return render_template('dashboard.html', data=data)



@dashboard_routes.route('/express-interest/<project_id>', methods=['POST'], strict_slashes=False)
@fully_private_route
def express_interest(project_id):
    data, current_user = set_data_and_current_user()    
    response = requests.put(build_url(f'api/projects/{project_id}'), data={'interested': current_user.get("id")}).json()
    if not response.get('status') == 'OK':
        r = requests.get(build_url('api/projects')).json()
        projects = r.get('projects')
        data['msg'] = 'request failed'
        return render_template('dashboard.html', data=data, projects=projects)
    return redirect(url_for('dash.dashboard'))
    
    
@dashboard_routes.route('/revoke-interest/<project_id>', methods=['POST'], strict_slashes=False)
@fully_private_route
def revoke_interest(project_id):
    data, current_user = set_data_and_current_user()
    response = requests.put(build_url(f'api/projects/{project_id}'), data={'not-interested': current_user.get("id")}).json()
    print(response)
    if not response.get('status') == 'OK':
        r = requests.get(build_url('api/projects')).json()
        projects = r.get('projects')
        data['msg'] = 'request failed'
        return render_template('dashboard.html', data=data, projects=projects)
    return redirect(url_for('dash.dashboard'))

