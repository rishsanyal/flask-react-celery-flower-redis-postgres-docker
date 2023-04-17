# from flask import request

# from auth.auth_models import User, UserProfile, sql_db

# def signup():
#     """Create a new user"""

#     email = request.form['email']
#     password = request.form['password']
#     full_name = request.form['full_name']
#     email = request.form['email']
#     phone = request.form['phone']


#     user = User(email=email, password=password)
#     profile = UserProfile()(full_name=full_name, email=email, phone=phone)
#     user.profile = profile

#     sql_db.session.add(user)
#     sql_db.session.commit()

#     return 'User created successfully'