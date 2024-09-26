// app.js
const map = L.map('map').setView([29.8884, -97.9384], 15); // Texas State University coordinates

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

async function fetchGarages() {
    try {
        const response = await fetch('/api/garages');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const garages = await response.json();
        populateGarageRecords(garages);
        addGarageMarkers(garages);
        return garages;
    } catch (error) {
        console.error('Error fetching garages:', error);
        throw error;
    }
}

function populateGarageRecords(garages) {
    const garageRecordsContainer = document.getElementById('garage-records');
    garageRecordsContainer.innerHTML = '<h2>Parking Garages</h2>';

    garages.forEach(garage => {
        const garageElement = document.createElement('div');
        garageElement.classList.add('garage-record');
        garageElement.innerHTML = `
            <h3>${garage.name}</h3>
            <p><strong>Permit Types:</strong> ${garage.permit_types}</p>
            <p><strong>Clearance:</strong> ${garage.clearance || 'N/A'} ft</p>
            <p><strong>Reservation Times:</strong> ${garage.reservation_times}</p>
            <button onclick="viewGarageDetails(${garage.id})">View Details</button>
        `;
        garageRecordsContainer.appendChild(garageElement);
    });
}

async function viewGarageDetails(garageId) {
    try {
        const response = await fetch(`/api/garage/${garageId}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const garageData = await response.json();
        displayGarageDetails(garageData);
    } catch (error) {
        console.error('Error fetching garage details:', error);
    }
}

function displayGarageDetails(garageData) {
    const garageElement = document.querySelector(`.garage-record:nth-child(${garageData.id + 1})`);
    const report = garageData.latest_report;

    let detailsHTML = `
        <h3>${garageData.name}</h3>
        <p><strong>Clearance:</strong> ${garageData.clearance || 'N/A'} ft</p>
        <p><strong>Reservation Times:</strong> ${garageData.reservation_times}</p>
        <p><strong>Permit Types:</strong> ${garageData.permit_types}</p>
    `;

    if (report) {
        detailsHTML += `
            <p><strong>Availability:</strong> ${report.availability}</p>
            <p><strong>Last Updated:</strong> ${new Date(report.timestamp).toLocaleString()}</p>
        `;
    } else {
        detailsHTML += '<p>No recent reports available.</p>';
    }

    detailsHTML += `
        <button onclick="showSubmitForm(${garageData.id})">Submit Report</button>
    `;

    garageElement.innerHTML = detailsHTML;

    // Update map view
    map.setView([garageData.latitude, garageData.longitude], 18);
}

function showSubmitForm(garageId) {
    const garageElement = document.querySelector(`.garage-record:nth-child(${garageId + 1})`);
    garageElement.innerHTML += `
        <form id="submit-form-${garageId}">
            <select id="availability-${garageId}" required>
                <option value="">Select availability</option>
                <option value="empty">Empty</option>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="full">Full</option>
            </select>
            <button type="submit">Submit Report</button>
        </form>
    `;

    document.getElementById(`submit-form-${garageId}`).addEventListener('submit', (event) => {
        event.preventDefault();
        submitReport(garageId);
    });
}

async function submitReport(garageId) {
    const availability = document.getElementById(`availability-${garageId}`).value;

    if (!availability) {
        alert('Please select availability');
        return;
    }

    if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(async (position) => {
            const { latitude, longitude } = position.coords;
            try {
                const response = await fetch('/api/report', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ garage_id: garageId, availability, latitude, longitude }),
                });

                if (!response.ok) {
                    throw new Error(`Failed to submit report: ${response.status} ${response.statusText}`);
                }

                const result = await response.json();
                alert('Report submitted successfully.');
                await fetchGarages(); // Refresh all garage data
                viewGarageDetails(garageId); // Refresh the specific garage details
            } catch (error) {
                console.error('Error in report submission:', error);
                alert(`Failed to submit report: ${error.message}`);
            }
        }, (error) => {
            console.error('Geolocation error:', error);
            alert(`Unable to get your location: ${error.message}. Please enable location services.`);
        });
    } else {
        alert('Geolocation is not supported by your browser');
    }
}

function addGarageMarkers(garages) {
    garages.forEach(garage => {
        L.marker([garage.latitude, garage.longitude])
         .addTo(map)
         .bindPopup(`
            <strong>${garage.name}</strong><br>
            Clearance: ${garage.clearance || 'N/A'} ft<br>
            Reservation Times: ${garage.reservation_times}<br>
            Permit Types: ${garage.permit_types}<br>
            <button onclick="viewGarageDetails(${garage.id})">View Details</button>
         `);
    });
}

async function init() {
    try {
        const garages = await fetchGarages();
        // Update availability every 30 seconds
        setInterval(fetchGarages, 30000);
    } catch (error) {
        console.error('Error initializing app:', error);
        alert(`Failed to initialize app: ${error.message}`);
    }
}

// Start the application
init();