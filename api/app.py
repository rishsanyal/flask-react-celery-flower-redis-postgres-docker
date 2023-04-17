import celery.states as states
from flask import Flask, Response, request
from flask import url_for, jsonify
from flask_cors import CORS
from worker import celery
from flask_sqlalchemy import SQLAlchemy

## Login libraries
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
# from redis_worker import redis_db
# from mock import mock_class_info, mock_office_hours_info
# from redis_crud import delete_students_queue

from flask_login import (
    LoginManager
)


sql_db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

migrate = Migrate()

def create_app():
    """Create the app.

    Returns:
        _type_: _description_
    """
    app = Flask(__name__)

    app.secret_key = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:root@db:5432/mydb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app)

    login_manager.init_app(app)
    sql_db.init_app(app)
    migrate.init_app(app, sql_db)

    bcrypt = Bcrypt(app)
    bcrypt.init_app(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
