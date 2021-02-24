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
        for member_id in project.get("contributors"):
            r = requests.get(build_url(f"api/members/{str(member_id)}")).json()
            member = r.get('member')
            tech_list = []
            for tech_id in member.get("tech"):
                r = requests.get(build_url(f"api/tech/{str(tech_id)}")).json()
                tech_obj = r.get('tech')
                tech_list.append(tech_obj)
            member["tech"] = tech_obj
            contributors.append(member)
        project["contributors"] = contributors
    return render_template('projects.html', projects=projects)

@landing.route('/members', methods=['GET'], strict_slashes=False)
def members():
    """ projects page """
    r = requests.get(build_url('api/members')).json()
    members = r.get('members')   
    for member in members:
        tech_list = []
        for tech_id in member.get("tech"):
            r = requests.get(build_url(f"api/tech/{str(tech_id)}")).json()
            tech_obj = r.get('tech')
            tech_list.append(tech_obj)
        member["tech"] = tech_obj
    return render_template('members.html', members=members)

@landing.route('/members/<id>', methods=['GET'], strict_slashes=False)
def member_profile(id):
    """ projects page """
    r = requests.get(build_url(f"api/members/{str(id)}")).json()
    member = r.get('member')
    return render_template('profile.html', member=member)

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