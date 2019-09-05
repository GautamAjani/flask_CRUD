from datetime import datetime
import re
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy
from apps import db

EMAIL_VERIFICATION = r'^([a-zA-Z0-9_.-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$'


class User(db.Model):
    """store the user information"""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    @validates('first_name')
    @classmethod
    def validate_first_name(cls, first_name):
        """validate first name function"""
        if not first_name:
            message = RESPONSES['EMPTY_FIRST_NAME']
            raise AssertionError(message)

        if len(first_name) > 30:
            message = RESPONSES['LENGTH_FIRST_NAME']
            raise AssertionError(message)
        return first_name

    @classmethod
    @validates('last_name')
    def validate_last_name(cls, last_name):
        """validate last name fucntion"""
        if not last_name:
            message = RESPONSES['EMPTY_LAST_NAME']
            raise AssertionError(message)
        if len(last_name) > 30:
            message = RESPONSES['EMPTY_LAST_NAME']
            raise AssertionError(message)
        return last_name

    @classmethod
    @validates('password')
    def validate_password(cls, password):
        """validate password fucntion"""
        if not password:
            message = "Password is not blank"
            raise AssertionError(message)
        if len(passowrd) > 20 and len(password) < 8:
            message = "password between 8 to 20 character"
            raise AssertionError(message)
        return password

    @classmethod
    @validates('email')
    def validate_email(cls, email):
        """validate email fucntion"""
        if email:
            if not re.match(EMAIL_VERIFICATION, email):
                message = RESPONSES['INVALID_EMAIL']
                raise AssertionError(message)

            if len(email) > 255:
                message = RESPONSES['LENGTH_EMAIL']
                raise AssertionError(message)
        return email

    @classmethod
    def create_or_update(cls, data):
        """create or update method """
        user_credential = User.query.filter_by(email=data['email'])
        if user_credential is None:
            user = User()
            user.upsert(data)
            Slot.create(user.id, time_slots())
            UserCredential.create(user, data)
        else:
            user = user_credential.user
            user.upsert(data)
        return user

    def upsert(self, data):
        """update the user Information"""

        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.phone_number = data['phone_number']
        self.profile_picture = data['profile_picture']
        self.email = data['email']
        db.session.add(self)
        db.session.commit()

        return self

    @classmethod
    def get_user(cls, user_id):
        """get user function"""
        user = User.query.filter_by(id=user_id).first()
        return user

class Appointment(db.Model): # pylint: disable=R0902
    """store the appointment information"""

    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('users.id', ondelete='CASCADE'))
    user = db.relationship('User', backref='appointments', passive_deletes=True)
    appointment_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

