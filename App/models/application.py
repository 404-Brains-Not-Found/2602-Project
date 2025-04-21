from App.database import db
from App.models.student import Student
from App.models.internship import Internship

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    internship_id = db.Column(db.Integer, db.ForeignKey('internship.id'), nullable=False)
    resume = db.Column(db.String(255))  # path to uploaded file
    status = db.Column(db.String(20), default='pending')

    # Inherited subclass relationship
    student = db.relationship('Student', foreign_keys=[student_id])
    internship = db.relationship('Internship', backref='applications')

    def get_json(self):
        return {
            'id': self.id,
            'student': self.student.username,
            'internship': self.internship.title,
            'status': self.status,
            'resume': self.resume
        }
