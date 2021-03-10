from flask import request, redirect, url_for
from functools import wraps


def build_url(endpoint):
    # in deployment
    # return 'http://127.0.0.1:8080/' + endpoint
    # in development
    return 'https://home-page-2-307010.uc.r.appspot.com/' + endpoint
    
    

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.current_user is None:
            return redirect(url_for('landing.login_page', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.current_user == 'Cgjye7K7itzPWxVRoyQG':
            return redirect(url_for('landing.login_page', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
