from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# from app import db, app
# from main import app
import app

migrate = Migrate(app, app.db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()