#importing stuff i need 
import numpy as np
import sqlalchemy
import pandas as pd
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#database setup
engine = create_engine("sqlite:///resources/hawaii.sqlite")
Base=automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurement=Base.classes.measurement
Station=Base.classes.station

#flask setup
app=Flask(__name__)


#flask routes
@app.route('/')
def welcome():
    """List all available api routes"""
    return(
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs'
    )
@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    qu_date_prcp=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date<'2017-08-23').filter(Measurement.date>'2016-08-23').order_by(Measurement.date).all()
    date_prcp_df=pd.DataFrame(qu_date_prcp, columns=['Date','Precipitation'])
    #
    session.close()

    station_prcp=[]
    for date, prcp in qu_date_prcp:
        station_dict={}
        station_dict['date']= date
        station_dict['prcp']= prcp
        station_prcp.append(station_dict)

    return jsonify(station_prcp)

@app.route('/api/v1.0/station')
def station():
    session = Session(engine)
    stations=session.query(Measurement.station)
    

if __name__ == "__main__":
    app.run(debug=True)
