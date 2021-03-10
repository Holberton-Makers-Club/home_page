from flask import abort, request

class Auth():
    @classmethod
    def authenticate(cls, url):
        """ parent method of Auth class, all others called from here """
        route = Auth.get_route(url)
        print(1)
        print(route)
        if not route:
            abort(400)
        # check if route is public, private, or neither
        is_public = Auth.public_route(route)
        is_private = Auth.private_route(route)
        # check if session cookie exists and is valid, if so set current user
        authenticated_user = Auth.current_user(request.cookies.get('session'))
        return Auth.set_view(is_public, is_private, authenticated_user)

    @classmethod
    def get_route(cls, url):
        """
        format the request url to isolate the route
        """
        print(url, 'url here')
        if not 'com' in url:
            if not 'club' in url:
                return url.split('8080')[-1]
            return url.split('club')[-1]
        return url.split('com')[-1]

    @classmethod
    def public_route(cls, route):
        """
        check if path is fully public such as the landing page
        """
        if route == '/' or route.startswith('/api') or route.startswith('/static') or route == '/users' or (route == '/login' and request.method == 'GET'):
            return True
        return False

    @classmethod
    def private_route(cls, route):
        """
        check if page requested has a private version
        """
        if route.startswith('/someprivateroutewehaventmadeyet'):
            return True
        return False

    @classmethod
    def current_user(cls, cookie):
        """
        check for a session cookie, if it matches an existing
        one, and if it's expired
        """
        from models.auth.session import Session
        from datetime import datetime
        if not cookie and not 'api' in request.url:
            return None
        this_session_dict = Session.get_by_id(cookie)
        if not this_session_dict:
            return None
        id, created_at = this_session_dict.get('id'), this_session_dict.get('created_at')
        if Session.expired(id, created_at):
            return None
        this_session_dict['created_at'] = datetime.utcnow()
        session = Session(**this_session_dict)
        return this_session_dict['user_id']

    @classmethod
    def set_view(cls, is_public, is_private, authenticated_user):
        """
        set whether or not to load the full/privileged version of a template
        """
        # not signed in, viewing public page - show public page with login/register links
        if is_public and not authenticated_user:
            if 'api' not in request.url:
                print(1)
            full_view = True
        # signed in, viewing public page - show public page without login/register links
        if is_public and authenticated_user:
            if 'api' not in request.url:
                print(2)
            full_view = False
        # not signed in, viewing private page - show only public version [can view stuff but not interact]
        if not authenticated_user and is_private:
            if 'api' not in request.url:
                print(3)
            full_view = False
        # signed in, viewing private page - show private page
        # CHECK PERMISSION IN THOSE ROUTES
        if authenticated_user and is_private:
            if 'api' not in request.url:
                print(4)
            full_view = True
        # not signed in, viewing pages neither public nor private [public version of page with private features, like profile]
        if not authenticated_user and not is_private and not is_public:
            full_view = False
            if 'api' not in request.url:
                print(5)
        # signed in, viewing pages neither public nor private [private version of page with private features, like your own profile page]
        if authenticated_user and not is_private and not is_public:
            full_view = True
            if 'api' not in request.url:
                print(6)
        return full_view, authenticated_user

    @classmethod
    def get_current_user(cls):
        """ make request to api for current user based on request.current_user """
        from models.users import User
        from flask import request
        import requests
        from helpers import build_url
        id = request.current_user if request.current_user else ''
        response = requests.get(build_url(f'api/users/{id}')).json()
        if response.get('user'):
            return response.get('user')
        return None