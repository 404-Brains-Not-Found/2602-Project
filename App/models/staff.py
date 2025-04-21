from App.models.user import User
from App.database import db

class Staff(User):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    full_name = db.Column(db.String(100))
    department = db.Column(db.String(100))

    __mapper_args__ = {
        'polymorphic_identity': 'staff'
    }

    def __init__(self, username, password, full_name, department):
        super().__init__(username, password)
        self.role = 'staff'
        self.full_name = full_name
        self.department = department

    def get_json(self):
        base = super().get_json()
        base.update({
            'full_name': self.full_name,
            'department': self.department
        })
        return base
