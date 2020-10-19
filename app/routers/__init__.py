from .v1 import v1_auth, v1_user
# from app.middleware import AuthSessionMiddle

def list_routes(app):
    routes = []
    
    for rule in app.url_map.iter_rules():
        method = str()
        endpoint = rule.endpoint
        
        METHODS = ['GET', 'POST', 'PUT', 'DELETE']

        method_list = list()
        for m in METHODS:
            if m in list(rule.methods):
                method_list.append(m)
        
        if endpoint != 'static':
            method = ','.join(method_list)
            fmt = '{}  {}  --> {}'.format(method, rule, endpoint)
            routes.append(fmt)

    for r in routes:
        print(r)


def init_app(app):
    app.register_blueprint(v1_auth, url_prefix='/api/v1/auth')
    app.register_blueprint(v1_user, url_prefix='/api/v1/user')

    # app.before_request_funcs = {
    #     # blueprint name: [list_of_functions]
    #     'user': [AuthSessionMiddle]
    # }
    
    list_routes(app)
        
