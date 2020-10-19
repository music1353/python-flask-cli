from flask import Flask
import logging
from logging.handlers import TimedRotatingFileHandler

from config import LOG_DIR
from . import database, routers


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    # set logging
    formatter = logging.Formatter("[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s")
    handler = TimedRotatingFileHandler(
        LOG_DIR+"flask.log", when="D", interval=1, backupCount=15, encoding="UTF-8", delay=False, utc=True)
    app.logger.addHandler(handler)
    handler.setFormatter(formatter)

    # init app
    # database.init_app(app)
    routers.init_app(app)

    return app