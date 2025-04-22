from flask_admin.contrib.sqla import ModelView
from flask_jwt_extended import jwt_required, current_user
from flask_admin import Admin
from flask import request, redirect, url_for, flash
from App.models import User
from App.database import db

class AdminView(ModelView):
    @jwt_required()
    def is_accessible(self):
        return current_user is not None

    def inaccessible_callback(self, name, **kwargs):
        flash("Login to access admin")
        return redirect(url_for('index_page', next=request.url))

def setup_admin(app):
    admin = Admin(app, name='FlaskMVC', template_mode='bootstrap3')
    admin.add_view(AdminView(User, db.session))