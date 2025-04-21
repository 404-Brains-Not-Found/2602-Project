from App.database import db
from App.models.company import Company  # import the subclass directly if needed

class Internship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(50))
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # This will resolve to the actual Company subclass instance
    company = db.relationship('Company', foreign_keys=[company_id])
    shortlist = db.relationship('Shortlist', backref='internship', lazy=True)

    def get_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'duration': self.duration,
            'company_id': self.company_id,
            'company': self.company.company_name  # changed to show company name
        }
