// Get root colors
const root = document.documentElement;
const rootStyles = getComputedStyle(root);
const colorOne = rootStyles.getPropertyValue('--color-one').trim();
const colorTwo = rootStyles.getPropertyValue('--color-two').trim();
const colorThree = rootStyles.getPropertyValue('--color-three').trim();

let hospitals = [];
let currentPage = 1;
const itemsPerPage = 10;
let sortBy = 'name'; // Default sort attribute
let order = 'asc'; // Default order

// FETCH AND FILTER

function sortHospitals(attribute, order = 'asc') {
    return hospitals.sort((a, b) => {
        const valueA = a[attribute].toLowerCase();
        const valueB = b[attribute].toLowerCase();
        if (valueA < valueB) return order === 'asc' ? -1 : 1; // Ascending order
        if (valueA > valueB) return order === 'asc' ? 1 : -1; // Descending order
        return 0; // No change
    });
}

async function fetchHospitals() {
    try {
        const [locationsResponse, detailsResponse] = await Promise.all([
            fetch('http://localhost:8000/api/hospital_locations/?format=json'),
            fetch('http://localhost:8000/api/hospital_details/?format=json')
        ]);
        if (!locationsResponse.ok || !detailsResponse.ok) {
            throw new Error('Network response was not ok');
        }
        const locations = await locationsResponse.json();
        const details = await detailsResponse.json();
        hospitals = combineHospitalData(locations, details);

        currentPage = 1;
        hospitals = sortHospitals(sortBy, order);
        populateTable(hospitals);
        populateMap(hospitals);
    } catch (error) {
        console.error('Error fetching hospitals:', error);
    }
}

// Function to combine data from two API endpoints
function combineHospitalData(locations, details) {
    // Create a mapping of hospital details by hospital_id
    const detailsMap = {};
    details.forEach(detail => {
        detailsMap[detail.hospital] = detail; // Assuming hospital_id is the primary key
    });

    // Combine locations with their corresponding details
    return locations.map(location => {
        const hospitalDetails = detailsMap[location.hospital_id];
        
        // If details exist, combine them into the hospital object
        return hospitalDetails ? { ...location, ...hospitalDetails } : location;
    });
}

function getFilteredHospitals() {
    const filterPostalCode = document.getElementById('filter-zip').value;
    const filterCityName = document.getElementById('filter-city').value.toLowerCase();
    const filterHospitalName = document.getElementById('filter-name').value.toLowerCase();
    const filterPublic = document.getElementById('filter-public').checked;
    const filterPrivate = document.getElementById('filter-private').checked;
    const filterNonProfit = document.getElementById('filter-non-profit').checked;
    const filterEmergencyService = document.getElementById('filter-emergency-service').checked;
    const filterNoEmergencyService = document.getElementById('filter-no-emergency-service').checked;

    const bedCountRange = bedCountSlider.noUiSlider.get();
    const minBedCount = Number(bedCountRange[0]);
    const maxBedCount = Number(bedCountRange[1]);

    const filteredHospitals = hospitals.filter(hospital => {
        const containsName = hospital.name.toLowerCase().includes(filterHospitalName);
        const startsWithCity = hospital.city.toLowerCase().startsWith(filterCityName);
        const startsWithZIP = hospital.zip.startsWith(filterPostalCode);
        const isPublic = hospital.provider_type_code === 'O';
        const isPrivate = hospital.provider_type_code === 'P';
        const isNonProfit = hospital.provider_type_code === 'F';
        const hasEmergencyService = hospital.has_emergency_service === 1;
        const hasNoEmergencyService = hospital.has_emergency_service === 0;
        const matchesEmergencyService = (filterEmergencyService && hasEmergencyService) || (filterNoEmergencyService && hasNoEmergencyService) || (!filterEmergencyService && !filterNoEmergencyService);
        const matchesProviderType = (filterPublic && isPublic) || (filterPrivate && isPrivate) || (filterNonProfit && isNonProfit) || (!filterPublic && !filterPrivate && !filterNonProfit);
        const withinBedCount = hospital.bed_count >= minBedCount && hospital.bed_count <= maxBedCount;

        console.log('Hospital:', {
            name: hospital.name,
            city: hospital.city,
            zip: hospital.zip,
            provider_type_code: hospital.provider_type_code,
            has_emergency_service: hospital.has_emergency_service,
            bed_count: hospital.bed_count,
            containsName,
            startsWithCity,
            startsWithZIP,
            matchesProviderType,
            matchesEmergencyService,
            withinBedCount
        });

        return containsName && startsWithCity && startsWithZIP && matchesProviderType && matchesEmergencyService && withinBedCount;
    });

    return filteredHospitals;
}

