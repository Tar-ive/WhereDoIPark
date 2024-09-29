from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
database_url = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # Enable SQL query logging

print("Database URL:", database_url)

# Initialize the database
try:
    db = SQLAlchemy(app)
    print("Database connection initialized successfully.")
except Exception as e:
    print(f"Error initializing the database connection: {e}")


# Define a simple model for testing
class TestModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


@app.route('/')
def index():
    try:
        # Attempt to query the database
        result = db.session.query(TestModel).first()
        return jsonify({
            "message": "Database connection successful",
            "data": str(result)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This will create the test table if it doesn't exist
    app.run(host='0.0.0.0', port=5001, debug=True)
