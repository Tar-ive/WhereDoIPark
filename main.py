from flask import Flask, render_template, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from sqlalchemy.types import TIMESTAMP
from flask_migrate import Migrate
import os
import traceback

# Create the Flask app
app = Flask(__name__)

# Database configuration
database_url = os.environ.get('DATABASE_URL')
if not database_url:
    raise ValueError("No DATABASE_URL set for Flask application.")

# Configure the app
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # Enable SQL query logging

print("Database URL:", database_url)

# Initialize the database
db = SQLAlchemy()

# Initialize the app with SQLAlchemy
db.init_app(app)

migrate = Migrate(app, db)
print("Database connection initialized successfully.")

# Import models here
from models import ParkingGarage, AvailabilityReport

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/api/garages', methods=['GET'])
def get_garages():
    try:
        garages = ParkingGarage.query.all()
        return jsonify([{
            'id': garage.id,
            'name': garage.name,
            'latitude': garage.latitude,
            'longitude': garage.longitude,
            'clearance': garage.clearance,
            'reservation_times': garage.reservation_times,
            'permit_types': garage.permit_types
        } for garage in garages])
    except Exception as e:
        current_app.logger.error(f"Error fetching garages: {str(e)}")
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error':
                        'An error occurred while fetching garages'}), 500

@app.route('/api/report', methods=['POST'])
def submit_report():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        garage_id = data.get('garage_id')
        availability = data.get('availability')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if not all([garage_id, availability, latitude, longitude]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Check if garage exists
        if not ParkingGarage.query.get(garage_id):
            return jsonify({'error': 'Garage not found'}), 404

        # Use UTC time for storing in the database
        utc_now = datetime.now(timezone.utc)

        # Create a new report
        new_report = AvailabilityReport(
            garage_id=garage_id,
            availability=availability,
            latitude=latitude,
            longitude=longitude,
            timestamp=utc_now,
            verification_status='pending',
            is_flagged=False
        )
        db.session.add(new_report)
        db.session.commit()

        return jsonify({
            'message': 'Report submitted successfully',
            'report_id': new_report.id,
            'timestamp': utc_now.isoformat()
        }), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error submitting report: {str(e)}")
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify(
            {'error': 'An error occurred while submitting the report'}), 500

@app.route('/api/reports', methods=['GET'])
def get_reports():
    try:
        # Subquery to get the latest report for each garage
        latest_reports = db.session.query(
            AvailabilityReport.garage_id,
            func.max(AvailabilityReport.timestamp).label('max_timestamp')
        ).group_by(AvailabilityReport.garage_id).subquery()

        # Query to join the latest reports with the full report details
        reports = db.session.query(AvailabilityReport).join(
            latest_reports,
            db.and_(
                AvailabilityReport.garage_id == latest_reports.c.garage_id,
                AvailabilityReport.timestamp == latest_reports.c.max_timestamp
            )
        ).all()

        return jsonify([{
            'id': report.id,
            'garage_id': report.garage_id,
            'availability': report.availability,
            'timestamp': report.timestamp.isoformat(),
            'latitude': report.latitude,
            'longitude': report.longitude,
            'verification_status': report.verification_status,
            'is_flagged': report.is_flagged
        } for report in reports])
    except Exception as e:
        current_app.logger.error(f"Error fetching reports: {str(e)}")
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': 'An error occurred while fetching reports'}), 500

@app.route('/api/garage/<int:garage_id>', methods=['GET'])
def get_garage(garage_id):
    try:
        garage = ParkingGarage.query.get(garage_id)
        if not garage:
            return jsonify({'error': 'Garage not found'}), 404

        latest_report = AvailabilityReport.query.filter_by(garage_id=garage_id).order_by(AvailabilityReport.timestamp.desc()).first()

        garage_data = {
            'id': garage.id,
            'name': garage.name,
            'latitude': garage.latitude,
            'longitude': garage.longitude,
            'clearance': garage.clearance,
            'reservation_times': garage.reservation_times,
            'permit_types': garage.permit_types,
            'latest_report': None
        }

        if latest_report:
            garage_data['latest_report'] = {
                'id': latest_report.id,
                'availability': latest_report.availability,
                'timestamp': latest_report.timestamp.isoformat(),
                'verification_status': latest_report.verification_status,
                'is_flagged': latest_report.is_flagged
            }

        return jsonify(garage_data)
    except Exception as e:
        current_app.logger.error(f"Error fetching garage details: {str(e)}")
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': 'An error occurred while fetching garage details'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This will create all tables defined in your models
    app.run(host='0.0.0.0', port=5000, debug=True)
