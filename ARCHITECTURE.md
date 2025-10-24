# Architecture Documentation

## Overview

The Runestaves Visualization project follows a **static site generation** architecture where all content is pre-rendered to HTML during build time. No server-side processing or Node.js build system is required.

## Design Principles

### 1. Simplicity First (KISS)

- Pure Python for data processing and site generation
- Vanilla JavaScript for client-side interactivity
- No complex build tools or bundlers
- Standard web technologies (HTML5, CSS3, ES6)

### 2. Smart Defaults, Expert Overrides

- Works out-of-the-box with minimal configuration
- All build steps configurable via Makefile parameters
- Color palette, periods, categories defined as CSS/Python constants
- Extensible filter and schema system

### 3. Correctness & Robustness

- Strict validation of critical fields (cal_id, coordinates)
- Graceful degradation for optional data
- Clear error messages with actionable guidance
- Referential integrity checks between data files

### 4. Modularity with Clean Interfaces

Each script has a single responsibility:

- `validate_data.py` → Validate TSVs
- `prepare_data.py` → Generate JSON/GeoJSON
- `build_site.py` → Render HTML
- `validate_site.py` → Test generated site

Clear data contracts between steps (JSON schemas).

### 5. Representation Over Logic

- Periods defined in data table (not hardcoded if/else chains)
- Symbol categories mapped via lookup file
- Translations in JSON (not scattered in code)
- Feast normalization via external table

## Data Architecture

### Input Data Model

```
inventory.tsv (1 row per calendar)
    ├─ Links to: gazetteer.tsv (location info)
    └─ Links to: individual.tsv (365/366 rows per calendar)
                    └─ References: feast_canonical.tsv

symbol_instances.tsv
    ├─ Links to: inventory.tsv (cal_id)
    └─ Links to: symbol_types.tsv (category mapping)
```

### Intermediate Representation

```python
{
  "cal_id": "umf1766",
  "properties": {
    "catalog": "UMF1766",
    "location_precision": "exact",
    "period_bucket_en": "Medieval",
    "has_religious": true,
    "has_agricultural": false,
    ...
  },
  "geometry": {"type": "Point", "coordinates": [lon, lat]}
}
```

### Output Files

| File | Format | Size | Purpose |
|------|--------|------|---------|
| `map_markers.geojson` | GeoJSON FeatureCollection | ~500 KB | Leaflet map markers |
| `search_docs.json` | JSON array | ~200 KB | Fuse.js search index |
| `stats.json` | JSON object | ~5 KB | Global statistics for charts |
| `calendars/{id}.json` | JSON object | Variable | Per-calendar detail data |

## Rendering Pipeline

### Phase 1: Data Preparation

```
TSV Files
    ↓
[Pandera Validation]
    ↓
[Year Parsing & Period Assignment]
    ↓
[Symbol Category Computation]
    ↓
[GeoJSON Feature Generation]
    ↓
site/data/*.json
```

**Key Functions:**

- `parse_year_range(year_str)` → (year_min, year_max)
- `assign_period_bucket(year_min, year_max)` → (en_label, sv_label)
- `compute_symbol_categories(symbols, types)` → {cal_id: {has_*: bool}}

### Phase 2: Site Building

```
Templates + i18n + Data
    ↓
[Jinja2 Environment]
    ↓
[Markdown Rendering]
    ↓
[Bilingual Page Generation]
    ↓
site/**/*.html
```

**Context Variables:**

```python
{
    't': translations,        # All UI strings
    'lang': 'sv' | 'en',
    'base_url': '' | '/en',
    'version': '0.1.0',
    'build_date': '2025-10-22',
    ... page-specific data
}
```

## Bilingual Strategy

### URL Structure

Swedish (default):

```
/                       → Home (map)
/bladdra/               → Browse
/kalendrar/{id}.html    → Calendar detail
/metod/                 → Methods
/om/                    → About
/data/                  → Data
```

English (mirrored):

```
/en/                    → Home (map)
/en/browse/             → Browse
/en/calendars/{id}.html → Calendar detail
/en/methods/            → Methods
/en/about/              → About
/en/data/               → Data
```

