from api import all_projects

from flask import Blueprint, render_template, request, url_for
import requests
from helpers import build_url

landing = Blueprint("landing", __name__, url_prefix="")

@landing.route('/', methods=['GET'], strict_slashes=False)
def index():
    """ public landing page """
    r = requests.get(build_url('api/projects')).json()
    projects = r.get('projects')
    return render_template('index.html', projects=projects)


@landing.route('/search', methods=['POST'], strict_slashes=False)
def search():
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
    return render_template('index.html', projects=matches, msg=msg)