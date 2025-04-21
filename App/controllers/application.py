from App.models import Application, Student, Internship
from App.database import db

def create_application(student_id, internship_id, resume=None):
    student = Student.query.get(student_id)
    internship = Internship.query.get(internship_id)

    if not student or not internship:
        return None

    existing = Application.query.filter_by(student_id=student_id, internship_id=internship_id).first()
    if existing:
        return None  # prevent duplicate applications

    app = Application(student_id=student_id, internship_id=internship_id, resume=resume)
    db.session.add(app)
    db.session.commit()
    return app

def get_application(id):
    return Application.query.get(id)

def get_applications_by_student(student_id):
    return Application.query.filter_by(student_id=student_id).all()

def get_applications_by_internship(internship_id):
    return Application.query.filter_by(internship_id=internship_id).all()

def update_application_status(id, status):
    app = get_application(id)
    if app:
        app.status = status
        db.session.commit()
        return app
    return None

def get_all_applications():
    return Application.query.all()

def get_all_applications_json():
    return [a.get_json() for a in get_all_applications()]

def delete_application_by_id(application_id, student_id):
    app = Application.query.filter_by(id=application_id, student_id=student_id).first()
    if app:
        db.session.delete(app)
        db.session.commit()
        return True
    return False
