from flask import Blueprint, render_template, request

from services.prediction_service import predict_and_store

prediction_bp = Blueprint("prediction", __name__)


# The application is mapping the predicted status to a visual indicator here.
def _build_status_display(air_quality_status):
    if air_quality_status in {"Excellent", "Good"}:
        return {
            "label": "Safe",
            "icon": "✅",
            "header_class": "bg-success text-white",
            "message": "Air quality is below the alert threshold.",
        }
    if air_quality_status == "Moderate":
        return {
            "label": "Warning",
            "icon": "⚠️",
            "header_class": "bg-warning text-dark",
            "message": "Air quality is approaching the alert threshold.",
        }
    return {
        "label": "Alert",
        "icon": "🚨",
        "header_class": "bg-danger text-white",
        "message": "Air quality is above the alert threshold.",
    }


# The application is serving the prediction form here.
@prediction_bp.route("/prediction")
def prediction_page():
    return render_template("prediction.html")


# The application is handling the prediction result flow here.
@prediction_bp.route("/predict", methods=["POST"])
def prediction():
    try:
        data = {
            "PM10": float(request.form["PM10"]),
            "SO2": float(request.form["SO2"]),
            "NO2": float(request.form["NO2"]),
            "CO": float(request.form["CO"]),
            "O3": float(request.form["O3"]),
            "TEMP": float(request.form["TEMP"]),
            "PRES": float(request.form["PRES"]),
            "DEWP": float(request.form["DEWP"]),
            "RAIN": float(request.form["RAIN"]),
            "WSPM": float(request.form["WSPM"])
        }

        prediction, air_quality_status = predict_and_store(data)
        status_display = _build_status_display(air_quality_status)

        return render_template(
            "result.html",
            prediction=round(prediction, 2),
            air_quality_status=air_quality_status,
            status_display=status_display,
            show_air_quality_alert=prediction < 35,
            input_data=data
        )

    except Exception as e:
        return render_template(
            "prediction.html",
            error=str(e)
        )
