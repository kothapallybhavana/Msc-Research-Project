from flask import Blueprint, jsonify, render_template
import plotly.io as pio

from database.queries import (
    get_average_pollutants_chart,
    get_dataset_summary,
    get_environmental_statistics,
    get_historical_pm25_trend,
    get_monthly_pm25,
    get_pm10_trend,
    get_parameter_chart_data,
    get_station_distribution,
    get_top_pm25_records,
)

dashboard_bp = Blueprint("dashboard", __name__)


# The dashboard is building the reusable parameter chart payloads here.
def _build_parameter_chart(parameter_data, column_name, display_name, description):
    column_frame = parameter_data[["No", column_name]].dropna().copy()
    if column_frame.empty:
        return None

    x_values = column_frame["No"].astype(int).tolist()
    y_values = column_frame[column_name].astype(float).tolist()

    highest_index = column_frame[column_name].idxmax()
    lowest_index = column_frame[column_name].idxmin()
    highest_row = column_frame.loc[highest_index]
    lowest_row = column_frame.loc[lowest_index]

    figure = {
        "data": [
            {
                "x": x_values,
                "y": y_values,
                "type": "scatter",
                "mode": "lines+markers",
                "marker": {"size": 4, "color": "#0d6efd"},
                "line": {"width": 1.5, "color": "#0d6efd"},
                "name": display_name,
            },
            {
                "x": [int(highest_row["No"])],
                "y": [float(highest_row[column_name])],
                "type": "scatter",
                "mode": "markers+text",
                "marker": {"size": 11, "color": "#dc3545"},
                "text": [f"Highest: {float(highest_row[column_name]):.2f}"],
                "textposition": "top center",
                "name": "Highest",
                "showlegend": False,
            },
            {
                "x": [int(lowest_row["No"])],
                "y": [float(lowest_row[column_name])],
                "type": "scatter",
                "mode": "markers+text",
                "marker": {"size": 11, "color": "#198754"},
                "text": [f"Lowest: {float(lowest_row[column_name]):.2f}"],
                "textposition": "bottom center",
                "name": "Lowest",
                "showlegend": False,
            },
        ],
        "layout": {
            "title": {"text": f"{display_name} Readings"},
            "height": 420,
            "margin": {"l": 40, "r": 40, "t": 60, "b": 50},
            "xaxis": {"title": {"text": "Record No"}, "title_standoff": 15},
            "yaxis": {"title": {"text": display_name}, "title_standoff": 15},
        },
    }

    return {
        "id": f"{column_name.lower()}-chart",
        "name": display_name,
        "description": description,
        "stats": {
            "records": int(len(column_frame)),
            "average": round(float(column_frame[column_name].mean()), 2),
            "highest": round(float(highest_row[column_name]), 2),
            "highest_no": int(highest_row["No"]),
            "lowest": round(float(lowest_row[column_name]), 2),
            "lowest_no": int(lowest_row["No"]),
        },
        "figure": figure,
    }


