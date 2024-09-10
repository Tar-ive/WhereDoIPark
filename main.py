from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, ParkingGarage, AvailabilityReport
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/garages', methods=['GET'])
def get_garages():
    garages = ParkingGarage.query.all()
    return jsonify([{
        'id': garage.id,
        'name': garage.name,
        'latitude': garage.latitude,
        'longitude': garage.longitude
    } for garage in garages])

@app.route('/api/reports', methods=['GET'])
def get_reports():
    # Get reports from the last 30 minutes
    time_threshold = datetime.utcnow() - timedelta(minutes=30)
    reports = AvailabilityReport.query.filter(AvailabilityReport.timestamp > time_threshold).all()
    return jsonify([{
        'garage_id': report.garage_id,
        'availability': report.availability,
        'timestamp': report.timestamp.isoformat()
    } for report in reports])

@app.route('/api/report', methods=['POST'])
def submit_report():
    data = request.json
    new_report = AvailabilityReport(
        garage_id=data['garage_id'],
        availability=data['availability'],
        latitude=data['latitude'],
        longitude=data['longitude']
    )
    db.session.add(new_report)
    db.session.commit()
    return jsonify({'message': 'Report submitted successfully'}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
