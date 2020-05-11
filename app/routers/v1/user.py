from flask import Blueprint, current_app
from app.models import User
from app.pkg.resp_handler import resp_wrapper

v1_user = Blueprint('user', __name__)

@v1_user.route('/getInfo', methods=['GET'])
def v1_user_get_info():
    res = User.get_all_users()

    current_app.logger.info("Successfully get uesrs info")

    return resp_wrapper(res, 'Successfully get uesrs info'), 200