from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# from app import db, app
# from main import app
# from .app import app, db
import app.init_app

migrate = Migrate(app.app.app, app.app.db)

manager = Manager(app.app.app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()