# The dashboard is building the monthly PM2.5 chart payload here.
def _build_monthly_pm25_chart(monthly_pm25):
    chart_frame = monthly_pm25[["month", "PM25"]].dropna().copy()
    if chart_frame.empty:
        return None

    x_values = chart_frame["month"].astype(int).tolist()
    y_values = chart_frame["PM25"].astype(float).tolist()

    highest_index = chart_frame["PM25"].idxmax()
    lowest_index = chart_frame["PM25"].idxmin()
    highest_row = chart_frame.loc[highest_index]
    lowest_row = chart_frame.loc[lowest_index]

    # The dashboard is showing the month-by-month PM2.5 pattern from the database.
    figure = {
        "data": [
            {
                "x": x_values,
                "y": y_values,
                "type": "scatter",
                "mode": "lines+markers",
                "marker": {"size": 8, "color": "#0d6efd"},
                "line": {"width": 2, "color": "#0d6efd"},
                "name": "Monthly PM2.5",
            },
            {
                "x": [int(highest_row["month"])],
                "y": [float(highest_row["PM25"])],
                "type": "scatter",
                "mode": "markers+text",
                "marker": {"size": 11, "color": "#dc3545"},
                "text": [f"Highest: {float(highest_row['PM25']):.2f}"],
                "textposition": "top center",
                "name": "Highest Month",
                "showlegend": False,
            },
            {
                "x": [int(lowest_row["month"])],
                "y": [float(lowest_row["PM25"])],
                "type": "scatter",
                "mode": "markers+text",
                "marker": {"size": 11, "color": "#198754"},
                "text": [f"Lowest: {float(lowest_row['PM25']):.2f}"],
                "textposition": "bottom center",
                "name": "Lowest Month",
                "showlegend": False,
            },
        ],
        "layout": {
            "title": {"text": "Monthly PM2.5 Trend"},
            "height": 420,
            "margin": {"l": 40, "r": 40, "t": 60, "b": 50},
            "xaxis": {"title": {"text": "Month"}, "title_standoff": 15},
            "yaxis": {"title": {"text": "PM2.5"}, "title_standoff": 15},
        },
    }

    return {
        "id": "monthly-pm25-chart",
        "name": "Monthly PM2.5",
        "description": "This chart is showing how PM2.5 changes across the available months in the database.",
        "stats": {
            "records": int(len(chart_frame)),
            "average": round(float(chart_frame["PM25"].mean()), 2),
            "highest": round(float(highest_row["PM25"]), 2),
            "highest_month": int(highest_row["month"]),
            "lowest": round(float(lowest_row["PM25"]), 2),
            "lowest_month": int(lowest_row["month"]),
        },
        "figure": figure,
    }


# The dashboard is building the top PM2.5 chart payload here.
def _build_top_pm25_chart(top_pm25_records):
    chart_frame = top_pm25_records[["No", "PM25", "year", "month", "day", "hour", "station"]].dropna().copy()
    if chart_frame.empty:
        return None

    x_values = chart_frame["No"].astype(int).tolist()
    y_values = chart_frame["PM25"].astype(float).tolist()

    highest_index = chart_frame["PM25"].idxmax()
    lowest_index = chart_frame["PM25"].idxmin()
    highest_row = chart_frame.loc[highest_index]
    lowest_row = chart_frame.loc[lowest_index]

    # The dashboard is highlighting the strongest and weakest records in the top PM2.5 list.
    figure = {
        "data": [
            {
                "x": x_values,
                "y": y_values,
                "type": "bar",
                "marker": {"color": "#0d6efd"},
                "width": 80,
                "name": "Top PM2.5 Records",
            },
            {
                "x": [int(highest_row["No"])],
                "y": [float(highest_row["PM25"])],
                "type": "scatter",
                "mode": "markers+text",
                "marker": {"size": 11, "color": "#dc3545"},
                "text": [f"Highest: {float(highest_row['PM25']):.2f}"],
                "textposition": "top center",
                "name": "Highest Record",
                "showlegend": False,
            },
            {
                "x": [int(lowest_row["No"])],
                "y": [float(lowest_row["PM25"])],
                "type": "scatter",
                "mode": "markers+text",
                "marker": {"size": 11, "color": "#198754"},
                "text": [f"Lowest: {float(lowest_row['PM25']):.2f}"],
                "textposition": "bottom center",
                "name": "Lowest Record",
                "showlegend": False,
            },
        ],
        "layout": {
            "title": {"text": "Top 10 Highest PM2.5 Records"},
            "height": 420,
            "margin": {"l": 60, "r": 40, "t": 60, "b": 50},
            "bargap": 0.2,
            "xaxis": {"title": {"text": "Record No"}, "title_standoff": 15},
            "yaxis": {"title": {"text": "PM2.5"}, "title_standoff": 15},
        },
    }

    return {
        "id": "top-pm25-chart",
        "name": "Top 10 Highest PM2.5 Records",
        "description": "This chart is showing the highest PM2.5 readings stored in the database and the related record numbers.",
        "stats": {
            "records": int(len(chart_frame)),
            "average": round(float(chart_frame["PM25"].mean()), 2),
            "highest": round(float(highest_row["PM25"]), 2),
            "highest_no": int(highest_row["No"]),
            "lowest": round(float(lowest_row["PM25"]), 2),
            "lowest_no": int(lowest_row["No"]),
        },
        "figure": figure,
    }


