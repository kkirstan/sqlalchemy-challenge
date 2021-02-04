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

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

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

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    most_active = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281')
    
    session.close()
    
    most_active_list = []
    for date, tobs in most_active:
        most_active_dict = {}
        most_active_dict['date'] = date
        most_active_dict['tobs'] = tobs
        most_active_list.append(most_active_dict)
        
    return jsonify(most_active_list)

@app.route("/api/v1.0/<start>")
def start():
    

@app.route("/api/v1.0/<start>/<end>")
def end():

if __name__ == '__main__':
    app.run(debug=True)
