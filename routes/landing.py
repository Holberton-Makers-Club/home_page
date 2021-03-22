from api import all_projects
from flask import Blueprint, render_template, request, url_for, g, redirect, make_response
import requests
from helpers import build_url, fully_private_route, admin_required, set_data_and_current_user
from routes.users import display_user_with_projects

landing = Blueprint("landing", __name__, url_prefix="")


@landing.route('/', methods=['GET'], strict_slashes=False)
def index():
    """ about us page """
    data, current_user = set_data_and_current_user()
    if current_user:
        return redirect(url_for('dash.dashboard'))
    return render_template('index.html', data=data)


@landing.route('/docs', methods=['GET'], strict_slashes=False)
@fully_private_route
def docs():
    data, current_user = set_data_and_current_user()
    return render_template('documentation_form.html', data=data)
