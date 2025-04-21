from App.models.user import User
from App.database import db

class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    degree = db.Column(db.String(100))
    year = db.Column(db.String(20))
    fullname = db.Column(db.String(100))

    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

    def __init__(self, username, password, degree, year):
        super().__init__(username, password)
        self.role = 'student'
        self.degree = degree
        self.year = year

    def get_json(self):
        base = super().get_json()
        base.update({
            'degree': self.degree,
            'year': self.year
        })
        return base
