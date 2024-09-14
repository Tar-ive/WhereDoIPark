from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from sqlalchemy.types import TIMESTAMP
from datetime import datetime

db = SQLAlchemy()


class ParkingGarage(db.Model):
    __tablename__ = 'parking_garage'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    permit_types = db.Column(db.String(100), nullable=False)
    reservation_times = db.Column(db.String(200),
                                  nullable=False)
    clearance = db.Column(db.Float)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)


class AvailabilityReport(db.Model):
    __tablename__ = 'availability_report'
    id = db.Column(db.Integer, primary_key=True)
    garage_id = db.Column(db.Integer,
                          db.ForeignKey('parking_garage.id'),
                          nullable=False)
    availability = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(TIMESTAMP(timezone=True),
                          nullable=False,
                          default=datetime.utcnow)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    verification_status = db.Column(Enum(
        'pending', 'verified', 'rejected', name='verification_status'),
                                    nullable=False,
                                    default='pending')
    is_flagged = db.Column(db.Boolean, default=False)
