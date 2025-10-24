/**
 * Map Page - Interactive Leaflet map with filtering
 *
 * Responsibilities:
 * - Initialize Leaflet map with OpenStreetMap tiles
 * - Load and display GeoJSON markers
 * - Implement marker clustering
 * - Handle filter UI and state management
 * - Update visible markers based on active filters
 * - Display result count
 * - Custom marker styling by period
 */

(function () {
    'use strict';

    // Private state
    let map = null;
    let markerClusterGroup = null;
    let allFeatures = [];
    let filteredFeatures = [];
    let filterState = {
        period: new Set(),
        diocese: new Set(),
        material: new Set(),
        shape: new Set(),
        symbols: new Set(),
    };
    let config = {};
    let translations = {};

    /**
     * Public API - Initialize map
     * Called from inline script in home.html
     */
    window.initializeMap = function (mapConfig) {
        config = mapConfig;
        translations = mapConfig.translations;

        // TODO: Initialize Leaflet map
        initMap();

        // TODO: Load GeoJSON data
        loadMapData();

        // TODO: Set up filter UI
        initializeFilters();

        // TODO: Set up event listeners
        setupEventListeners();
    };

    /**
     * Initialize Leaflet map instance
     */
    function initMap() {
        // TODO: Create map centered on Sweden
        // const swedenCenter = [62.0, 15.0];
        // map = L.map('map').setView(swedenCenter, 5);

        // TODO: Add OpenStreetMap tile layer
        // L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        //     attribution: '© OpenStreetMap contributors',
        //     maxZoom: 18,
        // }).addTo(map);

        // TODO: Initialize marker cluster group
        // markerClusterGroup = L.markerClusterGroup({
        //     showCoverageOnHover: false,
        //     zoomToBoundsOnClick: true,
        // });

        // TODO: Add cluster group to map
        // map.addLayer(markerClusterGroup);

        console.log('TODO: Initialize Leaflet map');
    }

    /**
     * Load GeoJSON marker data from server
     */
    function loadMapData() {
        // TODO: Fetch map_markers.geojson
        // fetch(config.dataUrl)
        //     .then(response => response.json())
        //     .then(data => {
        //         allFeatures = data.features;
        //         filteredFeatures = [...allFeatures];
        //         renderMarkers(filteredFeatures);
        //         updateResultCount();
        //         hideLoadingOverlay();
        //     })
        //     .catch(error => {
        //         console.error('Failed to load map data:', error);
        //         showErrorMessage();
        //     });

        console.log('TODO: Load GeoJSON data from:', config.dataUrl);
    }

    /**
     * Render markers on map
     */
    function renderMarkers(features) {
        // TODO: Clear existing markers
        // markerClusterGroup.clearLayers();

        // TODO: Create Leaflet markers for each feature
        // features.forEach(feature => {
        //     const marker = createMarker(feature);
        //     markerClusterGroup.addLayer(marker);
        // });

        console.log('TODO: Render', features.length, 'markers');
    }

    /**
     * Create individual marker with custom styling and popup
     */
    function createMarker(feature) {
        // TODO: Get coordinates
        // const coords = feature.geometry.coordinates;
        // const latLng = [coords[1], coords[0]];

        // TODO: Create custom icon based on period
        // const icon = createPeriodIcon(feature.properties.period_bucket_en);

        // TODO: Create marker
        // const marker = L.marker(latLng, { icon: icon });

        // TODO: Create popup content
        // const popupContent = createPopupContent(feature.properties);
        // marker.bindPopup(popupContent);

        // return marker;

        console.log('TODO: Create marker for', feature.properties.cal_id);
        return null;
    }

    /**
     * Create custom icon SVG based on period
     */
    function createPeriodIcon(period) {
        // TODO: Define period color mapping
        // const periodColors = {
        //     'Medieval': '#8b1a1a',
        //     '16th century': '#a0522d',
        //     '17th century': '#8b6f47',
        //     '18th century': '#4a5f7f',
        //     '19th century': '#2c5530',
        //     'Unknown': '#6b7280',
        // };

        // TODO: Create SVG marker icon
        // const color = periodColors[period] || periodColors['Unknown'];
        // const svgIcon = L.divIcon({
        //     html: `<svg>...</svg>`,
        //     className: 'custom-marker',
        //     iconSize: [25, 41],
        //     iconAnchor: [12, 41],
        // });

        // return svgIcon;

        console.log('TODO: Create icon for period', period);
        return null;
    }

    /**
     * Create popup HTML content for marker
     */
    function createPopupContent(properties) {
        // TODO: Build HTML string
        // const html = `
        //     <div class="marker-popup">
        //         <h3>${properties.catalog}</h3>
        //         <p class="cal-id"><code>${properties.cal_id}</code></p>
        //         <p>${properties.location_name}, ${properties.diocese_name}</p>
        //         <div class="popup-badges">
        //             <span class="badge badge-period">${properties.period_bucket}</span>
        //             <span class="badge">${properties.material_primary}</span>
        //             <span class="badge">${properties.shape}</span>
        //         </div>
        //         <a href="${properties.detail_url}" class="button">
        //             ${translations.map.view_details}
        //         </a>
        //     </div>
        // `;
        // return html;

        console.log('TODO: Create popup for', properties.cal_id);
        return '<div>Popup content</div>';
    }

    /**
     * Initialize filter UI - populate filter options
     */
    function initializeFilters() {
        // TODO: Extract unique values from features
        // const periods = [...new Set(allFeatures.map(f => f.properties.period_bucket))];
        // const dioceses = [...new Set(allFeatures.map(f => f.properties.diocese_name))];
        // const materials = [...new Set(allFeatures.map(f => f.properties.material_primary))];

        // TODO: Populate filter checkboxes/selects
        // populateFilterGroup('filter-period', periods);
        // populateFilterGroup('filter-diocese', dioceses);
        // populateFilterGroup('filter-material', materials);

        console.log('TODO: Initialize filter UI');
    }

    /**
     * Populate a filter group with options
     */
    function populateFilterGroup(containerId, values) {
        // TODO: Get container element
        // const container = document.getElementById(containerId);

        // TODO: Create checkbox for each value
        // values.forEach(value => {
        //     const label = document.createElement('label');
        //     const checkbox = document.createElement('input');
        //     checkbox.type = 'checkbox';
        //     checkbox.value = value;
        //     checkbox.addEventListener('change', onFilterChange);
        //     label.appendChild(checkbox);
        //     label.appendChild(document.createTextNode(value));
        //     container.appendChild(label);
        // });

        console.log('TODO: Populate filter', containerId, 'with', values.length, 'options');
    }

    /**
     * Handle filter change events
     */
    function onFilterChange(event) {
        // TODO: Update filterState based on checkbox changes
        // const filterType = event.target.closest('[id^="filter-"]').id.replace('filter-', '');
        // const value = event.target.value;
        // if (event.target.checked) {
        //     filterState[filterType].add(value);
        // } else {
        //     filterState[filterType].delete(value);
        // }

        console.log('TODO: Handle filter change');
    }

    /**
     * Apply filters and update map
     */
    function applyFilters() {
        // TODO: Filter features based on filterState
        // filteredFeatures = allFeatures.filter(feature => {
        //     const props = feature.properties;
        //
        //     // Period filter
        //     if (filterState.period.size > 0 &&
        //         !filterState.period.has(props.period_bucket)) {
        //         return false;
        //     }
        //
        //     // Diocese filter
        //     if (filterState.diocese.size > 0 &&
        //         !filterState.diocese.has(props.diocese_name)) {
        //         return false;
        //     }
        //
        //     // ... other filters
        //
        //     return true;
        // });

        // TODO: Re-render markers
        // renderMarkers(filteredFeatures);

        // TODO: Update result count
        // updateResultCount();

        // TODO: Update active filter chips
        // updateActiveFilters();

        console.log('TODO: Apply filters');
    }

    /**
     * Update result counter display
     */
    function updateResultCount() {
        // TODO: Update counter text
        // document.getElementById('visible-count').textContent = filteredFeatures.length;
        // document.getElementById('total-count').textContent = allFeatures.length;

        console.log('TODO: Update result count');
    }

    /**
     * Update active filter chips display
     */
    function updateActiveFilters() {
        // TODO: Show/hide active filters section
        // TODO: Create chip for each active filter
        // TODO: Add remove button to each chip

        console.log('TODO: Update active filter chips');
    }

    /**
     * Clear all filters
     */
    function clearFilters() {
        // TODO: Reset filterState
        // filterState = {
        //     period: new Set(),
        //     diocese: new Set(),
        //     material: new Set(),
        //     shape: new Set(),
        //     symbols: new Set(),
        // };

        // TODO: Uncheck all checkboxes
        // document.querySelectorAll('.filter-group input[type="checkbox"]')
        //     .forEach(cb => cb.checked = false);

        // TODO: Apply filters (shows all)
        // applyFilters();

        console.log('TODO: Clear all filters');
    }

    /**
     * Set up event listeners for UI controls
     */
    function setupEventListeners() {
        // TODO: Filter toggle button (mobile)
        // document.getElementById('toggle-filters')?.addEventListener('click', toggleFilters);

        // TODO: Apply filters button
        // document.getElementById('apply-filters')?.addEventListener('click', applyFilters);

        // TODO: Reset filters button
        // document.getElementById('reset-filters')?.addEventListener('click', clearFilters);

        // TODO: Clear filters button (in active chips)
        // document.getElementById('clear-filters')?.addEventListener('click', clearFilters);

        console.log('TODO: Set up event listeners');
    }

    /**
     * Toggle filter sidebar visibility (mobile)
     */
    function toggleFilters() {
        // TODO: Toggle sidebar class
        // const sidebar = document.getElementById('filter-sidebar');
        // sidebar.classList.toggle('active');

        console.log('TODO: Toggle filters');
    }

    /**
     * Hide loading overlay
     */
    function hideLoadingOverlay() {
        // TODO: Hide loading indicator
        // document.getElementById('map-loading').style.display = 'none';

        console.log('TODO: Hide loading overlay');
    }

    /**
     * Show error message
     */
    function showErrorMessage() {
        // TODO: Display user-friendly error
        console.error('TODO: Show error message');
    }
})();
