from api import all_projects

from flask import Blueprint, render_template, request, url_for
import requests
from helpers import build_url

landing = Blueprint("landing", __name__, url_prefix="")

@landing.route('/', methods=['GET'], strict_slashes=False)
def index():
    """ public landing page """
    r = requests.get(build_url('api/projects')).json()
    return render_template('index.html', projects=r)