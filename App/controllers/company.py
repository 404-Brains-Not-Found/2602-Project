from App.database import db
from App.models.company import Company

def create_company(username, password, company_name, website):
    if Company.query.filter_by(username=username).first():
        return None
    company = Company(username, password, company_name, website)
    db.session.add(company)
    db.session.commit()
    return company

def get_company_by_id(id):
    return Company.query.get(id)

def get_company_by_username(username):
    return Company.query.filter_by(username=username).first()

def get_all_companies():
    return Company.query.all()

def get_all_companies_json():
    return [c.get_json() for c in get_all_companies()]
