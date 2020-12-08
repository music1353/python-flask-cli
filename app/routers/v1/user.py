from flask import Blueprint, current_app
from app.models import User
from app.pkg.resp_handler import resp_wrapper

v1_user = Blueprint('user', __name__)

pass