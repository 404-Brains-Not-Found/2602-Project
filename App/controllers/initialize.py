from .user import create_user
from .application import create_application
from .internship import create_internship
from .shortlist import add_to_shortlist
from App.database import db

def initialize():
    db.drop_all()
    db.create_all()

    # Create users with inheritance-aware fields
    student = create_user('bob', 'bobpass', 'student', degree='Computer Science', year='Year 2')
    staff = create_user('alice', 'alicepass', 'staff', full_name='Alice Smith', department='Engineering')
    company = create_user('google', 'googlepass', 'company', company_name='Google LLC', website='https://google.com')

    # Use actual IDs returned by created users
    if student and staff and company:
        internship = create_internship('Internship 1', 'Description 1', '1 month', company.id)
        if internship:
            app = create_application(student.id, internship.id, 'path/to/resume')
            add_to_shortlist(staff_id=staff.id, application_id=app.id)

    