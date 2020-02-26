# hawaii-climate

## Summary
This repository contains a SQL database with precipitation and weather station data. The csvs contain the same data as in the database. The Jupyter notebook contains code analyzing the amount of rain by date and the most active stations by number of observations. 

![alt-text](https://raw.githubusercontent.com/jonathanpiech/hawaii-climate/master/precip.png "precipitation")
![alt-text](https://raw.githubusercontent.com/jonathanpiech/hawaii-climate/master/station.png "stations")

The other part of the repository is a flask app that uses SQLAlchemy to query the database and returns a JSON depending on the endpoint.

## Requirements
The flask app require the following Python modules: numpy, sqlalchemy, datetime, flask. Use `python3 app.py` to run locally.