from App.database import db
from App.models.staff import Staff

def create_staff(username, password, full_name, department):
    if Staff.query.filter_by(username=username).first():
        return None
    staff = Staff(username, password, full_name, department)
    db.session.add(staff)
    db.session.commit()
    return staff

def get_staff_by_id(id):
    return Staff.query.get(id)

def get_staff_by_username(username):
    return Staff.query.filter_by(username=username).first()

def get_all_staff():
    return Staff.query.all()

def get_all_staff_json():
    return [s.get_json() for s in get_all_staff()]
