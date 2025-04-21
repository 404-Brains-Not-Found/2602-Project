from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies, set_access_cookies
from App.controllers.application import get_applications_by_internship
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
    return render_template('view_internship.html', internship=internship, applications=applications, shortlisted_applications=shortlisted_applications)