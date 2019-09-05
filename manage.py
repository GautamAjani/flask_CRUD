"""migration file"""

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from apps import db
from apps.models import User
from app import app

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()