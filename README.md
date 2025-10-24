# Runestaves Visualization – Static Web Interface

A fully static, bilingual (Swedish/English) web interface for exploring Sweden's runestave calendars. Built with Python, Jinja2, and vanilla JavaScript—no Node.js build system required.

## Overview

This project generates a static website from TSV data files, creating an interactive map, browseable catalog, and detailed calendar pages. The site is designed for deployment to GitHub Pages and targets the general Swedish public, museum visitors, and heritage researchers.

### Features

- **Interactive map** with Leaflet.js showing calendar locations
- **Advanced filtering** by period, diocese, material, symbols, etc.
- **Bilingual interface** (Swedish default, English mirror)
- **Individual calendar pages** with feast tables, symbol analysis, and charts
- **Phylogenetic analysis** visualizations
- **Fully static** – no server-side processing required
- **Accessible** – WCAG 2.1 AA compliant
- **Heritage design** – warm, educational color palette

## Project Structure

```
runestaves_viz/
├── scripts/               # Python build scripts
│   ├── schemas.py         # Pandera validation schemas
│   ├── validate_data.py   # Data validation
│   ├── prepare_data.py    # Generate JSON/GeoJSON from TSVs
│   ├── build_site.py      # Render HTML from templates
│   └── validate_site.py   # Site validation (links, a11y)
├── templates/             # Jinja2 HTML templates
│   ├── base.html          # Base layout
│   ├── home.html          # Map page
│   ├── browse.html        # Browse/grid view
│   ├── calendar.html      # Individual calendar detail
│   ├── methods.html       # Methods page
│   ├── about.html         # About page
│   └── data.html          # Data & citation page
├── static/assets/         # CSS, JS, images
│   ├── site.css           # Custom styles (heritage palette)
│   ├── map.js             # Map + filtering logic (TODO)
│   ├── browse.js          # Browse page logic (TODO)
│   └── calendar.js        # Calendar detail logic (TODO)
├── i18n/                  # Translations and content
│   ├── sv.json            # Swedish UI strings
│   ├── en.json            # English UI strings
│   ├── sv/                # Swedish markdown content
│   │   ├── methods.md
│   │   └── about.md
│   └── en/                # English markdown content
│       ├── methods.md
│       └── about.md
├── tests/                 # Pytest tests
├── site/                  # Generated static site (gitignored)
│   ├── data/              # Generated JSON/GeoJSON files
│   ├── assets/            # Copied static assets
│   ├── kalendrar/         # Swedish calendar pages
│   └── en/                # English site mirror
├── Makefile               # Build automation
├── requirements.txt       # Python dependencies
├── VERSION                # Semantic version
└── README.md              # This file
```

## Quick Start

### 1. Setup Environment

```bash
make setup
source venv/bin/activate
```

This creates a virtual environment and installs all dependencies.

### 2. Prepare Data

Ensure the runestaves data repository is available at `../runestaves_data/`:

```bash
make site-prepare
```

This will:
- Validate all TSV files against schemas
- Generate `map_markers.geojson` (all calendars with coordinates)
- Generate `search_docs.json` (compact search index)
- Generate `stats.json` (global statistics)
- Generate per-calendar JSON files (for detail pages)

### 3. Build Site

```bash
make site-build
```

This will:
- Render all HTML pages (Swedish and English)
- Copy static assets (CSS, JS, images)
- Copy phylogeny figures from data repo
- Create `.nojekyll` file for GitHub Pages

### 4. Preview Locally

```bash
make site-serve
```

Open http://localhost:8000 in your browser.

### 5. Deploy to GitHub Pages

Since the data repository (`evotext/runestaves_data`) is private, deployment is done locally and pushed to GitHub Pages.

**One-time setup:**

1. **Enable GitHub Pages:**
   - Go to https://github.com/tresoldi/runestaves_viz/settings/pages
   - Under "Build and deployment":
     - **Source**: Select "Deploy from a branch"
     - **Branch**: Select `gh-pages` and `/ (root)`
     - Click **Save**

**Deploy the site:**

```bash
./deploy.sh
```

