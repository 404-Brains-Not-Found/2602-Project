from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies, set_access_cookies
from App.controllers.user import *
from App.controllers.internship import *
from App.controllers.application import *
from App.controllers.shortlist import *

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

@staff_views.route('/staff_dash', methods=['GET'])
@jwt_required()
def staff_dash():
    user_id = int(get_jwt_identity())
    internships = get_all_internships()
    applications = get_all_applications()
    shortlist = get_all_shortlist()
    return render_template('staff_dash.html', internships=internships, applications=applications, shortlist=shortlist)

@staff_views.route('/staff/view_internship/<int:internship_id>', methods=['GET'])
@jwt_required()
def view_internship(internship_id):
    internship = get_internship(internship_id)
    applications = get_applications_by_internship(internship_id)
    shortlisted_applications = get_shortlist_by_internship(internship_id)
    return render_template('view_internship.html', internship=internship, applications=applications, shortlist=shortlisted_applications)


@staff_views.route('/staff/view_application/<int:application_id>', methods=['GET'])
@jwt_required()
def view_application(application_id):
    application = get_application(application_id)
    return render_template('view_application.html', application=application)

@staff_views.route('/staff/shortlist/<int:application_id>', methods=['POST'])
@jwt_required()
def shortlist(application_id):
    user_id = int(get_jwt_identity())
    app = get_application(application_id)
    if app is None:
        flash('Application not found.', 'error')
        return redirect(url_for('staff_views.staff_dash'))
    internship_id = app.internship_id
    data = request.form
    if data.get('status') == 'shortlist':
        update_application_status(application_id, 'shortlisted')
        if add_to_shortlist(staff_id=user_id, application_id=application_id):
            flash('Application shortlisted successfully!', 'success')
        else:
            flash('Failed to shortlist application.', 'error')
    
    if data.get('status') == 'reject':
        update_application_status(application_id, 'rejected')
        if update_application_status(application_id, 'rejected'):
            flash('Application rejected successfully!', 'success')
        else:
            flash('Failed to reject application.', 'error')
    return redirect(url_for('staff_views.view_internship', internship_id=internship_id))

@staff_views.route('/staff/remove_shortlist/<int:application_id>', methods=['POST'])
@jwt_required()
def remove_shortlist(application_id):
    user_id = int(get_jwt_identity())
    app = get_application(application_id)
    if app is None:
        flash('Application not found.', 'error')
        return redirect(url_for('staff_views.staff_dash'))
    internship_id = app.internship_id
    if remove_from_shortlist(staff_id=user_id, application_id=application_id):
        flash('Application removed from shortlist successfully!', 'success')
    else:
        flash('Failed to remove application from shortlist.', 'error')
    return redirect(url_for('staff_views.view_internship', internship_id=internship_id))

    