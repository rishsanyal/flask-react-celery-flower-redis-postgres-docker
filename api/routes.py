# import celery.states as states
# from flask import Flask, Response, request
from flask import url_for
from flask_cors import CORS
from worker import celery
# from flask_sqlalchemy import SQLAlchemy

# from flask_bcrypt import bcrypt,generate_password_hash, check_password_hash

from flask_login import (
    logout_user,
    login_required,
    login_user
)


from flask import (
    render_template,
    redirect,
    flash,
    session
)

from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)


from auth.auth_models import User
from forms import login_form, register_form

from werkzeug.routing import BuildError

from app import create_app, login_manager, sql_db

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app = create_app()

## CELERY API JOBS
@app.route('/add/<int:param1>/<int:param2>')
def add(param1: int, param2: int) -> str:
    task = celery.send_task('tasks.add', args=[param1, param2], kwargs={})
    return "Ok"

@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)

@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    return render_template("index.html",title="Home")

#### AUTH ROUTES

@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if user.password == form.pwd.data:
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template("auth.html",
        form=form,
        text="Login",
        title="Login",
        btn_action="Login"
        )



# Register route
@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()
    if form.validate_on_submit():
        try:
            # email = form.email.data
            pwd = form.pwd.data
            username = form.username.data

            newuser = User(
                username=username,
                # email=email,
                password=pwd,
            )

            sql_db.session.add(newuser)
            sql_db.session.commit()
            flash(f"Account Succesfully created", "success")

            return redirect(url_for("login"))

        except InvalidRequestError:
            sql_db.session.rollback()
            flash(f"Something went wrong!", "danger")
        except IntegrityError:
            sql_db.session.rollback()
            flash(f"User already exists!.", "warning")
        except DataError:
            sql_db.session.rollback()
            flash(f"Invalid Entry", "warning")
        except InterfaceError:
            sql_db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except DatabaseError:
            sql_db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except BuildError:
            sql_db.session.rollback()
            flash(f"An error occured !", "danger")
    return render_template("auth.html",
        form=form,
        text="Create account",
        title="Register",
        btn_action="Register account"
        )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
