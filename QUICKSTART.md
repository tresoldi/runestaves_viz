# Quick Start Guide

Get the Runestaves Visualization site running in 5 minutes.

## Prerequisites

- Python 3.11+
- Access to `runestaves_data` repository (sibling directory)
- Basic familiarity with command line

## Step-by-Step

### 1. Set Up Environment (1 minute)

```bash
cd runestaves_viz
make setup
source venv/bin/activate
```

This creates a virtual environment and installs all Python dependencies.

### 2. Verify Data Repository (30 seconds)

```bash
ls ../runestaves_data/zenodo/data/
```

You should see:
- `inventory.tsv`
- `individual.tsv`
- `gazetteer.tsv`
- `generated/symbol_instances.tsv`
- `lookups/*.tsv`

If not, clone or create symlink to the data repository.

### 3. Prepare Data (1-2 minutes)

```bash
make site-prepare
```

This will:
- ✅ Validate all TSV files
- ✅ Generate `site/data/map_markers.geojson`
- ✅ Generate `site/data/search_docs.json`
- ✅ Generate `site/data/stats.json`
- ✅ Generate per-calendar JSON files

**Expected output:**

```
Loading TSV files...
  Loaded inventory: 891 rows, 43 columns
  Loaded individual: 324915 rows, 13 columns
  Loaded gazetteer: 123 rows, 7 columns
  ...
Generating map_markers.geojson...
  ✓ Generated 753 markers (487.3 KB)
...
✓ Data preparation complete
```

### 4. Build Site (30 seconds)

```bash
make site-build
```

This will:
- ✅ Render Swedish pages (`/`)
- ✅ Render English pages (`/en/`)
- ✅ Copy static assets
- ✅ Copy phylogeny images

**Expected output:**

```
Building SV site
  ✓ index.html
  ✓ bladdra/index.html
  ...
Building EN site
  ✓ en/index.html
  ✓ en/browse/index.html
  ...
Copying static assets...
  ✓ Copied assets to assets
✓ Site build complete
```

### 5. Preview Locally (30 seconds)

```bash
make site-serve
```

Open http://localhost:8000 in your browser.

**You should see:**

- ✅ Swedish homepage with map
- ✅ Navigation to all pages
- ✅ Language switcher to English

---

## Development Workflow

### Auto-Rebuild on Changes

Open two terminals:

**Terminal 1:**
```bash
make watch
```

**Terminal 2:**
```bash
make site-serve
```

Now any changes to `templates/`, `static/`, or `i18n/` will auto-rebuild!

### Making Changes

**Edit UI text:**
```bash
vi i18n/sv.json      # Swedish
vi i18n/en.json      # English
# Changes auto-rebuild
```

**Edit styles:**
```bash
vi static/assets/site.css
# Refresh browser to see changes
```

**Edit templates:**
```bash
vi templates/home.html
# Changes auto-rebuild
```

---

## Common Issues

### "Data directory not found"

**Problem:** `make site-prepare` fails with "ERROR: Data directory not found"

**Solution:** Ensure data repo is at `../runestaves_data/zenodo/data/`

```bash
ls ../runestaves_data/zenodo/data/inventory.tsv
# Should exist
```

### "No module named 'pandera'"

**Problem:** Python dependencies not installed

**Solution:**
```bash
source venv/bin/activate  # Activate venv first!
pip install -r requirements.txt
```

### "Command not found: make"

**Problem:** Make not installed (rare on Linux/Mac)

**Solution:**

**On Ubuntu/Debian:**
```bash
sudo apt install build-essential
```

**On macOS:**
```bash
xcode-select --install
```

**Alternative:** Run commands directly:
```bash
python scripts/prepare_data.py --data-dir ../runestaves_data/zenodo/data --release-dir ../runestaves_data/release --output-dir site/data
python scripts/build_site.py --data-dir ../runestaves_data/zenodo/data --site-dir site
```

### Map not loading

**Problem:** JavaScript console shows "TODO: Initialize Leaflet map"

**Solution:** The JavaScript files are currently stubs. See [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for implementation status.

---

## Next Steps

1. **Review the site structure:**
   ```bash
   tree site/ -L 2
   ```

2. **Check generated data files:**
   ```bash
   ls -lh site/data/
   head -20 site/data/map_markers.geojson
   ```

3. **Read the documentation:**
   - [README.md](README.md) – Full user guide
   - [ARCHITECTURE.md](ARCHITECTURE.md) – Technical design
   - [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) – What's done, what's next

4. **Implement JavaScript features:**
   - `static/assets/map.js` – Interactive map
   - `static/assets/browse.js` – Calendar grid
   - `static/assets/calendar.js` – Detail pages

---

## Deployment

When ready to deploy:

```bash
# 1. Tag a release
git tag v1.0.0

# 2. Build and validate
make site-release

# 3. Deploy to GitHub Pages
make deploy

# Or use GitHub Actions (automatic on tag push)
git push origin v1.0.0
```

---

**Questions?** See [README.md](README.md) or open an issue on GitHub.