# The dashboard is building the common chart payload for the proposal charts here.
def _build_trend_chart(chart_frame, x_column, y_column, chart_id, name, description, x_title, y_title):
    prepared_frame = chart_frame[[x_column, y_column]].dropna().copy()
    if prepared_frame.empty:
        return None

    x_values = prepared_frame[x_column].tolist()
    y_values = prepared_frame[y_column].astype(float).tolist()

    highest_index = prepared_frame[y_column].idxmax()
    lowest_index = prepared_frame[y_column].idxmin()
    highest_row = prepared_frame.loc[highest_index]
    lowest_row = prepared_frame.loc[lowest_index]

    figure = {
        "data": [
            {
                "x": x_values,
                "y": y_values,
                "type": "scatter",
                "mode": "lines+markers",
                "marker": {"size": 6, "color": "#0d6efd"},
                "line": {"width": 2, "color": "#0d6efd"},
                "name": name,
            },
            {
                "x": [highest_row[x_column]],
                "y": [float(highest_row[y_column])],
                "type": "scatter",
                "mode": "markers+text",
                "marker": {"size": 11, "color": "#dc3545"},
                "text": [f"Highest: {float(highest_row[y_column]):.2f}"],
                "textposition": "top center",
                "name": "Highest",
                "showlegend": False,
            },
            {
                "x": [lowest_row[x_column]],
                "y": [float(lowest_row[y_column])],
                "type": "scatter",
                "mode": "markers+text",
                "marker": {"size": 11, "color": "#198754"},
                "text": [f"Lowest: {float(lowest_row[y_column]):.2f}"],
                "textposition": "bottom center",
                "name": "Lowest",
                "showlegend": False,
            },
        ],
        "layout": {
            "title": {"text": name},
            "height": 420,
            "margin": {"l": 40, "r": 40, "t": 60, "b": 50},
            "xaxis": {"title": {"text": x_title}, "title_standoff": 15},
            "yaxis": {"title": {"text": y_title}, "title_standoff": 15},
        },
    }

    return {
        "id": chart_id,
        "name": name,
        "description": description,
        "stats": {
            "records": int(len(prepared_frame)),
            "average": round(float(prepared_frame[y_column].mean()), 2),
            "highest": round(float(highest_row[y_column]), 2),
            "highest_label": highest_row[x_column],
            "lowest": round(float(lowest_row[y_column]), 2),
            "lowest_label": lowest_row[x_column],
        },
        "figure": figure,
    }


