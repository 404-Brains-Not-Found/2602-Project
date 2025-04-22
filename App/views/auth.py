from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from App.controllers.user import create_user, get_all_users, get_user_by_username
from App.models.company import Company
from App.models.student import Student
from.index import index_views
from App.controllers import login

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.username}")

@auth_views.route('/login', methods=['GET'])
def show_login():
    showform = request.args.get('showform') == 'true'
    role = request.args.get('role')
    return render_template('login.html', title="Login", showform=showform, role=role)

@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.form
    role = data.get('role')
    username = data.get('username')
    password = data.get('password')
    user = get_user_by_username(username)
    if not user or not user.check_password(password) or user.role != role:
        flash('Invalid credentials or role')
        return redirect(request.referrer)
    token = login(username, password)
    response = redirect(url_for('index_views.index_page'))
    set_access_cookies(response, token)
    flash('Login successful')
    return response

@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(url_for('auth_views.show_login'))
    flash("Logged Out!")
    unset_jwt_cookies(response)
    return response

@auth_views.route('/signup', methods=['GET'])
def show_signup():
    return render_template('signup.html', title="Register")

@auth_views.route('/signup', methods=['POST'])
def signup_action():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    user = create_user(**data)
    if not user:
        flash('User already exists or invalid role')
        return redirect(request.referrer)
    return redirect(url_for('auth_views.show_login'))

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
    data = request.json
    token = login(data['username'], data['password'])
    if not token:
        return jsonify(message='bad username or password given'), 401
    response = jsonify(access_token=token)
    set_access_cookies(response, token)
    return response

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response