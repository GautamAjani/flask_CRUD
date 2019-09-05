from flask import Flask
from flask_cors import CORS
from apps import db
from apps.controller import USER_BLUEPRINT as user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin@localhost:3306/demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
CORS(app)
db.init_app(app)
app.register_blueprint(user, url_prefix='/api/v1')

if __name__ == "__main__":
    app.run()