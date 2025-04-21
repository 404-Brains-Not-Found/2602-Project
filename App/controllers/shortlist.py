from App.models import Shortlist, Application, Staff, Internship
from App.database import db

def add_to_shortlist(application_id, staff_id):
    application = Application.query.get(application_id)
    staff = Staff.query.get(staff_id)

    if not application:
        return None, "Application not found"
    if not staff:
        return None, "Staff not found"

    internship = application.internship
    if not internship:
        return None, "Internship not found"

    # Check if a shortlist already exists for this internship
    shortlist = Shortlist.query.filter_by(internship_id=internship.id).first()
    if not shortlist:
        # Create a new shortlist if not exists
        shortlist = Shortlist(
            internship_id=internship.id,
            staff_id=staff.id
        )
        db.session.add(shortlist)
        db.session.commit()

    # Prevent duplicate application on shortlist
    if application.shortlist_id == shortlist.id:
        return None, "Application already shortlisted"

    # Add application to shortlist
    application.shortlist_id = shortlist.id
    db.session.commit()
    return shortlist, "Application added to shortlist"

def get_shortlist_by_internship(internship_id):
    return Shortlist.query.filter_by(internship_id=internship_id).first()

def get_shortlist_by_staff(staff_id):
    return Shortlist.query.filter_by(staff_id=staff_id).all()

def get_all_shortlist():
    return Shortlist.query.all()

def get_all_shortlisted_json():
    return [s.get_json() for s in get_all_shortlist()]

def remove_from_shortlist(application_id, staff_id):
    application = Application.query.get(application_id)
    staff = Staff.query.get(staff_id)

    if not application:
        return None, "Application not found"
    if not staff:
        return None, "Staff not found"

    shortlist = Shortlist.query.filter_by(id=application.shortlist_id).first()
    if not shortlist:
        return None, "Shortlist not found"

    # Remove application from shortlist
    application.shortlist_id = None
    db.session.commit()
    return shortlist, "Application removed from shortlist"