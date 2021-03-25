from flask import request, redirect, url_for
from functools import wraps


def build_url(endpoint):
    # in deployment
    # in development
    # return 'https://home-page-2-307010.uc.r.appspot.com/' + endpoint
    return 'http://127.0.0.1:8080/' + endpoint

def set_data_and_current_user():
    """
    check the current user and set it in data response
    """
    from models.auth import Auth
    current_user = Auth.get_current_user()
    data = {
        'current_user': current_user
    }
    return data, current_user

def fully_private_route(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.current_user is None:
            return redirect(url_for('auth.login_page', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.current_user == 'Z1O5fbypLnSEx8c4NJfH':
            return redirect(url_for('auth.login_page', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
