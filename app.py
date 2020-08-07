#Import Dependencies
import numpy as np
import pandas as pd
import datetime as dt


# Reflect Tables into SQLAlchemy ORM

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date/<start_date><br/>"
        f"/api/v1.0/start_date/end_date/<start_date>/<end_date>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
 """Return a dictionary of all percipitation scores for the previous year"""
    # Calculate the date 1 year ago from last date in database
    last_y = dt.date(2017, 8,23) - dt.timedelta(days=365)

    # Query for the date and precipitation for the last year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= last_y).all()

    # Dict
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)


@app.route("/api/v1.0/stations")
    def stations():
        """Retun a list of station."""
        results = session.query(Station).all()

        # Unravel Results
        stations = list(np.ravel(results))
        return jsonify(stations)


@app.route("api/v1.0/tobs")
def tobs():
    """Retun the temperature observations (tobs) for previous year.""" 
    # Calculate the date 1 year ago from last date in database
    last_y = dt.date(2017, 8,23) - dt.timedelta(days=365)

    # Query_date  is "2016-08-23" for the last year query
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= last_y).all()

    # Unravel Results
    temps = list(np.ravel(results))
    return jsonify(temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""

    # Select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        # Calculate TMIN, TAVG, TMAX for dates > start
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()

        # Unravel Results
        temps = list(np.ravel(results))
        return jsonify(temps)


        # Calculate TMIN, TAVG, TMAX with start and stop
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()

        # Unravel Results
        temps = list(np.ravel(results))
        return jsonify(temps)

if __name__ == '__main__':
    app.run()