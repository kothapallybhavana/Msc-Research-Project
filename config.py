from pathlib import Path


class Config:
    # The application is keeping its configuration in this file.
    SECRET_KEY = "air_quality_prediction_secret_key"

    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "root"
    MYSQL_DATABASE = "air_quality_db"

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}/{MYSQL_DATABASE}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # The application is locating its local assets here.
    BASE_DIR = Path(__file__).resolve().parent
    MODEL_PATH = BASE_DIR / "models" / "best_air_quality_model.pkl"
    SCALER_PATH = BASE_DIR / "models" / "scaler.pkl"
    DATASET_PATH = BASE_DIR / "csv_data" / "Beijing_Air_Quality_SQL.csv"
