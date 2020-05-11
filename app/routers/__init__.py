from flask import jsonify
def resp_wrapper(res, msg):
    resp = {
        'result': res,
        'msg': msg
    }
    return jsonify(resp)



from .v1 import v1_base, v1_user
from app.middleware import AuthSessionMiddle

def before_my_blueprint():
    print(111)

def init_app(app):
    app.register_blueprint(v1_base, url_prefix='/api/v1')
    app.register_blueprint(v1_user, url_prefix='/api/v1/user')

    app.before_request_funcs = {
        # blueprint name: [list_of_functions]
        'user': [AuthSessionMiddle]
    }
        
