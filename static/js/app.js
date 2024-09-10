// Initialize map
const map = L.map('map').setView([29.8884, -97.9384], 15); // Texas State University coordinates

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Fetch parking garages data
async function fetchGarages() {
    const response = await fetch('/api/garages');
    const garages = await response.json();
    return garages;
}

// Fetch availability reports
async function fetchReports() {
    const response = await fetch('/api/reports');
    const reports = await response.json();
    return reports;
}

// Add garage markers to the map
function addGarageMarkers(garages) {
    const garageSelect = document.getElementById('garage-select');
    garages.forEach(garage => {
        L.marker([garage.latitude, garage.longitude])
            .bindPopup(`<b>${garage.name}</b><br>Loading availability...`)
            .addTo(map);

        const option = document.createElement('option');
        option.value = garage.id;
        option.textContent = garage.name;
        garageSelect.appendChild(option);
    });
}

// Update garage markers with availability information
function updateGarageAvailability(reports) {
    map.eachLayer(layer => {
        if (layer instanceof L.Marker) {
            const garageReport = reports.find(report => report.garage_id === layer.garage_id);
            if (garageReport) {
                layer.setPopupContent(`<b>${layer.getPopup().getContent().split('<br>')[0]}</b><br>Availability: ${garageReport.availability}`);
            }
        }
    });
}

// Submit availability report
async function submitReport(garageId, availability, latitude, longitude) {
    const response = await fetch('/api/report', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            garage_id: garageId,
            availability: availability,
            latitude: latitude,
            longitude: longitude
        }),
    });
    return response.json();
}

// Initialize the app
async function init() {
    const garages = await fetchGarages();
    addGarageMarkers(garages);

    // Update availability every 30 seconds
    async function updateAvailability() {
        const reports = await fetchReports();
        updateGarageAvailability(reports);
    }
    updateAvailability();
    setInterval(updateAvailability, 30000);

    // Handle report submission
    document.getElementById('submit-report').addEventListener('click', async () => {
        const garageId = document.getElementById('garage-select').value;
        const availability = document.getElementById('availability-select').value;

        if (!garageId || !availability) {
            alert('Please select a garage and availability');
            return;
        }

        if ('geolocation' in navigator) {
            navigator.geolocation.getCurrentPosition(async (position) => {
                const { latitude, longitude } = position.coords;
                try {
                    await submitReport(garageId, availability, latitude, longitude);
                    alert('Report submitted successfully');
                    updateAvailability();
                } catch (error) {
                    alert('Error submitting report');
                }
            }, () => {
                alert('Unable to get your location. Please enable location services.');
            });
        } else {
            alert('Geolocation is not supported by your browser');
        }
    });
}

init();
