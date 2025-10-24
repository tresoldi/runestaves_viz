/**
 * Browse Page - Card grid view with filtering and pagination
 *
 * Responsibilities:
 * - Load calendar data from GeoJSON
 * - Render calendar cards in grid layout
 * - Implement filtering (shared with map page)
 * - Implement client-side pagination
 * - Handle sorting (catalog, period, diocese)
 */

(function () {
    'use strict';

    // Private state
    let allCalendars = [];
    let filteredCalendars = [];
    let currentPage = 1;
    let itemsPerPage = 48;
    let sortBy = 'catalog';
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
     * Public API - Initialize browse page
     */
    window.initializeBrowse = function (browseConfig) {
        config = browseConfig;
        translations = browseConfig.translations;

        // TODO: Load calendar data
        loadCalendarData();

        // TODO: Initialize filters
        initializeFilters();

        // TODO: Set up event listeners
        setupEventListeners();
    };

    /**
     * Load calendar data from GeoJSON
     */
    function loadCalendarData() {
        // TODO: Fetch map_markers.geojson (same as map page)
        // fetch(config.dataUrl)
        //     .then(response => response.json())
        //     .then(data => {
        //         allCalendars = data.features;
        //         filteredCalendars = [...allCalendars];
        //         renderCalendars();
        //         updateResultCount();
        //     });

        console.log('TODO: Load calendar data from:', config.dataUrl);
    }

    /**
     * Render calendar cards with pagination
     */
    function renderCalendars() {
        // TODO: Sort calendars
        // sortCalendars();

        // TODO: Paginate
        // const start = (currentPage - 1) * itemsPerPage;
        // const end = start + itemsPerPage;
        // const pageCalendars = filteredCalendars.slice(start, end);

        // TODO: Render cards
        // const grid = document.getElementById('calendar-grid');
        // grid.innerHTML = '';
        // pageCalendars.forEach(feature => {
        //     const card = createCalendarCard(feature.properties);
        //     grid.appendChild(card);
        // });

        // TODO: Render pagination controls
        // renderPagination();

        console.log('TODO: Render calendars');
    }

    /**
     * Create calendar card element
     */
    function createCalendarCard(properties) {
        // TODO: Create card HTML
        // const card = document.createElement('div');
        // card.className = 'calendar-card';
        // card.innerHTML = `
        //     <h3>${properties.catalog}</h3>
        //     <p class="cal-id"><code>${properties.cal_id}</code></p>
        //     <p>${properties.location_name}, ${properties.diocese_name}</p>
        //     <div class="calendar-badges">
        //         <span class="badge badge-period">${properties.period_bucket}</span>
        //         <span class="badge">${properties.material_primary}</span>
        //         <span class="badge">${properties.shape}</span>
        //     </div>
        //     <div class="symbol-hints">
        //         ${createSymbolHints(properties)}
        //     </div>
        //     <a href="${properties.detail_url}" class="button">
        //         ${translations.browse.view_calendar}
        //     </a>
        // `;
        // return card;

        console.log('TODO: Create card for', properties?.cal_id);
        return document.createElement('div');
    }

    /**
     * Create symbol category hints (show up to 3)
     */
    function createSymbolHints(properties) {
        // TODO: Find which symbol categories are present
        // const categories = [];
        // const categoryKeys = Object.keys(properties).filter(k => k.startsWith('has_'));
        // categoryKeys.forEach(key => {
        //     if (properties[key] && categories.length < 3) {
        //         const category = key.replace('has_', '');
        //         categories.push(translations.symbol_categories[category]);
        //     }
        // });
        //
        // return categories.map(cat =>
        //     `<span class="badge badge-symbol">${cat}</span>`
        // ).join('');

        console.log('TODO: Create symbol hints');
        return '';
    }

    /**
     * Sort calendars by current sort criterion
     */
    function sortCalendars() {
        // TODO: Implement sorting
        // filteredCalendars.sort((a, b) => {
        //     const propsA = a.properties;
        //     const propsB = b.properties;
        //
        //     switch (sortBy) {
        //         case 'catalog':
        //             return propsA.catalog.localeCompare(propsB.catalog);
        //         case 'period':
        //             return comparePeriods(propsA.year_min, propsB.year_min);
        //         case 'diocese':
        //             return propsA.diocese_name.localeCompare(propsB.diocese_name);
        //         default:
        //             return 0;
        //     }
        // });

        console.log('TODO: Sort calendars by', sortBy);
    }

    /**
     * Render pagination controls
     */
    function renderPagination() {
        // TODO: Calculate page count
        // const pageCount = Math.ceil(filteredCalendars.length / itemsPerPage);

        // TODO: Create pagination buttons
        // const pagination = document.getElementById('pagination');
        // pagination.innerHTML = '';
        //
        // // Previous button
        // const prevBtn = document.createElement('button');
        // prevBtn.textContent = '←';
        // prevBtn.disabled = currentPage === 1;
        // prevBtn.addEventListener('click', () => goToPage(currentPage - 1));
        // pagination.appendChild(prevBtn);
        //
        // // Page numbers
        // for (let i = 1; i <= pageCount; i++) {
        //     const btn = document.createElement('button');
        //     btn.textContent = i;
        //     btn.classList.toggle('active', i === currentPage);
        //     btn.addEventListener('click', () => goToPage(i));
        //     pagination.appendChild(btn);
        // }
        //
        // // Next button
        // const nextBtn = document.createElement('button');
        // nextBtn.textContent = '→';
        // nextBtn.disabled = currentPage === pageCount;
        // nextBtn.addEventListener('click', () => goToPage(currentPage + 1));
        // pagination.appendChild(nextBtn);

        console.log('TODO: Render pagination');
    }

    /**
     * Navigate to specific page
     */
    function goToPage(page) {
        // TODO: Update current page
        // currentPage = page;

        // TODO: Re-render calendars
        // renderCalendars();

        // TODO: Scroll to top
        // window.scrollTo({ top: 0, behavior: 'smooth' });

        console.log('TODO: Go to page', page);
    }

    /**
     * Initialize filter UI
     */
    function initializeFilters() {
        // TODO: Same as map.js - extract unique values and populate
        console.log('TODO: Initialize filters');
    }

    /**
     * Apply filters
     */
    function applyFilters() {
        // TODO: Filter calendars based on filterState
        // filteredCalendars = allCalendars.filter(feature => {
        //     // Same logic as map.js
        //     return true;
        // });

        // TODO: Reset to page 1
        // currentPage = 1;

        // TODO: Re-render
        // renderCalendars();
        // updateResultCount();

        console.log('TODO: Apply filters');
    }

    /**
     * Update result counter
     */
    function updateResultCount() {
        // TODO: Update counter display
        console.log('TODO: Update result count');
    }

    /**
     * Handle sort change
     */
    function onSortChange(event) {
        // TODO: Update sortBy from select value
        // sortBy = event.target.value;

        // TODO: Re-render
        // renderCalendars();

        console.log('TODO: Handle sort change');
    }

    /**
     * Set up event listeners
     */
    function setupEventListeners() {
        // TODO: Sort select
        // document.getElementById('sort-select')?.addEventListener('change', onSortChange);

        // TODO: Filter controls (same as map page)

        // TODO: Toggle filters button (mobile)

        console.log('TODO: Set up event listeners');
    }
})();
