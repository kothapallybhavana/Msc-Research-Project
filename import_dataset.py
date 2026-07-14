from sqlalchemy import create_engine, text

import pandas as pd

from config import Config


# The script is importing the Beijing air quality dataset into MySQL here.
def import_dataset():
    # The script is reading the source dataset into memory here.
    frame = pd.read_csv(Config.DATASET_PATH)
    frame.columns = [
        "No",
        "year",
        "month",
        "day",
        "hour",
        "PM25",
        "PM10",
        "SO2",
        "NO2",
        "CO",
        "O3",
        "TEMP",
        "PRES",
        "DEWP",
        "RAIN",
        "wd",
        "WSPM",
        "station",
    ]

    # The script is creating the database connection here.
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)

    data_columns = [
        "year",
        "month",
        "day",
        "hour",
        "PM25",
        "PM10",
        "SO2",
        "NO2",
        "CO",
        "O3",
        "TEMP",
        "PRES",
        "DEWP",
        "RAIN",
        "wd",
        "WSPM",
        "station",
    ]

    with engine.begin() as connection:
        # The script is collecting the rows that already exist here.
        existing_rows = connection.execute(
            text(
                """
                SELECT year, month, day, hour, PM25, PM10, SO2, NO2, CO, O3,
                       TEMP, PRES, DEWP, RAIN, wd, WSPM, station
                FROM air_quality
                """
            )
        ).fetchall()

        existing_keys = {
            tuple(row)
            for row in existing_rows
        }

        # The script is keeping only the rows that are not already stored here.
        frame = frame[~frame[data_columns].apply(tuple, axis=1).isin(existing_keys)].copy()

        # The script is continuing the primary key sequence here.
        max_no = connection.execute(
            text("SELECT COALESCE(MAX(No), 0) FROM air_quality")
        ).scalar_one()
        frame["No"] = range(int(max_no) + 1, int(max_no) + 1 + len(frame))

    frame.to_sql(
        "air_quality",
        con=engine,
        if_exists="append",
        index=False,
        chunksize=1000,
        method="multi",
    )


if __name__ == "__main__":
    import_dataset()
