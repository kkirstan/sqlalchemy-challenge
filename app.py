import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

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

#Home page. List all routes that are available.
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>")


#Convert the query results to a dictionary using date as the key and prcp as the value.
#Retrun the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    last_year_prcp = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').\
        order_by(Measurement.date).all()
    
    session.close()
    
    prcp_df = []
    for date, prcp in last_year_prcp:
        prcp_df_dict = {}
        prcp_df_dict['date'] = date
        prcp_df_dict['prcp'] = prcp
        prcp_df.append(prcp_df_dict)
        
    return jsonify(prcp_df)


#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    stations = session.query(Station.station, Station.name)
    
    session.close()
    
    stations_list = []
    for station, name in stations:
        stations_dict = {}
        stations_dict['station'] = station
        stations_dict['name'] = name
        stations_list.append(stations_dict)
    
    return jsonify(stations_list)


#Query the dates and temperature observations of the most active station for the last year of data. Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    most_active = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281', Measurement.date >= '2016-08-23')
    
    session.close()
    
    most_active_list = []
    for date, tobs in most_active:
        most_active_dict = {}
        most_active_dict['date'] = date
        most_active_dict['tobs'] = tobs
        most_active_list.append(most_active_dict)
        
    return jsonify(most_active_list)


#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range. When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>")
def start_temp(start):
    session = Session(engine)
    
    results = session.query(
        Measurement.date,\
        func.min(Measurement.tobs), 
        func.avg(Measurement.tobs), 
        func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        group_by(Measurement.date).all()
    
    session.close()
    
    start_list = []
    
    for date, min, avg, max in results:
        start_dict = {}
        start_dict['Date'] = date
        start_dict['TMIN'] = min
        start_dict['TAVG'] = avg
        start_dict['TMAX'] = max
        start_list.append(start_dict)
    
    return jsonify(start_list)

#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def start_end_temp(start,end):
    session = Session(engine)
    
    results = session.query(
        Measurement.date,\
        func.min(Measurement.tobs), 
        func.avg(Measurement.tobs), 
        func.max(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).\
        group_by(Measurement.date).all()
    
    session.close()
    
    start_end_list = []
    
    for date, min, avg, max in results:
        start_end_dict = {}
        start_end_dict['Date'] = date
        start_end_dict['TMIN'] = min
        start_end_dict['TAVG'] = avg
        start_end_dict['TMAX'] = max
        start_end_list.append(start_end_dict)

    return jsonify(start_end_list)

if __name__ == '__main__':
    app.run(debug=True)
