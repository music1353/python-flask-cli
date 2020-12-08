from flask import Blueprint, request, session
from google.oauth2 import id_token
from google.auth.transport import requests

from app.models import Role
from app.models import Auth, User, LoginRecord
from app.middleware import permission_required
from app.pkg.resp_handler import resp_wrapper

GOOGLE_OAUTH2_CLIENT_ID = 'MY_GOOGLE_OAUTH2_CLIENT_ID'

v1_auth = Blueprint('auth', __name__)

@permission_required(role=[Role.ANONYMOUS])
@v1_auth.route('/hello', methods=['GET'])
def hello():
    return 'hello world'


@permission_required(role=[Role.ANONYMOUS])
@v1_auth.route('/check-identifier', methods=['GET'])
def v1_auth_check_identifier():
    identifier = request.args.get('identifier')

    exist, err = Auth.check_identifier(identifier)
    if err:
        return resp_wrapper('', 'Error: check identifier failed.'), 503
    if exist:
        return resp_wrapper('', 'Error: duplicated identifier.'), 400
    
    return resp_wrapper('', 'No duplicated.'), 200


@permission_required(role=[Role.ANONYMOUS])
@v1_auth.route('/check-nickname', methods=['GET'])
def v1_auth_check_nickname():
    nickname = request.args.get('nickname')

    exist, err = User.check_nickname(nickname)
    if err:
        return resp_wrapper('', 'Error: check nickname failed.'), 503
    if exist:
        return resp_wrapper('', 'Error: duplicated nickname.'), 400
    
    return resp_wrapper('', 'No duplicated.'), 200


@permission_required(role=[Role.ANONYMOUS])
@v1_auth.route('/signup', methods=['POST'])
def v1_auth_signup():
    ''' 一般信箱帳號註冊
        Method: POST
        Parameters:
            - identify_type {str}
            - identifier {str}
            - credential {str}
            - check_policy {bool}
            - nickname {str}
            - avatar {str}
    '''
    identify_type = request.json['identify_type']
    identifier = request.json['identifier']
    credential = request.json['credential']
    check_policy = request.json['check_policy']

    nickname = request.json['nickname']
    avatar = request.json['avatar']

    uid, err = Auth.insert_one(identify_type, identifier, credential, check_policy)
    if err:
        return resp_wrapper('', 'Error: insert auth failed'), 503

    err = User.insert_one(uid, nickname, avatar)
    if err:
        return resp_wrapper('', 'Error: insert auth failed.'), 503

    err = LoginRecord.init_one(uid)
    if err:
        return resp_wrapper('', 'Error: init login record failed.'), 503

    return resp_wrapper('', 'Successfully sign up.'), 200


@permission_required(role=[Role.ANONYMOUS])
@v1_auth.route('/google-signup', methods=['POST'])
def v1_auth_google_signup():
    ''' 使用google帳號註冊
        Method: POST
        Parameters:
            - id_token {str} Google's token
            - identify_type {str}
            - nickname {str}
            - avatar {str}
    '''
    token = request.json['id_token']
    identify_type = request.json['identify_type']
    nickname = request.json['nickname']
    avatar = request.json['avatar']
    check_policy = True

    try:
        id_info = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_OAUTH2_CLIENT_ID
        )
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return resp_wrapper('', 'google oauth sign up fail. Wrong issuer.'), 503   
    except ValueError:
        # Invalid token
        return resp_wrapper('', 'google oauth sign up fail. Invalid token.'), 503

    # ready user info
    identifier = id_info['email']
    credential = id_info['sub']
    avatar = id_info['picture']

    uid, err = Auth.insert_one(identify_type, identifier, credential, check_policy)
    if err:
        return resp_wrapper('', 'Error: insert auth failed'), 503

    err = User.insert_one(uid, nickname, avatar)
    if err:
        return resp_wrapper('', 'Error: insert auth failed.'), 503

    err = LoginRecord.init_one(uid)
    if err:
        return resp_wrapper('', 'Error: init login record failed.'), 503

    return resp_wrapper('', 'Successfully sign up.'), 200


@permission_required(role=[Role.ANONYMOUS])
@v1_auth.route('/login', methods=['POST'])
def v1_auth_login():
    identifier = request.json['identifier']
    credential = request.json['credential']

    # check auth
    auth_data, err = Auth.find_one(identifier, credential)
    if err:
        return resp_wrapper('', 'Error: find auth data failed.'), 503
    if auth_data is None:
        return resp_wrapper('', 'Error: the auth not exist.'), 401

    # find user information
    user_data, err = User.find_one(auth_data['uid'])
    if err:
        return resp_wrapper('', 'Error: find user data failed.'), 503

    # ready return data
    result_data = {
        'uid': auth_data['uid'],
        'role': auth_data['role'],
        'avatar': user_data['avatar'],
        'nickname': user_data['nickname']
    }

    # record login ip
    if 'HTTP_X_REAL_IP' not in request.environ.keys(): # 如果不是透過proxy
        login_ip = request.environ['REMOTE_ADDR']
    else:
        login_ip = request.environ['HTTP_X_REAL_IP'] # get real ip from proxy
    
    err = LoginRecord.update_one(auth_data['uid'], login_ip)
    if err:
        return resp_wrapper('', 'Error: insert login record failed.'), 503

    # set session
    session['login'] = True
    session['uid'] = auth_data['uid']
    session['role'] = auth_data['role']

    return resp_wrapper(result_data, 'Successfully login.'), 200


@v1_auth.route('/google-login', methods=['POST'])
def v1_auth_google_login_func():
    ''' 使用google帳號登入
        Method: POST
        Parameters:
            - id_token {str} Google's token
    '''
    token = request.json['id_token']

    try:
        id_info = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_OAUTH2_CLIENT_ID
        )
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return resp_wrapper('', 'google oauth sign up fail. Wrong issuer.'), 400   
    except ValueError:
        return resp_wrapper('', 'google oauth sign up fail. Invalid token.'), 400

    # check auth
    identifier = id_info['email']
    credential = id_info['sub']
    
    auth_data, err = Auth.find_one(identifier, credential)
    if err:
        return resp_wrapper('', 'Error: find auth data failed.'), 503
    if auth_data is None:
        return resp_wrapper('', 'Error: the auth not exist.'), 401

    # find user information
    user_data, err = User.find_one(auth_data['uid'])
    if err:
        return resp_wrapper('', 'Error: find user data failed.'), 503

    # ready return data
    result_data = {
        'uid': auth_data['uid'],
        'role': auth_data['role'],
        'avatar': user_data['avatar'],
        'nickname': user_data['nickname']
    }

    # record login ip
    if 'HTTP_X_REAL_IP' not in request.environ.keys(): # 如果不是透過proxy
        login_ip = request.environ['REMOTE_ADDR']
    else:
        login_ip = request.environ['HTTP_X_REAL_IP'] # get real ip from proxy
    
    err = LoginRecord.update_one(auth_data['uid'], login_ip)
    if err:
        return resp_wrapper('', 'Error: insert login record failed.'), 503

    # set session
    session['login'] = True
    session['uid'] = auth_data['uid']
    session['role'] = auth_data['role']

    return resp_wrapper(result_data, 'Successfully login.'), 200


@permission_required(role=[Role.USER])
@v1_auth.route('/logout', methods=['POST'])
def v1_auth_logout():
    if(session.get('login') != None):
        # delete session
        session.pop('login', None)
        session.pop('uid', None)
        session.pop('role', None)

        return resp_wrapper('', 'Successfully logout.'), 200
    else:
        return resp_wrapper('', 'Error: not exist the login record.'), 400