# The dashboard is building the live report payload here.
def _build_dashboard_report():
    summary = get_dataset_summary()
    pollution_statistics = get_average_pollutants_chart()
    environmental_statistics = get_environmental_statistics()
    parameter_data = get_parameter_chart_data()
    historical_pm25 = get_historical_pm25_trend()
    pm10_trend = get_pm10_trend()
    monthly_pm25 = get_monthly_pm25()
    station_distribution = get_station_distribution()
    top_pm25_records = get_top_pm25_records()

    parameter_chart_specs = [
        ("PM25", "PM2.5"),
        ("PM10", "PM10"),
        ("SO2", "SO2"),
        ("NO2", "NO2"),
        ("CO", "CO"),
        ("O3", "O3"),
        ("TEMP", "Temperature"),
        ("PRES", "Pressure"),
        ("DEWP", "Dew Point"),
    ]

    parameter_summaries = []
    for column_name, display_name in parameter_chart_specs:
        chart = _build_parameter_chart(
            parameter_data,
            column_name,
            display_name,
            f"This chart is showing how {display_name.lower()} is changing across the imported air quality records.",
        )
        if chart is not None:
            parameter_summaries.append(
                {
                    "name": chart["name"],
                    "description": chart["description"],
                    "average": chart["stats"]["average"],
                    "highest": chart["stats"]["highest"],
                    "lowest": chart["stats"]["lowest"],
                }
            )

    historical_pm25_chart = _build_trend_chart(
        historical_pm25,
        "record_date",
        "PM25",
        "historical-pm25-chart",
        "Historical PM2.5 Trend",
        "This chart is showing the average PM2.5 reading over time from the database.",
        "Record Date",
        "PM2.5",
    )
    pm10_trend_chart = _build_trend_chart(
        pm10_trend,
        "record_date",
        "PM10",
        "pm10-trend-chart",
        "PM10 Trend",
        "This chart is showing the average PM10 reading over time from the database.",
        "Record Date",
        "PM10",
    )
    average_pollutants_frame = pollution_statistics.rename(columns={"pollutant": "label", "average_value": "value"})
    average_pollutants_chart = _build_trend_chart(
        average_pollutants_frame,
        "label",
        "value",
        "average-pollutants-chart",
        "Average Pollutants",
        "This chart is showing the average level of each pollutant stored in the database.",
        "Pollutant",
        "Average Value",
    )
    station_distribution_chart = _build_trend_chart(
        station_distribution,
        "station",
        "record_count",
        "station-distribution-chart",
        "Station Distribution",
        "This chart is showing how many records are stored for each station in the database.",
        "Station",
        "Record Count",
    )
    monthly_pm25_chart = _build_monthly_pm25_chart(monthly_pm25)
    top_pm25_chart = _build_top_pm25_chart(top_pm25_records)

    return {
        "summary": {
            "total_records": int(summary["total_records"]),
            "avg_pm25": summary["avg_pm25"],
            "avg_pm10": summary["avg_pm10"],
        },
        "pollution_statistics": pollution_statistics.to_dict("records"),
        "environmental_statistics": environmental_statistics.to_dict("records"),
        "parameter_summaries": parameter_summaries,
        "historical_pm25": historical_pm25_chart["stats"] if historical_pm25_chart else None,
        "pm10_trend": pm10_trend_chart["stats"] if pm10_trend_chart else None,
        "average_pollutants": average_pollutants_chart["stats"] if average_pollutants_chart else None,
        "station_distribution": station_distribution_chart["stats"] if station_distribution_chart else None,
        "monthly_pm25": monthly_pm25_chart["stats"] if monthly_pm25_chart else None,
        "top_pm25": top_pm25_chart["stats"] if top_pm25_chart else None,
        "generated_at": "live",
    }