### Translation Loading

```python
# Load translations
translations_sv = json.load('i18n/sv.json')
translations_en = json.load('i18n/en.json')

# Access in templates
{{ t.nav.home }}          → "Start" (sv) | "Home" (en)
{{ t.periods.medieval }}  → "Medeltid" (sv) | "Medieval" (en)
```

### Content Rendering

```python
# Markdown content
content_sv = markdown('i18n/sv/methods.md')
content_en = markdown('i18n/en/methods.md')

# Injected into template
{{ content | safe }}
```

## Frontend Architecture

### No Build System Philosophy

**Why no bundler?**

- Reduces complexity and maintenance burden
- Faster iteration (edit → refresh, no compile step)
- Transparent debugging (readable source in DevTools)
- Works on any web server (no preprocessing required)

**Tradeoffs:**

- ❌ No tree shaking or minification
- ❌ No TypeScript type checking
- ✅ Faster development workflow
- ✅ Lower barrier to contribution
- ✅ No dependency churn (npm, webpack, etc.)

### JavaScript Module Pattern

```javascript
// map.js structure
(function() {
    'use strict';

    // Private state
    let map = null;
    let markers = [];
    let activeFilters = {};

    // Public API
    window.initializeMap = function(config) {
        // Initialize map, load data, set up filters
    };

    // Private helper functions
    function filterMarkers() { ... }
    function updateResultCount() { ... }
})();
```

### Data Loading

All data is fetched once on page load:

```javascript
// Fetch GeoJSON
fetch(config.dataUrl)
    .then(res => res.json())
    .then(data => {
        features = data.features;
        initializeFilters(features);
        renderMap(features);
    });
```

### Filter State Management

```javascript
const filterState = {
    period: new Set(),
    diocese: new Set(),
    material: new Set(),
    symbols: new Set(),
};

function applyFilters() {
    const visible = allFeatures.filter(feature => {
        if (filterState.period.size > 0 &&
            !filterState.period.has(feature.properties.period_bucket)) {
            return false;
        }
        // ... other filters
        return true;
    });

    updateMap(visible);
    updateResultCount(visible.length, allFeatures.length);
}
```

## Performance Considerations

### File Size Optimization

**GeoJSON Compression:**

```python
# Limit coordinate precision
lon = round(float(row['longitude']), 5)  # ~1 meter precision
lat = round(float(row['latitude']), 5)
```

**Compact JSON:**

```python
json.dump(data, f, separators=(',', ':'))  # No whitespace
```

**Per-Calendar Threshold:**

```python
# Embed small calendars in HTML
if json_size < 30_000:  # 30 KB
    embed_in_html(calendar_data)
else:
    write_to_file(f'calendars/{cal_id}.json')
```

### Lazy Loading

- Calendar detail charts only initialized when visible
- Images use `loading="lazy"` attribute
- External calendar JSON only fetched when page is viewed

### Map Performance

- Marker clustering for dense areas (Leaflet.markercluster)
- Filter debouncing (update on "Apply" button, not every keystroke)
- Limited marker popups (only visible markers)

## Accessibility Architecture

### Semantic HTML

```html
<nav aria-label="breadcrumb">...</nav>
<table>
    <caption>Feast days for UMF1766</caption>
    <thead>
        <tr>
            <th scope="col">Month</th>
            ...
```

### Keyboard Navigation

- All interactive elements focusable
- Logical tab order
- Skip links for screenreaders

### ARIA Labels

