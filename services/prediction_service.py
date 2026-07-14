import joblib

from config import Config
from database.database import db
from database.models import PredictionHistory


# The service is loading the trained model and saving each prediction here.
model = joblib.load(Config.MODEL_PATH)


# The service is preparing the model inputs in the expected order here.
def preprocess_input(data):
    return [[
        float(data["PM10"]),
        float(data["SO2"]),
        float(data["NO2"]),
        float(data["CO"]),
        float(data["O3"]),
        float(data["TEMP"]),
        float(data["PRES"]),
        float(data["DEWP"]),
        float(data["RAIN"]),
        float(data["WSPM"]),
    ]]


def predict_pm25(data):
    processed_data = preprocess_input(data)
    return float(model.predict(processed_data)[0])


# The service is classifying the predicted PM2.5 value here.
def classify_air_quality_status(predicted_pm25):
    if predicted_pm25 < 35:
        return "Excellent"
    if predicted_pm25 < 75:
        return "Good"
    if predicted_pm25 < 115:
        return "Moderate"
    if predicted_pm25 < 150:
        return "Poor"
    return "Very Poor"


def save_prediction_history(data, predicted_pm25, air_quality_status):
    # The service is persisting the prediction result into MySQL here.
    record = PredictionHistory(
        PM10=float(data["PM10"]),
        SO2=float(data["SO2"]),
        NO2=float(data["NO2"]),
        CO=float(data["CO"]),
        O3=float(data["O3"]),
        TEMP=float(data["TEMP"]),
        PRES=float(data["PRES"]),
        DEWP=float(data["DEWP"]),
        RAIN=float(data["RAIN"]),
        WSPM=float(data["WSPM"]),
        predicted_pm25=predicted_pm25,
        air_quality_status=air_quality_status,
    )

    db.session.add(record)
    db.session.commit()


def predict_and_store(data):
    # The service is running prediction and persistence together here.
    predicted_pm25 = predict_pm25(data)
    air_quality_status = classify_air_quality_status(predicted_pm25)
    save_prediction_history(data, predicted_pm25, air_quality_status)
    return predicted_pm25, air_quality_status
