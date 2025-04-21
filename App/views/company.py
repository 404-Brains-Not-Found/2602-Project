from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies, set_access_cookies
from App.controllers.application import get_application, get_applications_by_internship, update_application_status
from App.controllers.internship import *
from App.controllers.shortlist import *



company_views = Blueprint('company_views', __name__, template_folder='../templates')


@company_views.route('/company_dash', methods=['GET'])
@jwt_required()
def company_dash():
    user_id = int(get_jwt_identity())
    internships = get_internships_by_company(user_id)
    shortlists = get_all_shortlist()
    return render_template('company_dash.html', internships=internships, shortlists=shortlists)

@company_views.route('/company/view_internship/<int:internship_id>', methods=['GET'])
@jwt_required()
def view_internship(internship_id):
    internship = get_internship(internship_id)
    applications = get_applications_by_internship(internship_id)
    shortlisted_applications = get_shortlist_by_internship(internship_id)
    return render_template('view_internship.html', internship=internship, applications=applications, shortlist=shortlisted_applications)

@company_views.route('/company/add_internship', methods=['POST'])
@jwt_required()
def add_internship():
    user_id = int(get_jwt_identity())
    data = request.form
    title = data.get('title')
    description = data.get('description')
    duration = data.get('duration')
    internship = create_internship(title, description, duration, user_id)
    if internship:
        flash('Internship created successfully!', 'success')
    else:
        flash('Failed to create internship.')
    return redirect(url_for('company_views.company_dash'))

@company_views.route('/company/delete_internship/<int:internship_id>', methods=['POST'])
@jwt_required()
def delete_internship(internship_id):
    user_id = int(get_jwt_identity())
    internship = delete_internship_by_id(internship_id, user_id)
    if internship:
        flash('Internship deleted successfully!', 'success')
    else:
        flash('Failed to delete internship.')
    return redirect(url_for('company_views.company_dash'))

@company_views.route('/company/view_app/<int:application_id>', methods=['POST'])
@jwt_required()
def view_app(application_id):
    user_id = int(get_jwt_identity())
    application = get_application(application_id)
    internship = get_internship(application.internship_id)
    return render_template('view_application.html', application=application, internship=internship)

@company_views.route('/company/update_app/<int:application_id>', methods=['POST'])
@jwt_required()
def update_application(application_id):
    user_id = int(get_jwt_identity())
    data = request.form
    status = data.get('status')
    application = update_application_status(application_id, status)
    if application.status == 'approved':
        flash('Application status updated successfully!', 'success')
    elif application.status == 'rejected':
        remove_from_shortlist(application_id, user_id)
        flash('Application status updated successfully!', 'success')
    else:
        flash('Failed to update application status.')
    return redirect(url_for('company_views.company_dash'))