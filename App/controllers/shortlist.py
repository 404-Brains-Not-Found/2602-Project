from App.models import Shortlist, Student, Staff, Internship
from App.database import db

def add_to_shortlist(staff_id, student_id, internship_id):
    staff = Staff.query.get(staff_id)
    student = Student.query.get(student_id)
    internship = Internship.query.get(internship_id)

    if not staff:
        return (None, "Staff not found")
    if not student:
        return (None, "Student not found")
    if not internship:
        return (None, "Internship not found")

    existing = Shortlist.query.filter_by(student_id=student_id, internship_id=internship_id).first()
    if existing:
        return None  # already shortlisted

    s = Shortlist(staff_id=staff_id, student_id=student_id, internship_id=internship_id)
    db.session.add(s)
    db.session.commit()
    return s

def get_shortlist_by_internship(internship_id):
    return Shortlist.query.filter_by(internship_id=internship_id).all()

def get_shortlist_by_staff(staff_id):
    return Shortlist.query.filter_by(staff_id=staff_id).all()

def get_all_shortlist():
    return Shortlist.query.all()

def get_all_shortlisted_json():
    return [s.get_json() for s in get_all_shortlist()]
