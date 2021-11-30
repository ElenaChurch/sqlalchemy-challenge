#importing stuff i need 
import numpy as np
import sqlalchemy
import pandas as pd
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import json

#database setup
engine = create_engine("sqlite:///resources/hawaii.sqlite")
Base=automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurement=Base.classes.measurement
Station=Base.classes.station
session = Session(engine)

#flask setup
app=Flask(__name__)


#flask routes
@app.route('/')
def welcome():
    """List all available api routes"""
    return(
        '<h1>Available routes:</h1>'
        f'<ul><li>/api/v1.0/precipitation</li>'
        f'<li>/api/v1.0/stations</li>'
        f'<li>/api/v1.0/tobs</li>'
        f'<li>/api/v1.0/</li>'
        f'<li>/api/v1.0//</li></ul>'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    qu_date_prcp=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date<'2017-08-23').filter(Measurement.date>'2016-08-23').order_by(Measurement.date).all()
    date_prcp_df=pd.DataFrame(qu_date_prcp, columns=['Date','Precipitation'])

    station_prcp=[]
    for date, prcp in qu_date_prcp:
        station_dict={}
        station_dict['date']= date
        station_dict['prcp']= prcp
        station_prcp.append(station_dict)

    return jsonify(station_prcp)

@app.route('/api/v1.0/stations')
def station():
    stations=session.query(Station.station,Station.name).all()
    return { id:location for id,location in stations }

@app.route('/api/v1.0/tobs')
def activestation():
    tobUSC00519281=session.query(Measurement.tobs,Measurement.date).\
    filter(Measurement.station=='USC00519281').\
    filter(Measurement.date<'2017-08-23').\
    filter(Measurement.date>'2016-08-23').all()
    
    mostactivestation=[]
    for tobs, date in tobUSC00519281:
        active_dict={}
        active_dict['Date']=date
        active_dict['tobs']=tobs
        mostactivestation.append(active_dict)
    
    return jsonify(mostactivestation)

@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def tobs(start, end='2017-08-23'):
    session = Session(engine)
    res=session.query(func.min(Measurement.tobs),
    func.max(Measurement.tobs),
    func.avg(Measurement.tobs)).filter((Measurement.date>=start)&
    (Measurement.date<=end)).all()
    tobs_list = list(np.ravel(res))
    return jsonify(tobs_list)

if __name__ == "__main__":
    app.run(debug=True)
