from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

if __name__ == '__main__':
    with app.app_context():
        # First transaction: Add new ENUM value
        with db.engine.connect() as connection:
            # Check if 'pending' is already a valid value for verification_status
            result = connection.execute(
                text("SELECT enum_range(NULL::verification_status)")).scalar()
            enum_values = result[1:-1].split(
                ',')  # Remove parentheses and split

            if 'pending' not in enum_values:
                # Add 'pending' to the ENUM type
                connection.execute(
                    text("ALTER TYPE verification_status ADD VALUE 'pending'"))
                connection.commit()
                print("Added 'pending' to verification_status ENUM")

        # Second transaction: Add new columns and update data
        with db.engine.connect() as connection:
            # Add new columns if they don't exist
            connection.execute(
                text("""
                DO $$
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                                   WHERE table_name='availability_report' AND column_name='reliability_score') THEN
                        ALTER TABLE availability_report ADD COLUMN reliability_score FLOAT;
                    END IF;

                    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                                   WHERE table_name='availability_report' AND column_name='is_flagged') THEN
                        ALTER TABLE availability_report ADD COLUMN is_flagged BOOLEAN DEFAULT FALSE;
                    END IF;
                END $$;
            """))

            # Update existing rows
            connection.execute(
                text(
                    "UPDATE availability_report SET verification_status = 'pending' WHERE verification_status IS NULL"
                ))
            connection.execute(
                text(
                    "UPDATE availability_report SET reliability_score = 1.0 WHERE reliability_score IS NULL"
                ))

            # Commit the transaction
            connection.commit()

        print("Migration completed successfully.")
