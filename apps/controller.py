from flask import jsonify, Blueprint, request
from werkzeug.security import generate_password_hash
from apps import db
from apps.models import User
from .helper import generate_token
from werkzeug.security import check_password_hash
import pdb

USER_BLUEPRINT = Blueprint('signup', __name__)

@USER_BLUEPRINT.route('/signup', methods=['POST'])
def create_user():
    """User registration in the system."""
    
    try:
        data = request.json
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        email = request.json['email']
        password = request.json['password']
        user_info = User.query.filter_by(email=email).first()
        print(user_info)
        if user_info:
            message = "User already exits"
            code = 400
        else:
            password = generate_password_hash(password)
            user = User()
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.password = password
            db.session.add(user)
            db.session.commit()
            message = "User create successfully"
            code = 200
    except Exception as error:
        return jsonify({'message':str(error)}), 400
    return jsonify({'message':message}), code

import pdb
@USER_BLUEPRINT.route('/login', methods=['POST'])
def login():
    """user social login"""

    try:
        pdb.set_trace()
        data = request.json
        if login_validation(data) is not None:
            return False
        # token = generate_token(user.id, data)
        user = User.query.filter_by(email=request.json['email']).first()
        password = check_password_hash(user.password, request.json['password'])
        if password == True:
            token = generate_token(user.id)
        message = "Login Successfully"
        code = 200
        
    except Exception as ex: # pylint: disable=W0703
        return jsonify({'message':str(ex)}), 400
    return jsonify({'message':message, 'token': token}), code


def login_validation(data):
    """social login validation"""

    User.validate_email(data['email'])