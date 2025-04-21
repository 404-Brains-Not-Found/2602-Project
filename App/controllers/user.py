from App.models import User, Student, Staff, Company
from App.database import db

def create_user(username, password, role, **kwargs):
    if get_user_by_username(username):  # prevent duplicates
        return None

    new_user = None

    if role == 'student':
        degree = kwargs.get('degree')
        year = kwargs.get('year')
        new_user = Student(username, password, degree, year)

    elif role == 'staff':
        full_name = kwargs.get('full_name')
        department = kwargs.get('department')
        new_user = Staff(username, password, full_name, department)

    elif role == 'company':
        company_name = kwargs.get('company_name')
        website = kwargs.get('website')
        new_user = Company(username, password, company_name, website)

    else:
        return None  # invalid role

    db.session.add(new_user)
    db.session.commit()
    return new_user

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
    