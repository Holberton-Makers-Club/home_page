from api import all_projects

from flask import Blueprint, render_template, request, url_for, g, redirect
import requests
from helpers import build_url

landing = Blueprint("landing", __name__, url_prefix="")

@landing.route('/', methods=['GET'], strict_slashes=False)
def index():
    """ about us page """
    return render_template('index.html')








@landing.route('/login', methods=['GET'], strict_slashes=False)
def login_page():
    """ login page """
    return render_template('login.html')

@landing.route('/login', methods=['POST'], strict_slashes=False)
def login_form_submit():
    """ login form """
    # post request to api/sessions
    # using user id from that, get user from /users
    # data dict with current_user = user
    # make response for profile.html with data
    # set cookie on response
    # return response
    return render_template('login.html')

@landing.route('/logout', methods=['GET'], strict_slashes=False)
def logout():
    """ logout route redirects to login page """
    # delete request to api/sessions/<request.cookies>
    # data dict with current_user = user
    # make response with data
    # return response
    return render_template('login.html')

@landing.route('/register', methods=['POST'], strict_slashes=False)
def register():
    """ about us page """
    # post request to api/users to create new one
    # check if worked
    # post to api/sessions
    # using user id from that, get user from /users
    # data dict with current_user = user
    # make response for profile.html with data
    # set cookie on response
    # return response

    return render_template('login.html')







@landing.route('/projects', methods=['GET'], strict_slashes=False)
def projects():
    """ projects page """
    r = requests.get(build_url('api/projects')).json()
    projects = r.get('projects')
    for project in projects:
        contributors = []
        for member_id in project.get("contributors"):
            r = requests.get(build_url(f"api/members/{str(member_id)}")).json()
            member_obj = ''
            if r.get('Status') == 'OK':
                member_obj = r.get('member')
                contributors.append(member_obj)
        project["contributors"] = contributors
        tech_list = []
        for tech_id in project.get("tech"):
            r = requests.get(build_url(f"api/tech/{str(tech_id)}")).json()
            tech_obj = ''
            if r.get('Status') == 'OK':
                tech_obj = r.get('tech')
                tech_list.append(tech_obj)
        project["tech"] = tech_list
    return render_template('projects.html', projects=projects)

@landing.route('/members', methods=['GET'], strict_slashes=False)
def members():
    """ members page """
    r = requests.get(build_url('api/members')).json()
    members = r.get('members')   
    for member in members:
        tech_list = []
        for tech_id in member.get("tech"):
            r = requests.get(build_url(f"api/tech/{str(tech_id)}")).json()
            tech_obj = ''
            if r.get('Status') == 'OK':
                tech_obj = r.get('tech')
                tech_list.append(tech_obj)
        member["tech"] = tech_list
    return render_template('members.html', members=members)

@landing.route('/members/<id>/delete', methods=['POST'], strict_slashes=False)
def delete_account(id):
    print('delete account')
    return render_template('profile.html', data={'member': None, 'msg': 'Account Deleted'})

@landing.route('/members/<id>', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
def member_profile(id):
    """ profile page """
    if request.method == 'DELETE':
        print('in delete')
        return render_template('profile', member=None)
    if request.method == 'GET':
        r = requests.get(build_url(f"api/members/{str(id)}")).json()
        member = r.get('member')
        tech_list = []
        for tech_id in member.get("tech"):
            r = requests.get(build_url(f"api/tech/{str(tech_id)}")).json()
            tech_obj = ''
            if r.get('Status') == 'OK':
                tech_obj = r.get('tech')
                tech_list.append(tech_obj)
        member["tech"] = tech_list
        proj_list = []
        for proj_id in member.get("projects"):
            r = requests.get(build_url(f"api/projects/{str(proj_id)}")).json()
            proj_obj = ''
            if r.get('Status') == 'OK':
                print('here')
                proj_obj = r.get('project')
                proj_list.append(proj_obj)
        member["projects"] = proj_list
        return render_template('profile.html', member=member)
    if request.method == 'POST':
        f = request.form
        email, password = f.get('email'), f.get('password')
        first, last = f.get('firstname'), f.get('lastname')
        title, bio = f.get('title'), f.get('bio')
        github, linkedin = f.get('github'), f.get('linkedin')
        return redirect(url_for('landing.index'))




@landing.route('/projects/search', methods=['POST'], strict_slashes=False)
def search():
    ''' search projects '''
    query = str(request.form.get('searchBar')).lower()
    r = requests.get(build_url('api/projects')).json()
    projects = r.get('projects')
    matches = []
    for project in projects:
        if query == project.get('name').lower() or query in project.get('name').lower():
            matches.append(project)
            continue
        if project not in matches:
            for member in project.get('members'):
                if query == member.lower() or query in member.lower():
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
    return render_template('projects.html', projects=matches, msg=msg)