function filterHospitals() {
    currentPage = 1;
    const filteredHospitals = getFilteredHospitals();
    populateTable(filteredHospitals);
    populateMap(filteredHospitals);
}


// MAP

// Initialize the map
const map = L.map('map', {zoomSnap: 0.1, scrollWheelZoom: false}).setView([51.35, 10.2], 5.7);

L.setOptions(map, {zoomSnap: 0.5});

// Enable scroll wheel zoom when the map is focused and Ctrl key is held
map.on('focus', function() {
    document.addEventListener('keydown', function(event) {
        if (event.ctrlKey) {
            map.scrollWheelZoom.enable();
        }
    });
    document.addEventListener('keyup', function(event) {
        if (!event.ctrlKey) {
            map.scrollWheelZoom.disable();
        }
    });
});

// Disable scroll wheel zoom when the map loses focus
map.on('blur', function() {
    map.scrollWheelZoom.disable();
});

// Load and display a tile layer (OpenStreetMap tiles)
L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

function getColorByProviderType(providerType) {
    switch (providerType) {
        case 'O':
            return colorOne;
        case 'P':
            return colorTwo;
        case 'F':
            return colorThree;
        default:
            return 'gray'; // Default color for unknown types
    }
}

function getMarkerSizeByBedCount(bedCount) {
    return Math.max(2, bedCount / 110);
}


// Function to fetch hospital data and add markers
async function populateMap(hospitals) {

    // Clear existing markers on the map (optional)
    map.eachLayer((layer) => {
        if (layer instanceof L.CircleMarker) {
            map.removeLayer(layer);
        }
    });

    const markers = []; // Array to hold markers
    hospitals.forEach(hospital => {
        const { provider_type_code, name, street, zip, city, phone, mail, latitude, longitude, bed_count, has_emergency_service } = hospital;
        const markerColor = getColorByProviderType(hospital.provider_type_code);
        const markerSize = getMarkerSizeByBedCount(bed_count);
        const circle = L.circleMarker([latitude, longitude], {
            stroke: false,
            fillColor: markerColor,
            fillOpacity: 0.7,
            radius: markerSize,
        });
        const badgeColor = getColorByProviderType(hospital.provider_type_code);
        circle.bindPopup(`
            <span style="background-color: ${badgeColor}; color: white" class="rounded-lg">&nbsp; ${translateProviderTypeCode(provider_type_code)} &nbsp;</span>
            <span class="border border-gray-600 rounded-lg">&nbsp;<span class="material-symbols-outlined text-sm" style="vertical-align: middle; position: relative; top: -1px">hotel</span> ${formatTotalTreatments(bed_count)}&nbsp;</span>
            ${has_emergency_service ? '<span class="material-symbols-outlined text-xl" style="vertical-align: middle; position: relative; top: -1px; color: #ef553b">local_hospital</span>' : '<span class="material-symbols-outlined text-xl text-neutral-300 icon-strikethrough" style="vertical-align: middle; position: relative; top: -1px;">local_hospital</span>'}
            <br><b>${name}</b>
            <br>${street}
            <br>${zip} ${city}
            <br>${phone}
            <br><a href="mailto:${mail}">${mail}</a>`);
        
        let isPopupOpenFromClick = false;
        circle.on('mouseover', function (e) {
            if (!isPopupOpenFromClick) {
                this.openPopup();
            }
        });
        circle.on('mouseout', function (e) {
            if (!isPopupOpenFromClick) {
                this.closePopup();
            }
        });
        circle.on('click', function (e) {
            isPopupOpenFromClick = true;
            this.openPopup();
        });
        map.on('click', function(e) {
            isPopupOpenFromClick = false;
            circle.closePopup();
        });

        markers.push(circle);
    });
    // Now add all markers to the map at once
    L.layerGroup(markers).addTo(map);
}


