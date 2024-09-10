from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ParkingGarage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

class AvailabilityReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    garage_id = db.Column(db.Integer, db.ForeignKey('parking_garage.id'), nullable=False)
    availability = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
