from api import all_projects

from flask import Blueprint, render_template, request, url_for
import requests
from helpers import build_url

landing = Blueprint("landing", __name__, url_prefix="")

@landing.route('/', methods=['GET'], strict_slashes=False)
def index():
    """ about us page """
    return render_template('index.html')

@landing.route('/projects', methods=['GET'], strict_slashes=False)
def projects():
    """ projects page """
    r = requests.get(build_url('api/projects')).json()
    projects = r.get('projects')
    for project in projects:
        contributors = []
        for member_id in project.contributors:
            member = request.get(build_url('api/members/' + member_id)).json()
            contributors.append(member)
        projects.contributors = contributors
    return render_template('projects.html', projects=projects)

@landing.route('/members', methods=['GET'], strict_slashes=False)
def members():
    """ projects page """
    r = requests.get(build_url('api/members')).json()
    members = r.get('members')
    return render_template('members.html', members=members)

@landing.route('/members/<id>', methods=['GET'], strict_slashes=False)
def member_profile(id):
    """ projects page """
    r = requests.get(build_url('api/members')).json()
    members = r.get('members')
    foundmember = None    
    for member in members:
        if id == member.get('id'):
            foundmember = member
    return render_template('profile.html', member=foundmember)

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