function formatTotalTreatments(num) {
    if (num >= 1e4) {
        return (num / 1e3).toFixed(0) + '&#8239;k';
    } else if (num >= 1e3) {
        return (num / 1e3).toFixed(1) + '&#8239;k';
    }
    return num.toString(); // Return the number as-is if less than 1000
}

function formatNursingQuotient(num) {
    return parseInt(num);
}

function translateProviderTypeCode(code) {
    switch (code) {
        case 'O':
            return 'Public';
        case 'P':
            return 'Private';
        case 'F':
            return 'Non-profit';
        default:
            return 'Unknown';
    }
}

// TABLE

function populateTable(hospitalsToDisplay) {
    const tableBody = document.querySelector('#hospital-table tbody');
    tableBody.innerHTML = ''; // Clear existing rows

    // Calculate the start and end index for pagination
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = Math.min(startIndex + itemsPerPage, hospitalsToDisplay.length);
    const paginatedHospitals = hospitalsToDisplay.slice(startIndex, endIndex);

    paginatedHospitals.forEach(hospital => {
        const row = document.createElement('tr');
        const badgeColor = getColorByProviderType(hospital.provider_type_code);
        row.innerHTML = `
            <td class="name-col">
                <span style="font-weight: 400"></span>${hospital.name}</span>
                <br><span style="font-weight: 300">${hospital.street}
                <br>${hospital.zip} ${hospital.city}</span>
            </td>
            <td>
                <span style="background-color: ${badgeColor}; color: white" class="rounded-lg text-xs">&nbsp; ${translateProviderTypeCode(hospital.provider_type_code)} &nbsp;</span>&thinsp;
                <span class="material-symbols-outlined text-base" style="vertical-align: middle; position: relative; top: -1px">hotel</span> ${hospital.bed_count.toLocaleString()}
                ${hospital.has_emergency_service ? '<span class="material-symbols-outlined text-xl" style="vertical-align: middle; position: relative; top: -1px; color: #ef553b">local_hospital</span>' : '<span class="material-symbols-outlined text-xl text-neutral-300 icon-strikethrough" style="vertical-align: middle; position: relative; top: -1px;">local_hospital</span>'}
                <br><span style="font-weight: 300">Total Treatments:</span> ${formatTotalTreatments(hospital.total_treatments)}
                <br><span style="font-weight: 300">Nursing Quotient:</span> ${formatNursingQuotient(hospital.nursing_quotient)}
            </td>
        `;
        tableBody.appendChild(row);
    });

    updatePaginationControls(hospitalsToDisplay.length);
}

function updatePaginationControls(totalItems) {
    const totalPages = Math.ceil(totalItems / itemsPerPage);
    document.getElementById('page-info').textContent = `Page ${currentPage} of ${totalPages}`;

    document.getElementById('prev-button').disabled = currentPage === 1;
    document.getElementById('next-button').disabled = currentPage === totalPages;
}

// Navigate to the next page
function nextPage() {
    currentPage++;
    const filteredHospitals = getFilteredHospitals();
    populateTable(filteredHospitals);
}

// Navigate to the previous page
function prevPage() {
    currentPage--;
    const filteredHospitals = getFilteredHospitals();
    populateTable(filteredHospitals);
}

// Call the function to fetch hospitals when the page loads
fetchHospitals();


// SLIDER

// Initialize the slider
const bedCountSlider = document.getElementById('bed-count-slider');
const minBedCountSpan = document.getElementById('min-bed-count');
const maxBedCountSpan = document.getElementById('max-bed-count');

// Create the noUiSlider with a range between 0 and 1000
noUiSlider.create(bedCountSlider, {
    start: [0, 1500], // Initial min and max values
    connect: true,
    range: {
        'min': 0,
        'max': 1500
    },
    step: 10, // The step value for the slider
    tooltips: false, // Show tooltips
    format: {
        to: value => Math.round(value),
        from: value => Number(value)
    }
});

// Debounce the filter function
const debouncedFilterHospitals = debounce(filterHospitals, 200);

// Update the display for min and max bed count
bedCountSlider.noUiSlider.on('update', function (values, handle) {
    minBedCountSpan.textContent = values[0];
    maxBedCountSpan.textContent = values[1];

    // Call the debounced filter function
    debouncedFilterHospitals();
});

// Debounce function to limit the rate at which a function is called
function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}
