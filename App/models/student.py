from App.models.user import User
from App.database import db

class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    degree = db.Column(db.String(100))
    year = db.Column(db.String(20))
    f_name = db.Column(db.String(50))
    l_name = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

    def __init__(self, username, password, degree, year, f_name, l_name):
        super().__init__(username, password)
        self.role = 'student'
        self.f_name = f_name
        self.l_name = l_name
        self.degree = degree
        self.year = year

    def get_json(self):
        base = super().get_json()
        base.update({
            'f_name': self.f_name,
            'l_name': self.l_name,
            'degree': self.degree,
            'year': self.year
        })
        return base
