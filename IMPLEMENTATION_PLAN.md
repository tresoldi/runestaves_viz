# Implementation Plan & Status

## Project Overview

This document tracks the implementation status of the Runestaves Visualization project—a static, bilingual web interface for exploring Swedish runestave calendars.

**Last Updated:** 2025-10-22
**Current Version:** 0.1.0 (Development)

---

## ✅ Completed Components

### 1. Project Infrastructure

- [x] Directory structure created
- [x] `.gitignore` configured
- [x] `VERSION` file
- [x] `requirements.txt` with all Python dependencies
- [x] `Makefile` with comprehensive build targets
- [x] Virtual environment setup instructions

**Files Created:**

```
/
├── Makefile
├── requirements.txt
├── VERSION
├── .gitignore
└── README.md
```

---

### 2. Data Validation System

- [x] Pandera schemas for all TSV files
- [x] Validation script with strict/graceful modes
- [x] Referential integrity checking
- [x] Period bucket definitions
- [x] Symbol category constants

**Files Created:**

```
scripts/
├── schemas.py           # Pandera schemas for validation
└── validate_data.py     # Data validation CLI
```

**Key Features:**

- Validates `inventory.tsv`, `individual.tsv`, `gazetteer.tsv`, `symbol_instances.tsv`
- Checks foreign key relationships
- Reports missing coordinates and orphaned records
- Configurable strictness (warnings vs. errors)

---

### 3. Data Preparation Pipeline

- [x] GeoJSON generation for map markers
- [x] Search index generation
- [x] Global statistics aggregation
- [x] Per-calendar JSON generation
- [x] Symbol category computation
- [x] Year range parsing and period assignment
- [x] Location precision tracking

**Files Created:**

```
scripts/
└── prepare_data.py      # Transform TSVs → JSON/GeoJSON
```

**Output Files Generated:**

```
site/data/
├── map_markers.geojson        # All calendars with coordinates
├── search_docs.json           # Compact search index
├── stats.json                 # Global statistics
├── calendar_index.json        # Metadata about calendar files
└── calendars/
    └── {cal_id}.json          # Per-calendar data (if > 30KB)
```

---

### 4. Bilingual Translation System

- [x] Swedish UI strings (`i18n/sv.json`)
- [x] English UI strings (`i18n/en.json`)
- [x] Swedish markdown content (methods, about)
- [x] English markdown content (methods, about)
- [x] Translation loading in build system
- [x] Language-specific period and category labels

**Files Created:**

```
i18n/
├── sv.json              # Swedish translations
├── en.json              # English translations
├── sv/
│   ├── methods.md
│   └── about.md
└── en/
    ├── methods.md
    └── about.md
```

---

### 5. Template System

- [x] Base template with header/footer
- [x] Home page (map view)
- [x] Browse page (card grid)
- [x] Calendar detail page
- [x] Methods page
- [x] About page
- [x] Data/citation page
- [x] Bilingual URL routing
- [x] Language switcher links

**Files Created:**

```
templates/
├── base.html
├── home.html
├── browse.html
├── calendar.html
├── methods.html
├── about.html
└── data.html
```

**URL Structure:**

| Swedish (/) | English (/en) | Template |
|-------------|---------------|----------|
| `/` | `/en/` | `home.html` |
| `/bladdra/` | `/en/browse/` | `browse.html` |
| `/kalendrar/{id}.html` | `/en/calendars/{id}.html` | `calendar.html` |
| `/metod/` | `/en/methods/` | `methods.html` |
| `/om/` | `/en/about/` | `about.html` |
| `/data/` | `/en/data/` | `data.html` |

---

### 6. Site Build System

- [x] Jinja2 environment setup
- [x] Markdown rendering for content pages
- [x] Bilingual page generation
- [x] Context variable assembly
- [x] Asset copying
- [x] `.nojekyll` file creation

**Files Created:**

```
scripts/
└── build_site.py        # Jinja2 → HTML rendering
```

**Build Process:**

1. Load translations for both languages
2. Render all page types (home, browse, calendar, methods, about, data)
3. Copy static assets (CSS, JS, images)
4. Copy phylogeny figures from data repo
5. Generate bilingual site structure

---

### 7. CSS Styling System

- [x] Heritage color palette definition
- [x] Period-specific colors
- [x] Responsive layout (mobile-first)
- [x] Filter sidebar styling
- [x] Card grid layout
- [x] Table styling with sticky headers
- [x] Badge components
- [x] Accessibility styles (skip links, focus states)
- [x] Reduced motion support

**Files Created:**

```
static/assets/
└── site.css             # Custom styles (3,000+ lines)
```

**Color Palette:**

```css
--color-parchment: #f5f1e8;    /* Background */
--color-wood-dark: #5d4a2f;    /* Primary */
--color-gold: #c9a227;          /* Accent */
--color-muted-blue: #4a5f7f;   /* Secondary */
```

---

### 8. Documentation

- [x] Comprehensive README
- [x] Architecture documentation
- [x] Implementation plan (this file)
- [x] Inline code documentation
- [x] TODO lists for pending work

**Files Created:**

