import pandas as pd
from sqlalchemy import create_engine, text

from config import Config


# The application is centralizing its database read queries here.
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)


# The application is returning query results as DataFrames here.
def _read_frame(query):
    return pd.read_sql_query(text(query), engine)


def get_dataset_summary():
    query = """
    SELECT
        COUNT(*) AS total_records,
        COUNT(DISTINCT station) AS total_stations,
        ROUND(AVG(PM25), 2) AS avg_pm25,
        ROUND(AVG(PM10), 2) AS avg_pm10
    FROM air_quality
    """
    return _read_frame(query).iloc[0].to_dict()


def get_pollution_statistics():
    query = """
    SELECT 'PM2.5' AS pollutant, ROUND(AVG(PM25), 2) AS average_value FROM air_quality
    UNION ALL
    SELECT 'PM10' AS pollutant, ROUND(AVG(PM10), 2) AS average_value FROM air_quality
    UNION ALL
    SELECT 'SO2' AS pollutant, ROUND(AVG(SO2), 2) AS average_value FROM air_quality
    UNION ALL
    SELECT 'NO2' AS pollutant, ROUND(AVG(NO2), 2) AS average_value FROM air_quality
    UNION ALL
    SELECT 'CO' AS pollutant, ROUND(AVG(CO), 2) AS average_value FROM air_quality
    UNION ALL
    SELECT 'O3' AS pollutant, ROUND(AVG(O3), 2) AS average_value FROM air_quality
    """
    return _read_frame(query)


def get_environmental_statistics():
    query = """
    SELECT 'Temperature' AS metric, ROUND(AVG(TEMP), 2) AS average_value FROM air_quality
    UNION ALL
    SELECT 'Pressure' AS metric, ROUND(AVG(PRES), 2) AS average_value FROM air_quality
    UNION ALL
    SELECT 'Dew Point' AS metric, ROUND(AVG(DEWP), 2) AS average_value FROM air_quality
    UNION ALL
    SELECT 'Rain' AS metric, ROUND(AVG(RAIN), 2) AS average_value FROM air_quality
    UNION ALL
    SELECT 'Wind Speed' AS metric, ROUND(AVG(WSPM), 2) AS average_value FROM air_quality
    """
    return _read_frame(query)


def get_historical_pm25_trend():
    query = """
    SELECT
        STR_TO_DATE(CONCAT(year, '-', LPAD(month, 2, '0'), '-', LPAD(day, 2, '0')), '%Y-%m-%d') AS record_date,
        ROUND(AVG(PM25), 2) AS PM25
    FROM air_quality
    GROUP BY record_date
    ORDER BY record_date
    """
    return _read_frame(query)


def get_pm10_trend():
    query = """
    SELECT
        STR_TO_DATE(CONCAT(year, '-', LPAD(month, 2, '0'), '-', LPAD(day, 2, '0')), '%Y-%m-%d') AS record_date,
        ROUND(AVG(PM10), 2) AS PM10
    FROM air_quality
    GROUP BY record_date
    ORDER BY record_date
    """
    return _read_frame(query)


def get_average_pollutants_chart():
    return get_pollution_statistics()


def get_station_distribution():
    query = """
    SELECT station, COUNT(*) AS record_count
    FROM air_quality
    GROUP BY station
    ORDER BY record_count DESC
    """
    return _read_frame(query)


def get_monthly_pm25():
    query = """
    SELECT
        month,
        ROUND(AVG(PM25), 2) AS PM25
    FROM air_quality
    GROUP BY month
    ORDER BY month
    """
    return _read_frame(query)


def get_top_pm25_records():
    query = """
    SELECT
        No,
        year,
        month,
        day,
        hour,
        station,
        PM25
    FROM air_quality
    ORDER BY PM25 DESC
    LIMIT 10
    """
    return _read_frame(query)


def get_prediction_history():
    query = """
    SELECT
        id,
        prediction_time,
        PM10,
        SO2,
        NO2,
        CO,
        O3,
        TEMP,
        PRES,
        DEWP,
        RAIN,
        WSPM,
        predicted_pm25,
        air_quality_status
    FROM prediction_history
    ORDER BY prediction_time DESC, id DESC
    """
    return _read_frame(query)


def get_parameter_chart_data():
    query = """
    SELECT No, PM25, PM10, SO2, NO2, CO, O3, TEMP, PRES, DEWP
    FROM air_quality
    ORDER BY No
    """
    return _read_frame(query)
