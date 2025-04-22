from App.database import db
from App.models.student import Student

def create_student(username, password, degree, year, f_name, l_name):
    if Student.query.filter_by(username=username).first():
        return None
    student = Student(username, password, degree, year, f_name, l_name)
    db.session.add(student)
    db.session.commit()
    return student

def get_student_by_id(id):
    return Student.query.get(id)

def get_student_by_username(username):
    return Student.query.filter_by(username=username).first()

def get_all_students():
    return Student.query.all()

def get_all_students_json():
    return [s.get_json() for s in get_all_students()]
