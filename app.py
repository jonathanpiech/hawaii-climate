#Imports

import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Setup database

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

#Setup Flask

app = Flask(__name__)

#Flask Routes

@app.route("/")
def home():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2010-01-01<br/>"
        f"/api/v1.0/2010-01-01/2017-08-23"
    )

#Return a dictionary of dates with precipitation measurements
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()

    session.close()

    all_dates = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_dates.append(prcp_dict)

    return jsonify(all_dates)

#Return a list of stations
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Station.station).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

#Return temperature observations of last year of data
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    results = session.query(Measurement.tobs).filter(Measurement.date > '2016-08-23').order_by(Measurement.date).all()

    session.close()

    last_year_tobs = list(np.ravel(results))

    return jsonify(last_year_tobs)

#Returns low, high, and avg temperature for the dates since given
#start_date is a date string in the %Y-%m-%d format
@app.route("/api/v1.0/<start_date>")
def calc_temps(start_date):
    
    #Check if inputs are in valid format
    try:
        dt.datetime.strptime(start_date, '%Y-%m-%d')
    except ValueError:
        return(
            f"No page exists with that URL.<br/>"
            f"If searching for temperatures over a date range, please use a date in the YYYY-MM-DD format"
        )


    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date)

    session.close()

    for temp in results:
        t_dict = {'Low Temperature': temp[0], 'High Temperature': temp[2], 'Avg Temperature': temp[1]}

    return jsonify(t_dict)



#Returns low, high, and avg temperature for the given dates inclusive
#start_date is a date string in the %Y-%m-%d format
#end_date is a date string in the %Y-%m-%d format
@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps_with_end(start_date, end_date):
    
    #Check if inputs are in valid format
    try:
        dt.datetime.strptime(start_date, '%Y-%m-%d')
    except ValueError:
        return(
            f"No page exists with that URL.<br/>"
            f"If searching for temperatures over a date range, please use a date in the YYYY-MM-DD format"
        )

    try:
        dt.datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return(
            f"No page exists with that URL.<br/>"
            f"If searching for temperatures over a date range, please use a date in the YYYY-MM-DD format"
        )

    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    session.close()

    for temp in results:
        t_dict = {'Low Temperature': temp[0], 'High Temperature': temp[2], 'Avg Temperature': temp[1]}

    return jsonify(t_dict)



if __name__ == "__main__":
    app.run(debug=True)