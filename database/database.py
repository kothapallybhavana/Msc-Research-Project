from flask_sqlalchemy import SQLAlchemy

# The application is creating the shared SQLAlchemy instance here.
db = SQLAlchemy()

# The application is attaching the database to Flask here.
def init_db(app):
    db.init_app(app)
