def build_url(endpoint):
    # in deployment
    # return 'home-page-304402.uc.r.appspot.com/' + endpoint
    # in development
    return 'http://127.0.0.1:8080/' + endpoint