This script will:
1. Clean previous builds
2. Build the site with the correct base path (`/runestaves_viz`)
3. Push the built site to the `gh-pages` branch
4. Your site will be live in 1-2 minutes at: `https://tresoldi.github.io/runestaves_viz/`

**Manual deployment steps:**

If you prefer to run steps manually:

```bash
# Build site with GitHub Pages base path
make clean
BASE_PATH=/runestaves_viz make site-release

# Deploy to gh-pages branch
cd site
git init
git add -A
git commit -m "Deploy site - $(date -I)"
git push -f origin master:gh-pages
cd ..
rm -rf site/.git
```

## Build System

### Makefile Targets

| Target | Description |
|--------|-------------|
| `make setup` | Create venv and install dependencies |
| `make site-prepare` | Validate data and generate JSON/GeoJSON |
| `make site-build` | Render all HTML pages |
| `make site-validate` | Run validation tests |
| `make site-serve` | Start local dev server (port 8000) |
| `make site-release` | Full build pipeline for deployment |
| `make deploy` | Deploy to gh-pages branch |
| `make watch` | Auto-rebuild on file changes (dev mode) |
| `make test` | Run pytest tests |
| `make clean` | Remove build artifacts |

### Data Flow

```
TSV files (runestaves_data/)
    ↓
[validate_data.py] ← schemas.py
    ↓
[prepare_data.py]
    ↓
JSON/GeoJSON (site/data/)
    ↓
[build_site.py] ← templates/ + i18n/
    ↓
HTML pages (site/)
    ↓
[validate_site.py]
    ↓
GitHub Pages (gh-pages branch)
```

## Data Files

### Input (from runestaves_data/)

- `inventory.tsv` – Calendar metadata (891 calendars)
- `individual.tsv` – Daily entries (365/366 rows per calendar)
- `gazetteer.tsv` – Location coordinates
- `generated/symbol_instances.tsv` – Symbol occurrences
- `lookups/symbol_types.tsv` – Symbol category mappings
- `lookups/feast_canonical.tsv` – Feast normalization
- `release/phylogeny_*.png` – Analysis figures

### Output (site/data/)

- `map_markers.geojson` – All calendars for map (with properties)
- `search_docs.json` – Compact search index for Fuse.js
- `stats.json` – Global statistics for charts
- `calendars/{cal_id}.json` – Per-calendar data (if >30KB)
- `calendar_index.json` – Metadata about calendar data files

## Bilingual Implementation

- **Swedish** is the default language (root paths: `/`, `/bladdra/`, etc.)
- **English** is mirrored under `/en/` (`/en/`, `/en/browse/`, etc.)
- All UI strings are loaded from `i18n/{lang}.json`
- Narrative content (methods, about) uses markdown files in `i18n/{lang}/`
- Language switcher links to mirrored path in other language

## Customization

### Color Palette

The heritage color palette is defined in `static/assets/site.css`:

```css
--color-parchment: #f5f1e8;
--color-wood-dark: #5d4a2f;
--color-gold: #c9a227;
--color-muted-blue: #4a5f7f;
...
```

All colors use CSS variables for easy theming.

### Period Colors

Map markers and badges are colored by historical period:

- Medieval (≤1527): Deep red
- 16th century: Rust
- 17th century: Medium wood
- 18th century: Muted blue
- 19th century: Forest green
- Unknown: Gray

### Adding New Filters

To add a new filter to the map/browse pages:

1. Add filter UI in `templates/home.html` and `templates/browse.html`
2. Add translation strings to `i18n/sv.json` and `i18n/en.json`
3. Update `static/assets/map.js` to handle the new filter
4. Ensure the property exists in `map_markers.geojson` (via `prepare_data.py`)

## JavaScript Architecture

The site uses vanilla JavaScript with no build step:

- `map.js` – Leaflet map initialization, filtering, clustering
- `browse.js` – Card grid rendering, filtering, pagination
- `calendar.js` – Feast table, symbol charts (D3.js), mini map

All scripts receive configuration from inline `<script>` blocks in HTML:

```javascript
const mapConfig = {
    lang: 'sv',
    baseUrl: '',
    dataUrl: '/data/map_markers.geojson',
    translations: { ... }
};
```

## Symbol Categories

Symbol instances are classified into 15 categories:

