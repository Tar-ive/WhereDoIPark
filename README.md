# Where do I park? - Texas State University

## Project Description

'Where do I park?' is a mobile-responsive web application designed for Texas State University students to report and view parking availability in campus garages. This app aims to help students save time and reduce frustration when looking for parking spots on campus.

## Features

- Real-time parking availability reporting
- View current parking status for all campus garages
- Mobile-responsive design for easy access on various devices
- Interactive map showing garage locations
- Detailed information for each parking garage
- User-friendly interface for submitting parking reports
- Admin panel for monitoring system reliability

## Technologies Used

- Backend: Python, Flask
- Database: PostgreSQL with SQLAlchemy ORM
- Frontend: HTML, CSS, JavaScript
- Mapping: Leaflet.js
- Version Control: Git

## Installation and Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-repo/where-do-i-park.git
   cd where-do-i-park
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up the environment variables:
   Create a `.env` file in the root directory and add the following:
   ```
   DATABASE_URL=postgresql://username:password@host:port/database
   ```

4. Initialize the database:
   ```
   flask db upgrade
   ```

5. Run the application:
   ```
   python main.py
   ```

The application will be available at `http://localhost:5000`.

## Usage

1. Open the application in your web browser.
2. View the map to see all parking garages on campus.
3. Click on a garage to view its details and current availability.
4. To report parking availability:
   - Select a garage
   - Choose the current availability level
   - Submit your report

## API Endpoints

- `GET /api/garages`: Retrieve all parking garages
- `GET /api/garage/<int:garage_id>`: Get details for a specific garage
- `GET /api/reports`: Get the latest availability reports for all garages
- `POST /api/report`: Submit a new availability report

## Contributing

We welcome contributions to improve 'Where do I park?'. Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Developed with ❤️ for Texas State University students
