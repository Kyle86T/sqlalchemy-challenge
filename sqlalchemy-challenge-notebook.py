#Import Dependancies
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
#Create engine and start the automap
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
#Automap measurements and stations data
Measurement = Base.classes.measurement
Station = Base.classes.station
#Start flask
app = Flask(__name__)
#App route for homepage
@app.route("/")
def Homepage():
    """List all available api routes."""
    return (
        f"List of Available Routes: <br/>"
        f"1. Precipitation: /api/v1.0/precipitation<br/>"
        f"2. List of Stations: /api/v1.0/stations<br/>"
        f"3. Temperature for one year: /api/v1.0/tobs<br/>"
        f"4. Temperature stats from the start date(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>"
        f"5. Temperature stats from start to end dates(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )
#App route for #1
@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    result = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
#Create an empty dictionary, and append with queried results
    precipitation = []
    for date, prcp in result:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        precipitation.append(prcp_dict)
#Return the queried results in jsonified version
    return jsonify(precipitation)

#App route for #2
@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    queryresult = session.query(Station.station, Station.name).all()
    session.close()
#Create an empty dictionary, and append with queried results
    stations = []
    for station,name,lat,lon,el in queryresult:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        stations.append(station_dict)
#Return the queried results in jsonified version
    return jsonify(stations)

#App route for #3
@app.route('/api/v1.0/tobs')
def temp_observation():
    session = Session(engine)
    latest_date_str = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    latestdate = dt.datetime.strptime(latest_date_str, '%Y-%m-%d')
    querydate = dt.date(latestdate.year -1, latestdate.month, latestdate.day)
    queryresult = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= querydate).all()
    session.close()
#Create an empty dictionary, and append with queried results
    tobs_all = []
    for date, tobs in queryresult:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        tobs_all.append(tobs_dict)
#Return the queried results in jsonified version
    return jsonify(tobs_all)

#App route for #4
@app.route("/api/v1.0/min_max_avg/<start>")
def start(start):
    # create session link
    session = Session(engine)
    # take any date and convert to yyyy-mm-dd format for the query
    start_dt = dt.datetime.strptime(start, '%Y-%m-%d')
    # query data for the start date value
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_dt).all()

    session.close()

    # Create a list to hold results
    tobs_all = []
    for result in results:
        tobs_dict = {}
        tobs_dict["StartDate"] = start_dt
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobs_all.append(tobs_dict)

    # jsonify the result
    return jsonify(temps_list)

#App route for #5
@app.route('/api/v1.0/<start>/<stop>')
def temp_start_stop(start,stop):
    session = Session(engine)
    queryresult = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= stop).all()
    session.close()
#Create an empty dictionary, and append with queried results
    tobs_all = []
    for min,avg,max in queryresult:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobs_all.append(tobs_dict)
#Return the queried results in jsonified version
    return jsonify(tobs_all)

if __name__ == '__main__':
    app.run(debug=True)