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
    # Query all percipitation scores for the year
    precipitation_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date < '2017-08-24').filter(Measurement.date > '2016-08-23').group_by(Measurement.date).order_by(Measurement.date).all()

# Design a query to show how many stations are available in this dataset?
session.query(func.count(Station.station)).all()

# What are the most active stations? (i.e. what stations have the most rows)?
# List the stations and the counts in descending order.
session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature of the most active station?
session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.station =="USC00519281").all()

# Choose the station with the highest number of temperature observations.
# Query the last 12 months of temperature observation data for this station 
session.query(Measurement.station, func.count(Measurement.id)).\
    group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).limit(1).all()


# Perform a query to retrieve the temperature data 
temperature_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date < '2017-08-24').filter(Measurement.date > '2016-08-23').filter(Measurement.station == 'USC00519281').\
    group_by(Measurement.date).order_by(desc(Measurement.date)).all()
temperature_data



