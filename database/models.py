from sqlalchemy.sql import func

from database.database import db


# The application is mapping the MySQL tables to SQLAlchemy models here.
class AirQuality(db.Model):
    __tablename__ = "air_quality"

    No = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.SmallInteger, nullable=False)
    month = db.Column(db.SmallInteger, nullable=False)
    day = db.Column(db.SmallInteger, nullable=False)
    hour = db.Column(db.SmallInteger, nullable=False)
    PM25 = db.Column(db.Float)
    PM10 = db.Column(db.Float)
    SO2 = db.Column(db.Float)
    NO2 = db.Column(db.Float)
    CO = db.Column(db.Float)
    O3 = db.Column(db.Float)
    TEMP = db.Column(db.Float)
    PRES = db.Column(db.Float)
    DEWP = db.Column(db.Float)
    RAIN = db.Column(db.Float)
    wd = db.Column(db.String(10))
    WSPM = db.Column(db.Float)
    station = db.Column(db.String(50))


class PredictionHistory(db.Model):
    # The application is storing each prediction outcome here.
    __tablename__ = "prediction_history"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prediction_time = db.Column(
        db.DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    )
    PM10 = db.Column(db.Float)
    SO2 = db.Column(db.Float)
    NO2 = db.Column(db.Float)
    CO = db.Column(db.Float)
    O3 = db.Column(db.Float)
    TEMP = db.Column(db.Float)
    PRES = db.Column(db.Float)
    DEWP = db.Column(db.Float)
    RAIN = db.Column(db.Float)
    WSPM = db.Column(db.Float)
    predicted_pm25 = db.Column(db.Float, nullable=False)
    air_quality_status = db.Column(db.String(50), nullable=False)
