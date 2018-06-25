from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config

db=SQLAlchemy()
bootstrap=Bootstrap()
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # from .ctr import ctr as ctr_blueprint
    # app.register_blueprint(ctr_blueprint)
    from app.ctr import ctr
    app.register_blueprint(ctr)
    # app.register_blueprint(ctr,url_prefix='/ctr')

    db.init_app(app)
    bootstrap.init_app(app)

    return app