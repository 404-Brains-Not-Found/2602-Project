from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for
from App.controllers import create_user, initialize, get_all_internships
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies, get_jwt_identity
from App.controllers.user import get_all_users, get_user
from App.models import User

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index():
    return render_template('login.html')

@index_views.route('/home', methods=['GET'])
@jwt_required()
def index_page():
    user_id = int(get_jwt_identity())
    current_user = User.query.get(user_id)
    if current_user is None:
        return redirect(url_for('auth_views.login_action'))
    if current_user.role == 'student':
        return redirect(url_for('student_views.student_dash'))
    elif current_user.role == 'staff':
        return redirect(url_for('staff_views.staff_dash'))
    elif current_user.role == 'company':
        return redirect(url_for('company_views.company_dash'))
    return redirect(url_for('auth_views.login_action'))

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})