import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Internship, Application, Shortlist
from App.main import create_app
from App.controllers import (
    create_user, get_all_users_json, get_all_users, initialize,
    create_internship, get_all_internships_json,
    create_application, get_all_applications_json,
    add_to_shortlist, get_all_shortlisted_json, get_all_shortlist
)

app = create_app()
migrate = get_migrate(app)

@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database initialized')

# --------------------
# User Commands
# --------------------
user_cli = AppGroup('user', help='User object commands')

@user_cli.command("create", help="Creates a user based on role")
@click.argument("username")
@click.argument("password")
@click.argument("role")  # 'student', 'staff', or 'company'
@click.option("--degree", default="", help="Student degree")
@click.option("--year", default="", help="Student year")
@click.option("--full_name", default="", help="Staff full name")
@click.option("--department", default="", help="Staff department")
@click.option("--company_name", default="", help="Company name")
@click.option("--website", default="", help="Company website")
def create_user_command(username, password, role, degree, year, full_name, department, company_name, website):
    user = create_user(
        username, password, role,
        degree=degree, year=year,
        full_name=full_name, department=department,
        company_name=company_name, website=website
    )
    if user:
        print(f"{role.capitalize()} user '{username}' created successfully.")
    else:
        print("Failed to create user (might already exist or invalid role).")

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        for u in get_all_users():
            print(u)
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli)

# --------------------
# Internship Commands
# --------------------
internship_cli = AppGroup('internship', help='Internship object commands')

@internship_cli.command("create", help="Creates an internship")
@click.argument("title")
@click.argument("description")
@click.argument("duration")
@click.argument("company_id", type=int)
def create_internship_command(title, description, duration, company_id):
    internship = create_internship(title, description, duration, company_id)
    if internship:
        print(f'Internship "{title}" created!')
    else:
        print(f'Failed to create internship. Invalid company ID?')

@internship_cli.command("list", help="Lists internships in the database")
@click.argument("format", default="string")
def list_internship_command(format):
    internships = get_all_internships_json()
    if format == 'string':
        for i in internships:
            print(i)
    else:
        print(internships)

app.cli.add_command(internship_cli)

# --------------------
# Application Commands
# --------------------
application_cli = AppGroup('application', help='Application object commands')

@application_cli.command("create", help="Creates an application")
@click.argument("student_id", type=int)
@click.argument("internship_id", type=int)
@click.argument("resume", default="path/to/resume")
def create_application_command(student_id, internship_id, resume):
    app = create_application(student_id, internship_id, resume)
    if app:
        print(f'Application submitted by student {student_id} for internship {internship_id}')
    else:
        print('Application failed (possibly already exists or invalid IDs)')

@application_cli.command("list", help="Lists applications in the database")
@click.argument("format", default="string")
def list_application_command(format):
    apps = get_all_applications_json()
    if format == 'string':
        for a in apps:
            print(a)
    else:
        print(apps)

app.cli.add_command(application_cli)

# --------------------
# Shortlist Commands
# --------------------
shortlist_cli = AppGroup('shortlist', help='Shortlist object commands')

@shortlist_cli.command("create", help="Creates a shortlist entry")
@click.argument("staff_id", type=int)
@click.argument("student_id", type=int)
@click.argument("internship_id", type=int)
def create_shortlist_command(staff_id, student_id, internship_id):
    s = add_to_shortlist(staff_id, student_id, internship_id)
    if s:
        print(f'Student {student_id} shortlisted for internship {internship_id} by staff {staff_id}')
    else:
        print('Failed to add to shortlist. Check roles or duplicates.')

@shortlist_cli.command("list", help="Lists all shortlisted students")
@click.argument("format", default="string")
def list_shortlist_command(format):
    sl = get_all_shortlist()
    if format == 'string':
        for s in sl:
            print(s.get_json())
    else:
        print(get_all_shortlisted_json())

app.cli.add_command(shortlist_cli)

# --------------------
# All Data
# --------------------
@app.cli.command("list-all", help="Lists all objects in the database")
def list_all_command():
    users = get_all_users_json()
    internships = get_all_internships_json()
    applications = get_all_applications_json()
    shortlists = get_all_shortlisted_json()

    print("Users:")
    for u in users:
        print(u)

    print("\nInternships:")
    for i in internships:
        print(i)

    print("\nApplications:")
    for a in applications:
        print(a)

    print("\nShortlists:")
    for s in shortlists:
        print(s)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)