from flask import session
from app.models import Role
from app.pkg.resp_handler import resp_wrapper
from app.database import db


def AuthSessionMiddle():
    if 'login' not in session:
        return resp_wrapper('', "Error: unauthorized"), 401


def permission_required(role=[], permission=[]):
    '''權限認證裝飾器'''
    def decorator(f):
        def decorated_function(*args, **kwargs):
            try:
                if role:
                    if Role.ANONYMOUS in role:
                        pass
                    elif session['role'] not in role:
                        return resp_wrapper('', "Error: you don't have the authority."), 403

                if permission:
                    auth_collect = db['auth']
                    auth_doc = auth_collect.find_one({'id': session['id']}, {'_id': False})

                    if auth_doc['permission'] not in permission:
                        return resp_wrapper('', "Error: you don't have the authority."), 403
                
                return f(*args, **kwargs)
            except Exception as e:
                print(e)
                return resp_wrapper('', "Error: check permissions error."), 503
        return decorated_function
    return decorator