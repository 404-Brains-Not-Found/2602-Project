from App.models import Internship, Company
from App.database import db

def create_internship(title, description, duration, company_id):
    company = Company.query.get(company_id)
    if not company:
        return None
    internship = Internship(
        title=title,
        description=description,
        duration=duration,
        company_id=company_id
    )
    db.session.add(internship)
    db.session.commit()
    return internship

def get_internship(id):
    return Internship.query.get(id)

def get_all_internships():
    return Internship.query.all()

def get_all_internships_json():
    return [i.get_json() for i in get_all_internships()]

def get_internships_by_company(company_id):
    return Internship.query.filter_by(company_id=company_id).all()

def get_internship_by_id(internship_id):
    return Internship.query.get(internship_id)

def delete_internship_by_id(internship_id, company_id):
    internship = Internship.query.filter_by(id=internship_id, company_id=company_id).first()
    if internship:
        apps = internship.applications
        for app in apps:
            db.session.delete(app)
        if internship.shortlist:
            db.session.delete(internship.shortlist)
        db.session.delete(internship)
        db.session.commit()
        return True
    return False