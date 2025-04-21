from App.database import db
from App.models.company import Company

class Internship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(50))
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    company = db.relationship('Company', foreign_keys=[company_id])
    
    # One-to-one relationship
    shortlist = db.relationship('Shortlist', back_populates='internship', uselist=False)

    def get_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'duration': self.duration,
            'company_id': self.company_id,
            'company': self.company.company_name if self.company else None,
            'has_shortlist': self.shortlist is not None
        }
