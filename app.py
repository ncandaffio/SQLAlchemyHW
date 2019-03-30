import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create Session
session = Session(engine)

#create flask
app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )   

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    percip = []
    for value in results:
        percip.append(value)
    return(jsonify(percip))

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Measurement.station).all()
    stations = [r for r in results]
    return(jsonify(stations))

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date).order_by(Measurement.date.desc()).limit(1)
    for r in results:
        results_dt = str(r).strip("'(),")
    max_date = dt.datetime.strptime(results_dt, '%Y-%m-%d')
    start_date = max_date - dt.timedelta(days=366)

    results = session.query(Measurement.tobs).filter(Measurement.date > start_date)
    temp = [t for t in results]
    return(jsonify(temp))

@app.route('/api/v1.0/<start>/<end>')
#@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>', defaults={'end':'2099-01-01'})
def range(start, end='2099-01-01'):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temps = {}
    for mn, avg, mx in results:
        temps['Min Temp'] = mn
        temps['Avg Temp'] = avg
        temps['Max Temp'] = mx
    return jsonify(temps)

if __name__ == '__main__':
    app.run(debug=True)