@dashboard_bp.route("/dashboard")
def dashboard():
    # The dashboard is loading the summary and chart-ready records here.
    summary = get_dataset_summary()
    pollution_statistics = get_average_pollutants_chart()
    environmental_statistics = get_environmental_statistics()
    parameter_data = get_parameter_chart_data()
    historical_pm25 = get_historical_pm25_trend()
    pm10_trend = get_pm10_trend()
    monthly_pm25 = get_monthly_pm25()
    station_distribution = get_station_distribution()
    top_pm25_records = get_top_pm25_records()

    show_historical_pm25 = len(historical_pm25) > 1
    show_pm10_trend = len(pm10_trend) > 1
    show_average_pollutants = len(pollution_statistics) > 1
    show_station_distribution = len(station_distribution) > 1
    monthly_pm25_chart = _build_monthly_pm25_chart(monthly_pm25)
    top_pm25_chart = _build_top_pm25_chart(top_pm25_records)
    show_monthly_pm25 = monthly_pm25_chart is not None
    show_top_pm25 = top_pm25_chart is not None

    # The dashboard is preparing the proposal charts with matching stats panels here.
    parameter_chart_specs = [
        ("PM25", "PM2.5"),
        ("PM10", "PM10"),
        ("SO2", "SO2"),
        ("NO2", "NO2"),
        ("CO", "CO"),
        ("O3", "O3"),
        ("TEMP", "Temperature"),
        ("PRES", "Pressure"),
        ("DEWP", "Dew Point"),
    ]

    # The dashboard is building the parameter chart cards here.
    parameter_charts = []
    for column_name, display_name in parameter_chart_specs:
        description = (
            f"This chart is showing how {display_name.lower()} is changing "
            f"across the imported air quality records."
        )
        chart = _build_parameter_chart(parameter_data, column_name, display_name, description)
        if chart is not None:
            parameter_charts.append(chart)

    # The dashboard is building the proposal chart payloads here.
    historical_pm25_chart = _build_trend_chart(
        historical_pm25,
        "record_date",
        "PM25",
        "historical-pm25-chart",
        "Historical PM2.5 Trend",
        "This chart is showing the average PM2.5 reading over time from the database.",
        "Record Date",
        "PM2.5",
    )
    pm10_trend_chart = _build_trend_chart(
        pm10_trend,
        "record_date",
        "PM10",
        "pm10-trend-chart",
        "PM10 Trend",
        "This chart is showing the average PM10 reading over time from the database.",
        "Record Date",
        "PM10",
    )
    average_pollutants_frame = pollution_statistics.rename(columns={"pollutant": "label", "average_value": "value"})
    average_pollutants_chart = _build_trend_chart(
        average_pollutants_frame,
        "label",
        "value",
        "average-pollutants-chart",
        "Average Pollutants",
        "This chart is showing the average level of each pollutant stored in the database.",
        "Pollutant",
        "Average Value",
    )
    station_distribution_chart = _build_trend_chart(
        station_distribution,
        "station",
        "record_count",
        "station-distribution-chart",
        "Station Distribution",
        "This chart is showing how many records are stored for each station in the database.",
        "Station",
        "Record Count",
    )

    # The dashboard is sending the chart payloads to the template here.
    return render_template(
        "dashboard.html",
        summary=summary,
        pollution_statistics=pollution_statistics.to_dict("records"),
        environmental_statistics=environmental_statistics.to_dict("records"),
        parameter_charts=parameter_charts,
        show_historical_pm25=show_historical_pm25,
        show_pm10_trend=show_pm10_trend,
        show_average_pollutants=show_average_pollutants,
        show_station_distribution=show_station_distribution,
        show_monthly_pm25=show_monthly_pm25,
        show_top_pm25=show_top_pm25,
        historical_pm25_chart=historical_pm25_chart,
        pm10_trend_chart=pm10_trend_chart,
        average_pollutants_chart=average_pollutants_chart,
        station_distribution_chart=station_distribution_chart,
        monthly_pm25_chart=monthly_pm25_chart,
        top_pm25_chart=top_pm25_chart,
        graph_historical_pm25=pio.to_html(
            historical_pm25_chart["figure"],
            full_html=False,
            include_plotlyjs=False,
            config={"responsive": True},
        ) if historical_pm25_chart else None,
        graph_pm10_trend=pio.to_html(
            pm10_trend_chart["figure"],
            full_html=False,
            include_plotlyjs=False,
            config={"responsive": True},
        ) if pm10_trend_chart else None,
        graph_average_pollutants=pio.to_html(
            average_pollutants_chart["figure"],
            full_html=False,
            include_plotlyjs=False,
            config={"responsive": True},
        ) if average_pollutants_chart else None,
        graph_station_distribution=pio.to_html(
            station_distribution_chart["figure"],
            full_html=False,
            include_plotlyjs=False,
            config={"responsive": True},
        ) if station_distribution_chart else None,
        graph_monthly_pm25=pio.to_html(
            monthly_pm25_chart["figure"],
            full_html=False,
            include_plotlyjs=False,
            config={"responsive": True},
        ) if monthly_pm25_chart else None,
        graph_top_pm25=pio.to_html(
            top_pm25_chart["figure"],
            full_html=False,
            include_plotlyjs=False,
            config={"responsive": True},
        ) if top_pm25_chart else None,
        dashboard_report=_build_dashboard_report(),
    )


@dashboard_bp.route("/dashboard/report-data")
def dashboard_report_data():
    # The dashboard is returning live report data here.
    return jsonify(_build_dashboard_report())
