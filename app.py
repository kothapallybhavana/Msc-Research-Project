from flask import Flask

from config import Config
from database.database import init_db
from routes.dashboard import dashboard_bp
from routes.home import home_bp
from routes.prediction import prediction_bp


# The application is wiring Flask and blueprint registration here.
app = Flask(__name__)
app.config.from_object(Config)

init_db(app)

# The application is registering the route groups here.
app.register_blueprint(home_bp)
app.register_blueprint(prediction_bp)
app.register_blueprint(dashboard_bp)


if __name__ == "__main__":
    app.run(debug=True)
