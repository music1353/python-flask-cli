from flask import Blueprint, request, session
from app.models import Auth, User
from app.pkg.resp_handler import resp_wrapper

v1_auth = Blueprint('auth', __name__)

@v1_auth.route('/hello', methods=['GET'])
def hello():
    return 'hello world'

@v1_auth.route('/signup', methods=['POST'])
def v1_auth_signup():
    identify_type = request.json['identify_type']
    identifier = request.json['identifier']
    credential = request.json['credential']
    name = request.json['name']
    phone = request.json['phone']

    res = Auth.check_auth(identifier, credential)
    if res['is_exist'] == True:
        return resp_wrapper('', 'the account is exist'), 404
    
    uid, err = Auth.insert_one(identify_type, identifier, credential)
    if err:
        return resp_wrapper('', 'insert auth fail'), 404

    err = User.insert_one(uid, name, phone)
    if err:
        return resp_wrapper('', 'insert auth fail'), 404

    return resp_wrapper('', 'Successfully sign up'), 200


@v1_auth.route('/login', methods=['POST'])
def v1_auth_login():
    account = request.json['account']
    password = request.json['password']

    session['login'] = True
    session['account'] = account

    return resp_wrapper('', 'Successfully login'), 200

