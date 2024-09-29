import os
import traceback
from main import app, db, ParkingGarage 

# Corrected Parking data to populate the database
parking_data = [
    {
        'name': 'Pleasant Garage (R5)',
        'permit_types': 'Red/Restricted',
        'reservation_times': '7 a.m. until 5 p.m. Monday through Friday',
        'clearance': 7.3,
        'latitude': 29.890113,
        'longitude': -97.940727
    },
    {
        'name': 'Matthews St. Garage (R46)',
        'permit_types': 'Red/Restricted & Residence Hall',
        'reservation_times':
        'Levels 1 and 2: 7 a.m. until 5 p.m., Monday through Friday. Level 3 and above: Resident Hall permits',
        'clearance': 8.2,
        'latitude': 29.890060,
        'longitude': -97.944266
    },
    {
        'name': 'Jackson (204)',
        'permit_types': 'Red',
        'reservation_times': '7 a.m. until 5 p.m. Monday through Friday',
        'clearance': None,
        'latitude': 29.890276,
        'longitude': -97.944796
    },
    {
        'name': 'Speck Garage (306)',
        'permit_types': 'Red/Green',
        'reservation_times': '24/7',
        'clearance': 7.0,
        'latitude':
        29.890605,  # Corrected latitude from 229.890605 to 29.890605
        'longitude': -97.953046
    },
    {
        'name': 'Blanco Garage (303)',
        'permit_types': 'Red/Green',
        'reservation_times': '24/7',
        'clearance': 7.0,
        'latitude': 29.887209,
        'longitude': -97.952759
    },
    {
        'name': 'Academy St. Garage (304)',
        'permit_types': 'Red/Green',
        'reservation_times': '24/7',
        'clearance': 7.0,
        'latitude': 29.8920,
        'longitude': -97.9460
    },
    {
        'name': 'Education',
        'permit_types': 'Red',
        'reservation_times': '24/7',
        'clearance': 7.0,
        'latitude': 29.887253,
        'longitude': -97.938516
    },
    {
        'name': 'Lindsey St Lot (115)',
        'permit_types': 'Red',
        'reservation_times': '7 a.m. until 5 p.m. Monday through Friday',
        'clearance': None,
        'latitude': 29.886485,
        'longitude': -97.945891
    },
    {
        'name': 'Woods Parking Garage',
        'permit_types': 'Red/Green',
        'reservation_times': '24/7',
        'clearance': 7.0,  # Used 7.0 as a representative clearance value
        'latitude': 29.887424,
        'longitude': -97.943940
    },
    {
        'name': 'Cypress Garage (CYPN)',
        'permit_types': 'Red/Green',
        'reservation_times': '24/7',
        'clearance': 7.0,
        'latitude': 29.885704,
        'longitude': -97.943778
    },
    {
        'name': 'San Jacinto Hall (112)',
        'permit_types': 'Red',
        'reservation_times': '7 a.m. until 5 p.m. Monday through Friday',
        'clearance': None,
        'latitude': 29.887011,
        'longitude': -97.943961
    },
    {
        'name': 'Tower Garage (106)',
        'permit_types': 'Red/Green',
        'reservation_times': '24/7',
        'clearance': 7.0,
        'latitude': 29.887038,
        'longitude': -97.942647
    },
    {
        'name': 'Edward Gary Residential',
        'permit_types': 'Residential',
        'reservation_times': '24/7',
        'clearance': None,
        'latitude': 29.885955,
        'longitude': -97.939669
    },
    {
        'name': 'Bobcat Stadium East (P10E)',
        'permit_types': 'Red',
        'reservation_times': '7 a.m. until 5 p.m. Monday through Friday',
        'clearance': None,
        'latitude': 29.891118,
        'longitude': -97.924026
    },
    {
        'name': 'Pay-by-App Bobcat Stadium West',
        'permit_types': 'Pay-by-App',
        'reservation_times': '24/7',
        'clearance': None,
        'latitude': 29.889062,
        'longitude': -97.926692
    },
    {
        'name': 'Strahan Lot (P8)',
        'permit_types': 'Red',
        'reservation_times': '7 a.m. until 5 p.m. Monday through Friday',
        'clearance': None,
        'latitude': 29.888081,
        'longitude': -97.931430
    },
    {
        'name': 'Sewell North (P14)',
        'permit_types': 'Red',
        'reservation_times': '7 a.m. until 5 p.m. Monday through Friday',
        'clearance': None,
        'latitude': 29.889462,
        'longitude': -97.933250
    }
]


def populate_parking_garages():
    with app.app_context():
        try:
            # Print the database URL for verification
            database_url = app.config['SQLALCHEMY_DATABASE_URI']
            print(f"Using database URL: {database_url}")

            # Create tables if they don't exist
            db.create_all()
            print("Tables created successfully.")

            # Clear existing data (optional)
            num_deleted = db.session.query(ParkingGarage).delete()
            db.session.commit()
            print(
                f"Deleted {num_deleted} existing records from ParkingGarage.")

            # Insert parking data
            for garage in parking_data:
                print(f"Inserting garage: {garage['name']}")
                new_garage = ParkingGarage(
                    name=garage['name'],
                    permit_types=garage['permit_types'],
                    reservation_times=garage['reservation_times'],
                    clearance=garage['clearance'],
                    latitude=garage['latitude'],
                    longitude=garage['longitude'])
                db.session.add(new_garage)
            db.session.commit()
            print("Parking garages populated successfully.")
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")
            traceback.print_exc()


if __name__ == '__main__':
    populate_parking_garages()
