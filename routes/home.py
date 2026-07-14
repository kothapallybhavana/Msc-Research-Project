from flask import Blueprint, render_template
import pandas as pd

from database.queries import get_prediction_history

home_bp = Blueprint("home", __name__)


# The application is serving the home page from here.
@home_bp.route("/")
def home():
    return render_template("index.html")


# The application is serving the prediction history page from here.
@home_bp.route("/history")
def history():
    history_frame = get_prediction_history()
    if not history_frame.empty:
        history_frame["prediction_time"] = pd.to_datetime(
            history_frame["prediction_time"]
        ).dt.strftime("%Y-%m-%d %H:%M:%S")
    return render_template(
        "history.html",
        records=history_frame.to_dict("records"),
    )
