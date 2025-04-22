from App.database import db
from App.models.staff import Staff
from App.models.internship import Internship

class Shortlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    internship_id = db.Column(db.Integer, db.ForeignKey('internship.id'), unique=True, nullable=False)

    # Relationships
    staff = db.relationship('Staff', backref='created_shortlists')
    internship = db.relationship('Internship')
    applications = db.relationship('Application', backref='shortlist')

    def get_json(self):
        return {
            'id': self.id,
            'internship_id': self.internship_id,
            'internship_title': self.internship.title,
            'staff': self.staff.username,
            'applications': [app.get_json() for app in self.applications]
        }
