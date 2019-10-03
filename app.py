import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from datetime import timedelta, datetime

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Instructions/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return (
        f"<h1>Welcome to the Climate API!</h1></br>"
        f"<h3>Available routes:</h3></br>"
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs </br>"
        f"/api/v1.0/start </br>"
        f"/api/v1.0/start/end </br>"
    )

@app.route("/api/v1.0/precipitation")
# Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
# Return the JSON representation of your dictionary.
def get_prcp():
 # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query prepipitation
    sel = [Measurement.date, Measurement.prcp]
    results = session.query(*sel).all()

    session.close()

    # Create dictionary with date as key and prcp as value
    precipitation = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        precipitation.append(prcp_dict)
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
# Return a JSON list of stations from the dataset.
def get_stations():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    results = session.query(Station.station, Station.name).all()
    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
# query for the dates and temperature observations from a year from the last data point
# Return a JSON list of Temperature Observations (tobs) for the previous year
def get_tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query date and temperature
    last = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(last[0],"%Y-%m-%d").date()
    first_date = last_date - timedelta(365)

    sel = [Measurement.date, Measurement.prcp]
    results = session.query(*sel).filter(Measurement.date >= first_date).filter(Measurement.date <= last_date).all()
    
    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)

#@app.route("/api/v1.0/start")

#@app.route("//api/v1.0/start/end")


if __name__ == '__main__':
    app.run(debug=True)