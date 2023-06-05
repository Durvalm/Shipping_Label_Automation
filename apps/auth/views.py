from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from apps.models import db, SuperUser
from apps.utils.alert import flash_message

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")
    
    email = request.form.get("email")
    password = request.form.get("password")

    superuser = SuperUser.query.filter_by(email=email).first()
    if not superuser or not check_password_hash(superuser.password, password):
        flash_message('Please check your login details and try again.', "warning")
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
    login_user(superuser)

    return redirect(url_for("dashboard.dashboard"))

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# @auth_bp.route('/create-superuser', methods=['POST', "GET"])
# def create_superuser():
#     """Endpoint should not be exposed, created superuser"""
#     if request.method == "GET":
#         return render_template("auth/signup.html")
#     # code to validate and add user to database goes here
#     email = request.form.get('email')
#     password1 = request.form.get('password1')
#     password2 = request.form.get('password2')

#     if password1 == password2:
#         # create a new user with the form data. Hash the password so the plaintext version isn't saved.
#         superuser = SuperUser(email=email, password=generate_password_hash(password1, method='sha256'))
#         # add the new user to the database
#         db.session.add(superuser)
#         db.session.commit()

#     return redirect(url_for('auth.login'))