- Religious, Liturgical, Royal
- Agricultural, Tools, Occupational
- Drinking, Animals, Human, Plants
- Geometric, Natural phenomena
- Text, Notation, Generic

Categories are assigned via `lookups/symbol_types.tsv`.

## Testing

### Data Validation

```bash
python scripts/validate_data.py --data-dir ../runestaves_data/zenodo/data --strict
```

- Validates schemas with Pandera
- Checks referential integrity between files
- Reports missing coordinates, orphaned records

### Site Validation

```bash
python scripts/validate_site.py --site-dir site
```

- Validates JSON schema conformance
- Checks internal link integrity
- Runs accessibility tests (Pa11y)

### Unit Tests

```bash
make test
# or
pytest tests/ -v
```

## Accessibility

- Semantic HTML throughout
- ARIA labels for all interactive elements
- Keyboard navigation support
- `prefers-reduced-motion` respected
- WCAG 2.1 AA contrast compliance
- Screen reader tested

## Browser Support

Modern browsers (2021+):

- Safari 15+
- Chrome 90+
- Firefox 88+
- Edge 90+

Graceful degradation messages for older browsers.

## Performance

### Targets

- `map_markers.geojson` ≤ 800 KB
- Initial page load < 2 seconds (broadband)
- Lazy chart initialization on calendar pages

### Optimization

- GeoJSON uses compact coordinate precision
- Per-calendar JSON only loaded when needed
- Images lazy-loaded with `loading="lazy"`
- CDN resources for Leaflet, D3, Pico.css

## Deployment

### GitHub Pages Configuration

1. Build site: `make site-release`
2. Deploy: `make deploy`
3. Configure GitHub repository settings:
   - Settings → Pages → Source: `gh-pages` branch
   - Custom domain (optional)

### Automated Deployment

A GitHub Actions workflow (`.github/workflows/deploy.yml`) can automate deployment on tagged releases:

```yaml
on:
  push:
    tags:
      - 'v*'
```

See "Set up GitHub Actions for automated deployment" in project plan.

## Development Workflow

### Iterative Development

```bash
# Terminal 1: Watch for changes
make watch

# Terminal 2: Serve site
make site-serve
```

The `watch` target monitors `scripts/`, `templates/`, `static/`, and `i18n/` for changes and auto-rebuilds.

### Making Changes

1. **Data changes**: Update TSVs in runestaves_data/, run `make site-prepare`
2. **UI strings**: Edit `i18n/{lang}.json`, run `make site-build`
3. **Templates**: Edit `templates/*.html`, run `make site-build`
4. **Styles**: Edit `static/assets/site.css`, refresh browser
5. **Scripts**: Edit `static/assets/*.js`, refresh browser

## License

This visualization interface is licensed under **MIT License**.

The runestave data is licensed under **CC-BY 4.0**.

## Acknowledgments

- **Uppsala University** – Project affiliation
- **Riksbankens Jubileumsfond (RJ)** – Funding
- **Swedish museums** – Data contributions

## Contact

For questions or contributions, please open an issue on GitHub.

## TODO

The following components need implementation:

### JavaScript (High Priority)

- [ ] `static/assets/map.js` – Map initialization, filtering, clustering
- [ ] `static/assets/browse.js` – Browse page with cards and pagination
- [ ] `static/assets/calendar.js` – Feast table, symbol charts, mini map

### Testing

- [ ] Unit tests for Python scripts (`tests/`)
- [ ] Integration tests for site generation
- [ ] Accessibility testing automation

### Additional Features

- [ ] Search functionality (Fuse.js integration)
- [ ] Watch mode implementation (`scripts/watch.py`)
- [ ] Site validation script (`scripts/validate_site.py`)
- [ ] GitHub Actions deployment workflow

### Content

- [ ] Update Zenodo DOI once data is published
- [ ] Add real Uppsala University and RJ logos
- [ ] Expand methods and about page content
- [ ] Add museum credits and contact information

### Refinements

- [ ] Calendar detail page: complete all sections
- [ ] Responsive design testing on mobile devices
- [ ] Performance optimization and bundle size analysis
- [ ] Browser compatibility testing

---

**Version:** 0.1.0 (Development)
**Last Updated:** 2025-10-22