```html
<button aria-label="{{ t.accessibility.open_menu }}">
    ☰
</button>

<div id="map" aria-label="{{ t.map.title }}"></div>
```

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}
```

## Color System

### Heritage Palette

Inspired by medieval manuscripts, wood, and parchment:

```css
:root {
    --color-parchment: #f5f1e8;    /* Aged paper background */
    --color-wood-dark: #5d4a2f;    /* Primary text, headers */
    --color-gold: #c9a227;          /* Accents, highlights */
    --color-muted-blue: #4a5f7f;   /* Secondary elements */
}
```

### Period Color Encoding

Each historical period has a distinct hue:

```css
--period-medieval: #8b1a1a;     /* Deep red */
--period-16th: #a0522d;         /* Rust */
--period-17th: #8b6f47;         /* Medium wood */
--period-18th: #4a5f7f;         /* Muted blue */
--period-19th: #2c5530;         /* Forest green */
--period-unknown: #6b7280;      /* Gray */
```

Used consistently across:

- Map markers
- Badge colors
- Chart categories

### Contrast Compliance

All text/background pairs tested for WCAG 2.1 AA:

- Normal text: ≥4.5:1
- Large text: ≥3:1
- Interactive elements: ≥3:1

## Validation Strategy

### Three-Tier Validation

**1. Data Validation (Pandera)**

- Schema conformance
- Type checking
- Range validation
- Referential integrity

**2. Build Validation**

- Template rendering errors
- Missing translation keys
- Broken asset references

**3. Site Validation**

- JSON schema conformance
- Internal link checking
- Accessibility testing (Pa11y)

### Error Handling

```python
# Hybrid strict/graceful approach
def validate_dataframe(df, schema, strict=False):
    try:
        return schema.validate(df)
    except SchemaError as e:
        if strict:
            raise
        else:
            warnings.warn(f"Validation issues: {e}")
            return df  # Continue with warnings
```

## Testing Philosophy

### Pyramid Strategy

```
         /\
        /UI\         ← Manual testing (browsers, mobile)
       /────\
      /Integ\        ← Site validation, link checking
     /──────\
    /  Unit  \       ← Python function tests
   /──────────\
```

### Test Coverage Goals

- **Unit tests**: 80%+ coverage for Python scripts
- **Integration**: All build steps run successfully
- **Accessibility**: Pa11y scores 100% on sample pages
- **Manual**: Test on 3+ browsers, 2+ mobile devices

## Deployment Architecture

### GitHub Pages Flow

```
main branch
    ↓
[Git tag v1.0.0]
    ↓
[GitHub Action: make site-release]
    ↓
[Generated site/]
    ↓
gh-pages branch ← force push
    ↓
GitHub Pages (CDN)
```

### Cache Strategy

- Bust cache on version change (footer shows version)
- GeoJSON/JSON data files: cache for 1 day
- HTML pages: no cache (always fresh)
- Assets (CSS/JS/images): cache for 1 week

## Extensibility Points

### Adding New Page Types

1. Create template in `templates/new_page.html`
2. Add translations to `i18n/{lang}.json`
3. Add markdown content to `i18n/{lang}/new_page.md`
4. Register in `build_site.py`:

```python
new_page_context = {
    **common_context,
    'content': load_markdown_content(lang, 'new_page', i18n_dir),
}
build_page(env, 'new_page.html', output_path, new_page_context)
```

### Adding New Data Sources

1. Define schema in `schemas.py`
2. Load in `prepare_data.py`
3. Join/merge with existing data
4. Add to output JSON

### Adding New Filters

1. Ensure property exists in GeoJSON (`prepare_data.py`)
2. Add UI in `templates/home.html`
3. Add translations to `i18n/*.json`
4. Update `map.js` filter logic

## Future Enhancements

### Considered but Deferred

**Progressive Web App (PWA):**

- Add service worker for offline access
- Add manifest.json for installability

**Advanced Search:**

- Integrate Fuse.js for fuzzy search
- Search across feasts, symbols, locations

**Timeline View:**

- Horizontal timeline showing calendar distribution by period
- Brush/zoom interaction

**Social Sharing:**

- Generate og:image preview cards
- Add share buttons to calendar pages

**User Annotations:**

- Allow visitors to submit corrections (via GitHub issues)
- Display community-contributed notes

## Conclusion

This architecture prioritizes **simplicity, maintainability, and correctness** while delivering a rich, interactive experience for exploring Sweden's runestave heritage. By keeping the build pipeline straightforward and avoiding unnecessary complexity, the project remains accessible to contributors with basic Python and web development skills.
