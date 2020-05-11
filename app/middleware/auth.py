from flask import jsonify, session

def AuthSessionMiddle():
    if 'login' not in session:
        resp = {
            'result': '',
            'msg': 'Unauthorized'
        }
        return jsonify(resp), 401