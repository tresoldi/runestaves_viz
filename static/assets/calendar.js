/**
 * Calendar Detail Page - Feast table, symbol charts, mini map
 *
 * Responsibilities:
 * - Load calendar data (embedded or external JSON)
 * - Render feast table with filtering/searching
 * - Render symbol charts with D3.js
 * - Initialize mini map showing calendar location
 */

(function () {
    'use strict';

    // Private state
    let calendarData = null;
    let config = {};
    let translations = {};

    /**
     * Public API - Initialize calendar page
     */
    window.initializeCalendar = function (calendarConfig) {
        config = calendarConfig;
        translations = calendarConfig.translations;

        // TODO: Load calendar data
        loadCalendarData();
    };

    /**
     * Load calendar data (embedded or external)
     */
    function loadCalendarData() {
        // TODO: Check if data is embedded
        // if (config.embedData) {
        //     const dataElement = document.getElementById('caldata');
        //     calendarData = JSON.parse(dataElement.textContent);
        //     initializeComponents();
        // } else {
        //     // Fetch external JSON
        //     fetch(calendarDataUrl)
        //         .then(response => response.json())
        //         .then(data => {
        //             calendarData = data;
        //             initializeComponents();
        //         });
        // }

        console.log('TODO: Load calendar data');
    }

    /**
     * Initialize all page components
     */
    function initializeComponents() {
        // TODO: Initialize components
        // renderFeastTable();
        // renderSymbolCharts();
        // initializeMiniMap();
        // setupFeastFilters();

        console.log('TODO: Initialize components');
    }

    /**
     * Render feast table
     */
    function renderFeastTable() {
        // TODO: Get feast data
        // const feasts = calendarData.individual;

        // TODO: Render table rows
        // const tbody = document.getElementById('feast-table-body');
        // tbody.innerHTML = '';
        //
        // feasts.forEach(feast => {
        //     const row = document.createElement('tr');
        //     row.innerHTML = `
        //         <td>${feast.month}</td>
        //         <td>${feast.day}</td>
        //         <td>${feast.day_of_year}</td>
        //         <td>${feast.fest}</td>
        //         <td>${feast.fest_canonical || ''}</td>
        //         <td>${feast.fest_type || ''}</td>
        //         <td>${feast.rune || ''}</td>
        //         <td>${feast.notes || ''}</td>
        //     `;
        //     tbody.appendChild(row);
        // });

        console.log('TODO: Render feast table');
    }

    /**
     * Set up feast table filters
     */
    function setupFeastFilters() {
        // TODO: Month filter
        // document.getElementById('month-filter')?.addEventListener('change', filterFeastTable);

        // TODO: Search input
        // document.getElementById('feast-search')?.addEventListener('input', searchFeastTable);

        console.log('TODO: Set up feast filters');
    }

    /**
     * Filter feast table by month
     */
    function filterFeastTable() {
        // TODO: Get selected month
        // const selectedMonth = document.getElementById('month-filter').value;

        // TODO: Show/hide rows based on month
        // const rows = document.querySelectorAll('#feast-table-body tr');
        // rows.forEach(row => {
        //     const month = row.cells[0].textContent;
        //     if (!selectedMonth || month === selectedMonth) {
        //         row.style.display = '';
        //     } else {
        //         row.style.display = 'none';
        //     }
        // });

        console.log('TODO: Filter feast table');
    }

    /**
     * Search feast table by text
     */
    function searchFeastTable() {
        // TODO: Get search query
        // const query = document.getElementById('feast-search').value.toLowerCase();

        // TODO: Show/hide rows based on search
        // const rows = document.querySelectorAll('#feast-table-body tr');
        // rows.forEach(row => {
        //     const text = row.textContent.toLowerCase();
        //     if (text.includes(query)) {
        //         row.style.display = '';
        //     } else {
        //         row.style.display = 'none';
        //     }
        // });

        console.log('TODO: Search feast table');
    }

    /**
     * Render symbol charts with D3.js
     */
    function renderSymbolCharts() {
        // TODO: Render symbol type bar chart
        // renderSymbolTypeChart();

        // TODO: Render symbol category bar chart
        // renderSymbolCategoryChart();

        console.log('TODO: Render symbol charts');
    }

    /**
     * Render symbol type bar chart
     */
    function renderSymbolTypeChart() {
        // TODO: Get symbol data
        // const symbolData = calendarData.symbols.by_type;

        // TODO: Create D3 bar chart
        // const data = Object.entries(symbolData)
        //     .map(([type, count]) => ({ type, count }))
        //     .sort((a, b) => b.count - a.count)
        //     .slice(0, 10);  // Top 10
        //
        // const width = 400;
        // const height = 300;
        // const margin = { top: 20, right: 20, bottom: 60, left: 60 };
        //
        // const svg = d3.select('#symbol-type-chart')
        //     .append('svg')
        //     .attr('width', width)
        //     .attr('height', height);
        //
        // // TODO: Create scales, axes, bars

        console.log('TODO: Render symbol type chart');
    }

    /**
     * Render symbol category bar chart
     */
    function renderSymbolCategoryChart() {
        // TODO: Get category data
        // const categoryData = calendarData.symbols.by_category;

        // TODO: Create D3 bar chart (similar to type chart)

        console.log('TODO: Render symbol category chart');
    }

    /**
     * Initialize mini map showing calendar location
     */
    function initializeMiniMap() {
        // TODO: Get location coordinates
        // const location = calendarData.location;
        // if (!location.latitude || !location.longitude) {
        //     return;  // No coordinates available
        // }

        // TODO: Create Leaflet map
        // const miniMap = L.map('mini-map').setView(
        //     [location.latitude, location.longitude],
        //     10
        // );

        // TODO: Add tile layer
        // L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        //     attribution: '© OpenStreetMap contributors',
        // }).addTo(miniMap);

        // TODO: Add marker at calendar location
        // L.marker([location.latitude, location.longitude])
        //     .addTo(miniMap)
        //     .bindPopup(location.location_name);

        console.log('TODO: Initialize mini map');
    }
})();
