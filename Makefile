# Runestaves Visualization - Static Site Generator
# ================================================

.PHONY: help setup clean site-clean site-prepare site-build site-validate site-serve site-release watch test

# Configuration
PYTHON := python3
VENV := venv
DATA_DIR := ../runestaves_data/zenodo/data
RELEASE_DIR := ../runestaves_data/release
SITE_DIR := site
SCRIPTS_DIR := scripts
PORT := 8000

help:
	@echo "Runestaves Visualization - Build System"
	@echo "========================================"
	@echo ""
	@echo "Available targets:"
	@echo "  setup           - Create virtual environment and install dependencies"
	@echo "  site-prepare    - Validate TSVs and generate JSON/GeoJSON data files"
	@echo "  site-build      - Render all HTML pages and copy assets"
	@echo "  site-validate   - Run validation tests (schemas, links, accessibility)"
	@echo "  site-serve      - Start local development server on port $(PORT)"
	@echo "  site-release    - Full build pipeline for deployment"
	@echo "  watch           - Auto-rebuild on file changes (development mode)"
	@echo "  test            - Run all tests"
	@echo "  clean           - Remove build artifacts"
	@echo "  site-clean      - Remove generated site directory"
	@echo ""

setup:
	@echo "Setting up development environment..."
	test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt
	@echo "✓ Setup complete. Activate with: source $(VENV)/bin/activate"

site-prepare:
	@echo "Preparing data files..."
	@test -d $(DATA_DIR) || (echo "ERROR: Data directory not found: $(DATA_DIR)" && exit 1)
	$(VENV)/bin/python $(SCRIPTS_DIR)/validate_data.py --data-dir $(DATA_DIR)
	$(VENV)/bin/python $(SCRIPTS_DIR)/prepare_data.py --data-dir $(DATA_DIR) --release-dir $(RELEASE_DIR) --output-dir $(SITE_DIR)/data
	@echo "✓ Data preparation complete"

site-build: site-prepare
	@echo "Building static site..."
	$(VENV)/bin/python $(SCRIPTS_DIR)/build_site.py --data-dir $(DATA_DIR) --site-dir $(SITE_DIR)
	@echo "✓ Site build complete"

site-validate:
	@echo "Validating generated site..."
	$(VENV)/bin/python $(SCRIPTS_DIR)/validate_site.py --site-dir $(SITE_DIR)
	@echo "✓ Validation complete"

site-serve:
	@echo "Starting development server at http://localhost:$(PORT)"
	@echo "Press Ctrl+C to stop"
	@cd $(SITE_DIR) && $(PYTHON) -m http.server $(PORT)

watch:
	@echo "Starting watch mode..."
	@echo "Watching for changes in scripts/, templates/, static/, i18n/"
	$(VENV)/bin/python $(SCRIPTS_DIR)/watch.py

site-release: clean site-prepare site-build site-validate
	@echo "Building release..."
	@echo "Version: $$(cat VERSION 2>/dev/null || echo 'dev')"
	@echo "Date: $$(date -I)"
	@touch $(SITE_DIR)/.nojekyll
	@echo "✓ Release build complete"
	@echo ""
	@echo "To deploy to GitHub Pages:"
	@echo "  1. Review the generated site in $(SITE_DIR)/"
	@echo "  2. Run: make deploy"

deploy:
	@echo "Deploying to gh-pages branch..."
	@if [ ! -d "$(SITE_DIR)" ]; then echo "ERROR: Site not built. Run 'make site-release' first."; exit 1; fi
	@git rev-parse --verify gh-pages >/dev/null 2>&1 || git checkout --orphan gh-pages
	@git --work-tree=$(SITE_DIR) checkout gh-pages
	@cp -r $(SITE_DIR)/* .
	@git add -A
	@git commit -m "Deploy site - $$(date -I)" || echo "No changes to deploy"
	@git checkout master
	@echo "✓ Deployed to gh-pages. Push with: git push origin gh-pages"

test:
	@echo "Running tests..."
	$(VENV)/bin/pytest tests/ -v --cov=$(SCRIPTS_DIR) --cov-report=term-missing

clean:
	@echo "Cleaning build artifacts..."
	rm -rf $(SITE_DIR)/*
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Clean complete"

site-clean: clean
	@echo "✓ Site directory cleaned"