```
/
├── README.md                   # User guide and quick start
├── ARCHITECTURE.md             # Technical design decisions
└── IMPLEMENTATION_PLAN.md      # This file
```

---

### 9. Development Tooling

- [x] Watch script for auto-rebuild
- [x] Site validation script
- [x] Make targets for common tasks
- [x] Virtual environment setup

**Files Created:**

```
scripts/
├── watch.py             # Auto-rebuild on file changes
└── validate_site.py     # JSON schema + link checking
```

**Make Targets:**

```bash
make setup          # Create venv and install deps
make site-prepare   # Validate + generate data files
make site-build     # Render HTML pages
make site-serve     # Local dev server
make watch          # Auto-rebuild
make site-release   # Full build pipeline
make deploy         # Push to gh-pages
make test           # Run pytest
make clean          # Remove build artifacts
```

---

### 10. CI/CD Pipeline

- [x] GitHub Actions workflow
- [x] Automated deployment on tags
- [x] Manual deployment trigger
- [x] Data repository integration

**Files Created:**

```
.github/workflows/
└── deploy.yml           # GitHub Pages deployment
```

**Workflow:**

1. Trigger on `v*` tags or manual dispatch
2. Checkout visualization and data repos
3. Install Python dependencies
4. Validate data with strict mode
5. Generate data files
6. Build static site
7. Deploy to `gh-pages` branch

---

## 🚧 In Progress / Pending

### 11. JavaScript Implementation (HIGH PRIORITY)

The following JavaScript files have **stub implementations** with detailed TODO comments. They need full implementation:

#### `static/assets/map.js` ⚠️ TODO

**Responsibilities:**

- Initialize Leaflet map centered on Sweden
- Load `map_markers.geojson`
- Render markers with marker clustering
- Implement custom period-colored icons
- Create interactive popups
- Build filter UI dynamically
- Handle filter state management
- Update visible markers on filter change
- Display result counter
- Mobile responsive filter sidebar

**Dependencies:**

- Leaflet.js (CDN)
- Leaflet.markercluster (CDN)

**Estimated Effort:** 6-8 hours

---

#### `static/assets/browse.js` ⚠️ TODO

**Responsibilities:**

- Load calendar data from GeoJSON
- Render calendar cards in grid layout
- Implement filtering (shared logic with map)
- Client-side pagination (48 items/page)
- Sorting (catalog, period, diocese)
- Symbol category hints
- Responsive card layout

**Estimated Effort:** 4-6 hours

---

#### `static/assets/calendar.js` ⚠️ TODO

**Responsibilities:**

- Load calendar data (embedded or external JSON)
- Render feast table (365/366 rows)
- Implement table filtering (month, search)
- Create D3.js bar charts for symbols
- Initialize mini map with Leaflet
- Add marker at calendar location
- Handle responsive table layout

**Dependencies:**

- D3.js (CDN)
- Leaflet.js (CDN)

**Estimated Effort:** 6-8 hours

---

### 12. Testing Infrastructure ⚠️ TODO

- [ ] Pytest unit tests for Python scripts
- [ ] Data validation test cases
- [ ] Site generation integration tests
- [ ] JSON schema validation tests
- [ ] Internal link checking implementation
- [ ] Pa11y accessibility testing automation

**Files to Create:**

```
tests/
├── __init__.py
├── test_validation.py
├── test_prepare_data.py
├── test_build_site.py
└── test_integration.py
```

**Test Coverage Goal:** 80%+

**Estimated Effort:** 8-10 hours

---

### 13. Additional Features (LOWER PRIORITY)

#### Search Functionality

- [ ] Integrate Fuse.js for fuzzy search
- [ ] Load `search_docs.json`
- [ ] Implement search UI (expandable overlay)
- [ ] Highlight matches in results
- [ ] Search across cal_id, location, diocese, symbols, feasts

**Estimated Effort:** 4-6 hours

---

#### Calendar Detail Page Enhancements

- [ ] Complete all section implementations
- [ ] Add feast type filtering
- [ ] Display Grotefend references
- [ ] Link to Wikidata/Wikipedia for feasts
- [ ] Symbol co-occurrence network visualization
- [ ] Writing sample display with expansion

**Estimated Effort:** 6-8 hours

---

#### Performance Optimization

- [ ] Minify CSS and JS for production
- [ ] Optimize GeoJSON coordinate precision
- [ ] Add service worker for offline access
- [ ] Implement lazy loading for charts
- [ ] Bundle size analysis

**Estimated Effort:** 3-4 hours

---

## 📋 Data Requirements

### Required from runestaves_data Repository

The build system expects the following files:

```
../runestaves_data/zenodo/data/
├── inventory.tsv
├── individual.tsv
├── gazetteer.tsv
├── grotefend.tsv
├── generated/
│   └── symbol_instances.tsv
└── lookups/
    ├── symbol_types.tsv
    ├── feast_canonical.tsv
    └── feast_normalization_map.tsv

../runestaves_data/release/
├── phylogeny_dendrogram.png
└── phylogeny_pca.png

../runestaves_data/CITATION.cff
```

### Missing Data Elements

The following are expected by the spec but may need creation:

- [ ] `gazetteer.tsv` with `precision` column
- [ ] `symbol_types.tsv` with `category` column
- [ ] `feast_canonical.tsv` with `wikidata_id` column
- [ ] Placeholder images for calendars
- [ ] Uppsala University logo (SVG or PNG)
- [ ] Riksbankens Jubileumsfond logo (SVG or PNG)

---

## 🔧 Configuration Updates Needed

### Update URLs and Metadata

In `scripts/build_site.py`, update:

```python
config = {
    'zenodo_url': 'https://zenodo.org/record/XXXXXX',  # ← Update with real DOI
    'zenodo_doi': '10.5281/zenodo.XXXXXX',             # ← Update with real DOI
    'github_url': 'https://github.com/username/runestaves_data',  # ← Update
    'github_viz_url': 'https://github.com/username/runestaves_viz',  # ← Update
}
```

### Update GitHub Actions Secrets

In repository settings, add:

- `DATA_REPO` – Full repository path (e.g., `username/runestaves_data`)
- `DATA_REPO_TOKEN` – Personal access token (if data repo is private)

---

## 🎯 Next Steps (Recommended Order)

### Phase 1: Core Functionality (Week 1)

1. **Implement `map.js`** (Day 1-2)
   - Get basic map working with markers
   - Add clustering
   - Implement period-colored icons

2. **Implement filtering** (Day 3)
   - Build filter UI dynamically
   - Wire up filter logic
   - Test filter combinations

3. **Implement `browse.js`** (Day 4)
   - Card rendering
   - Pagination
   - Sorting

4. **Test and refine** (Day 5)
   - Cross-browser testing
   - Mobile responsive fixes
   - Performance optimization

### Phase 2: Calendar Details (Week 2)

1. **Implement `calendar.js`** (Day 1-2)
   - Feast table rendering
   - Table filtering and search
   - Mini map

2. **Add D3.js charts** (Day 3)
   - Symbol type bar chart
   - Symbol category bar chart
   - Responsive sizing

3. **Complete calendar page sections** (Day 4)
   - Symbol co-occurrence
   - Writing samples
   - Dating context

4. **Test and refine** (Day 5)
   - Data loading (embedded vs. external)
   - Chart interactions
   - Mobile layout

### Phase 3: Polish & Deploy (Week 3)

1. **Testing infrastructure** (Day 1-2)
   - Write unit tests
   - Integration tests
   - Accessibility testing

2. **Search implementation** (Day 3)
   - Fuse.js integration
   - Search UI
   - Result highlighting

3. **Content and assets** (Day 4)
   - Expand methods/about pages
   - Add real logos
   - Add museum credits

4. **Deployment** (Day 5)
   - Update configuration
   - Test GitHub Actions
   - Deploy v1.0.0

---

## 📊 Progress Summary

| Category | Status | Progress |
|----------|--------|----------|
| **Infrastructure** | ✅ Complete | 100% |
| **Data Pipeline** | ✅ Complete | 100% |
| **Templates** | ✅ Complete | 100% |
| **Styling** | ✅ Complete | 100% |
| **Documentation** | ✅ Complete | 100% |
| **JavaScript** | ⚠️ Stubs Only | 10% |
| **Testing** | ⚠️ Not Started | 0% |
| **Content** | ⚠️ Partial | 40% |

**Overall Progress:** ~75% complete

---

## 🤝 Contributing

### For Developers

1. **Set up environment:**
   ```bash
   make setup
   source venv/bin/activate
   ```

2. **Start watch mode:**
   ```bash
   make watch
   # In another terminal:
   make site-serve
   ```

3. **Make changes:**
   - Templates: `templates/*.html`
   - Styles: `static/assets/site.css`
   - Scripts: `static/assets/*.js`
   - Translations: `i18n/{lang}.json`

4. **Test:**
   ```bash
   make test
   make site-validate
   ```

### For Translators

- Edit `i18n/sv.json` or `i18n/en.json`
- Edit markdown files in `i18n/sv/` or `i18n/en/`
- Run `make site-build` to see changes

### For Content Contributors

- Methods page: `i18n/{lang}/methods.md`
- About page: `i18n/{lang}/about.md`
- Update translations in JSON files for new content

---

## 📝 Notes

### Design Decisions

- **No Node.js build system:** Keeps project simple and accessible
- **Pure Python:** Familiar to researchers, easy to maintain
- **Static generation:** Fast, secure, works on any host
- **Bilingual by default:** Swedish primary audience, English for international access
- **Accessibility first:** WCAG 2.1 AA compliance from the start

### Known Limitations

- Calendar images are placeholders (awaiting high-res scans)
- Some data fields may be incomplete (location estimates, etc.)
- JavaScript features require implementation before site is fully functional

### Future Enhancements (Post-v1.0)

- Progressive Web App capabilities
- Advanced timeline view
- Network visualization of symbol co-occurrences
- User annotation system (via GitHub issues)
- Social media preview cards
- Downloadable datasets (CSV, JSON exports)

---

**Questions?** Open an issue on GitHub or consult the [README](README.md) and [ARCHITECTURE](ARCHITECTURE.md) docs.
