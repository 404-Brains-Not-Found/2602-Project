from App.models.user import User
from App.database import db

class Company(User):
    __tablename__ = 'company'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    company_name = db.Column(db.String(100))
    website = db.Column(db.String(100))

    __mapper_args__ = {
        'polymorphic_identity': 'company'
    }

    def __init__(self, username, password, company_name, website):
        super().__init__(username, password)
        self.role = 'company'
        self.company_name = company_name
        self.website = website

    def get_json(self):
        base = super().get_json()
        base.update({
            'company_name': self.company_name,
            'website': self.website
        })
        return base
