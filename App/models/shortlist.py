from App.database import db
from App.models.student import Student
from App.models.staff import Staff
from App.models.internship import Internship

class Shortlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    internship_id = db.Column(db.Integer, db.ForeignKey('internship.id'), nullable=False)

    # Use subclasses instead of base User
    staff = db.relationship('Staff', foreign_keys=[staff_id])
    student = db.relationship('Student', foreign_keys=[student_id])
    internship = db.relationship('Internship', backref='shortlisted_students')
    applications = db.relationship('Application', backref='shortlisted_students')

    def get_json(self):
        return {
            'id': self.id,
            'staff': self.staff.username if self.staff else None,
            'student': self.student.username if self.student else None,
            'internship': self.internship.title if self.internship else None,
            'internship_id': self.internship_id if self.internship else None
        }
