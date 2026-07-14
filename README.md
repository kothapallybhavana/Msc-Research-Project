# Air Quality Prediction and Monitoring Web Application

## Project Overview
This project is a Flask-based web application for predicting PM2.5 air quality levels and monitoring pollution statistics from the Beijing Multi-Site Air Quality dataset. It uses MySQL for data storage, SQLAlchemy for database access, and a pre-trained machine learning model for PM2.5 prediction.

## Objectives
- Predict PM2.5 using environmental measurements
- Store every prediction in MySQL
- Load prediction history from MySQL
- Display dataset summary and pollution statistics
- Present database-driven charts on the dashboard

## Technologies Used
- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- MySQL
- PyMySQL
- Pandas
- NumPy
- Scikit-learn
- Joblib
- Plotly
- HTML5
- CSS3
- JavaScript

## Folder Structure
```text
app.py
config.py
import_dataset.py
database/
models.py
queries.py
routes/
services/
templates/
static/
migrations/
models/
csv_data/
README.md
```

## Installation
1. Create and activate a virtual environment.
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Update MySQL credentials in `config.py` if needed.

## Database Setup

Before running the migration, the user is ensuring that `config.py` contains the correct MySQL connection settings (`MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`).

Option A — Run the SQL file in MySQL Workbench (GUI):

1. Open MySQL Workbench and connect to the desired MySQL server (create a connection if required).
2. From the menu, choose `File` → `Open SQL Script...` and select `migrations/init.sql` from the repository.
3. The SQL script is opening in a new SQL editor tab. Click the lightning bolt ("Execute") button or press `Ctrl+Shift+Enter` to run the whole script.
4. Refresh the Schema / Navigator panel to confirm that `air_quality_db` and its tables (`air_quality`, `prediction_history`) have been created.

Option B — Run the SQL file from the command line (mysql client):

1. Open a terminal or command prompt on the machine that can reach the MySQL server.
2. Run the following command (replace `<user>` and `<host>` as needed):

```bash
# You will be prompted for the MySQL password
mysql -h <host> -u <user> -p < migrations/init.sql
```

3. After the script completes, connect via Workbench or the `mysql` client and verify the schema and tables exist:

```sql
USE air_quality_db;
SHOW TABLES;
```

What the script is creating

- Database: `air_quality_db`
- Table: `air_quality` (storing imported dataset rows)
- Table: `prediction_history` (storing model prediction records)

If the user needs the migration to be run programmatically (for CI or scripted setup), they are using the `mysql` command shown above or can run the SQL file using a Python DB connector or SQLAlchemy engine.

## Import Dataset
Import the Beijing Multi-Site Air Quality dataset into MySQL:
```bash
python import_dataset.py
```

This loads `csv_data/Beijing_Air_Quality_SQL.csv` into the `air_quality` table.

## Train Models
Training is not required for normal use because the repository already includes the trained model files in `models/`.

## Run Flask
```bash
python app.py
```

Then open the application in your browser.

## Features
- PM2.5 prediction using a trained machine learning model
- MySQL-backed prediction history
- Prediction history view ordered by newest first
- Prediction result status panel with safe, warning, and alert indicators
- Dataset summary cards
- Pollution statistics and environmental statistics
- Database-driven dashboard charts

## Dashboard
The dashboard displays:
- Total Records
- Total Stations
- Average PM2.5
- Average PM10
- Average pollutant statistics
- Average environmental statistics
- Historical PM2.5 Trend
- PM10 Trend
- Average Pollutants
- Station Distribution
- Monthly PM2.5
- Top 10 Highest PM2.5 Records

## Machine Learning Models
The project keeps the existing pre-trained PM2.5 prediction model and scaler artifact supplied in the repository. The model is loaded directly for inference and is not retrained during normal application use.

## Screenshots
Add project screenshots here:

- Home page
- Prediction form
- Prediction result
- Dashboard
- Prediction history

## Future Scope
- Extend the dataset import workflow for multiple data files
- Add chart export options
- Add validation tools for data quality checks
- Improve deployment packaging for production environments
