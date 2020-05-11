from flask import jsonify

def resp_wrapper(res, msg):
    resp = {
        'result': res,
        'msg': msg
    }
    return jsonify(resp)