

from flask import Flask, jsonify

import datetime as dt
from datetime import datetime, date, timedelta
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import numpy as np

#################################################
# Database Set up 
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

#Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

#Home Route
@app.route("/")

def home():
    """List all available api routes."""
    
    return (
        
        f"Welcome to the Hawaii Climate App"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
              
    )   
    
@app.route("/api/v1.0/precipitation")

def precipitation():
    """Convert query results to a Dictionary using 'date' as the key and 'precipitation' as the value."""
    
    session = Session(engine)
    
    # Query all the precipitation data
    query_results = session.query(Measurement.date, Measurement.prcp).all()
    
    session.close()
    
    #Create the dictionary from the precipitation data and append to the list of all precipitation data
    precipitation_data = []
    
    for date, prcp in query_results:
        precipitation_data_dict = {}
        precipitation_data_dict["date"] = date
        precipitation_data_dict["prcp"] = prcp
        precipitation_data.append(precipitation_data_dict)
        
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")

def stations():
    
    """Return a JSON list of stations from the dataset"""
    
    session = Session(engine)
    
    all_stations = session.query(Station.name).all()
    
    session.close()
    
    #convert list into normal list
    all_stations_list = list(np.ravel(all_stations))
    
    return jsonify(all_stations_list)

@app.route("/api/v1.0/tobs")

def tobs():

    """Return a JSON list of Temperature Observations for the previous year"""
    
    session = Session(engine)

# Query for the dates and temperature observations from a year from the last data point
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    tobs_query = session.query(Measurement.tobs, Measurement.date).\
        filter(Measurement.date >= one_year_ago).\
        order_by(Measurement.date).all()
         
    session.close()
    
    tobs_data = []
    
    for date, tobs in tobs_query:
        tobs_data_dict = {}
        tobs_data_dict["date"] = date
        tobs_data_dict["tobs"] = tobs
        tobs_data.append(tobs_data_dict)
        
    return jsonify(tobs_data_dict)         
    

@app.route("/api/v1.0/<start>")

def calc_temp(start):
    
    session = Session(engine)
        
    sel = [Measurement.date,                 
                func.min(Measurement.tobs), 
                func.avg(Measurement.tobs), 
                func.max(Measurement.tobs)]
    
    results = session.query(*sel).\
                filter(Measurement.date >= start).\
                group_by(Measurement.date).all()
                
    session.close()         
     
    dates_tobs = []
    
    for min, avg, max in results:
        dates_tobs_dict = {}
        dates_tobs_dict["Min"] = min
        dates_tobs_dict["Avg"] = avg
        dates_tobs_dict["Max"] = max
        dates_tobs.append(dates_tobs_dict)
        
    return jsonify(dates_tobs)          
                    
    
@app.route("/api/v1.0/<start>/<end>")

def calc_temps(start, end):

    """Return a JSON list of TMIN, TAVG, TMAX for a list of start and end dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMin, TAvg, and TMax
    """

    session = Session(engine)
    
    start_end_tobs = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
        
    session.close()
    
    tobs_stats = []
    
    for min, avg, max in start_end_tobs:
        tobs_stats_dict = {}
        tobs_stats_dict["Min"] = min
        tobs_stats_dict["Avg"] = avg
        tobs_stats_dict["Max"] = max
        tobs_stats.append(tobs_stats_dict)
        
    return jsonify(tobs_stats)


if __name__ == "__main__":
    app.run(debug=True)
        
        
        


    
    
    
    
    
    
    
        
        
        
    
    
    
     
         
         
     
    

            
            
            
            
            
        
        
        
