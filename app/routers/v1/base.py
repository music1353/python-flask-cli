from flask import Blueprint, request, session, current_app
from .. import resp_wrapper

v1_base = Blueprint('base', __name__)

@v1_base.route('/hello', methods=['GET'])
def hello():
    return 'hello world'

@v1_base.route('/login', methods=['POST'])
def v1_base_login():
    account = request.json['account']
    password = request.json['password']

    session['login'] = True
    session['account'] = account

    return resp_wrapper('', 'Sunccessfully login'), 200

