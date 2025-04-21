from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies, set_access_cookies
from App.controllers.internship import *
from App.controllers.application import *
from App.controllers.user import get_user

student_views = Blueprint('student_views', __name__, template_folder='../templates')

@student_views.route('/student_dash', methods=['GET'])
@jwt_required()
def student_dash():
    user_id = int(get_jwt_identity())
    internships = get_all_internships()
    applications = get_applications_by_student(user_id)
    return render_template('temp_dash.html', internships=internships, applications=applications, current_user=get_user(user_id))

@student_views.route('/student/view_internship/<int:internship_id>', methods=['GET'])
@jwt_required()
def view_internship(internship_id):
    internship = get_internship(internship_id)
    showform = request.args.get('apply') == 'true'
    applications = get_applications_by_student(get_jwt_identity())
    if applications:
        student_application = Application.query.filter_by(internship_id=internship_id).first()
    else:
        student_application = None
    return render_template('view_internship.html', internship=internship, student_application=student_application, showform=showform, current_user=get_user(get_jwt_identity()))

@student_views.route('/student/apply_internship/<int:internship_id>', methods=['POST'])
@jwt_required()
def apply_internship(internship_id):
    user_id = int(get_jwt_identity())
    data = request.form
    resume = data.get('resume')
    internship_id = internship_id
    app = create_application(user_id, internship_id, resume)
    if app:
        flash('Application submitted successfully!', 'success')
    else:
        flash('Failed to submit application. You may have already applied.')
    return redirect(url_for('student_views.student_dash'))
    
@student_views.route('/student/delete_application/<int:application_id>', methods=['POST'])
@jwt_required()
def delete_application(application_id):
    user_id = int(get_jwt_identity())
    app = delete_application_by_id(application_id, user_id)
    if app:
        flash('Application deleted successfully!', 'success')
    else:
        flash('Failed to delete application.')
    return redirect(url_for('student_views.student_dash'))

