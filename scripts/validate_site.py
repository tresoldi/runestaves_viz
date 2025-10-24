#!/usr/bin/env python3
"""
Validate generated static site.

Checks:
- JSON schema conformance
- Internal link integrity
- Basic accessibility (if Pa11y available)
"""

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse


def validate_json_files(site_dir: Path) -> bool:
    """Validate JSON data files against basic schema."""
    print("Validating JSON files...")

    data_dir = site_dir / 'data'
    if not data_dir.exists():
        print("  ⚠ No data directory found")
        return False

    all_valid = True

    # Check map_markers.geojson
    geojson_file = data_dir / 'map_markers.geojson'
    if geojson_file.exists():
        try:
            with open(geojson_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if data.get('type') != 'FeatureCollection':
                print(f"  ❌ {geojson_file.name}: Not a FeatureCollection")
                all_valid = False
            elif not isinstance(data.get('features'), list):
                print(f"  ❌ {geojson_file.name}: Features is not a list")
                all_valid = False
            else:
                print(f"  ✓ {geojson_file.name}: Valid ({len(data['features'])} features)")
        except json.JSONDecodeError as e:
            print(f"  ❌ {geojson_file.name}: JSON decode error: {e}")
            all_valid = False
    else:
        print(f"  ⚠ {geojson_file.name}: Not found")
        all_valid = False

    # Check search_docs.json
    search_file = data_dir / 'search_docs.json'
    if search_file.exists():
        try:
            with open(search_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, list):
                print(f"  ❌ {search_file.name}: Not a list")
                all_valid = False
            else:
                print(f"  ✓ {search_file.name}: Valid ({len(data)} documents)")
        except json.JSONDecodeError as e:
            print(f"  ❌ {search_file.name}: JSON decode error: {e}")
            all_valid = False
    else:
        print(f"  ⚠ {search_file.name}: Not found")

    # Check stats.json
    stats_file = data_dir / 'stats.json'
    if stats_file.exists():
        try:
            with open(stats_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, dict):
                print(f"  ❌ {stats_file.name}: Not an object")
                all_valid = False
            else:
                print(f"  ✓ {stats_file.name}: Valid")
        except json.JSONDecodeError as e:
            print(f"  ❌ {stats_file.name}: JSON decode error: {e}")
            all_valid = False
    else:
        print(f"  ⚠ {stats_file.name}: Not found")

    return all_valid


def check_internal_links(site_dir: Path) -> bool:
    """Check that internal links point to existing files."""
    print("\nChecking internal links...")

    # TODO: Implement link checking
    # - Find all HTML files
    # - Parse <a href> and <link href> and <script src>
    # - Check if internal links (no http://) point to existing files
    # - Report broken links

    print("  ⚠ Link checking not yet implemented")
    return True


def check_accessibility(site_dir: Path) -> bool:
    """Run basic accessibility checks."""
    print("\nChecking accessibility...")

    # TODO: Run Pa11y if available
    # - Test sample pages (home, browse, one calendar)
    # - Report WCAG 2.1 AA violations

    print("  ⚠ Accessibility testing not yet implemented")
    print("  To test manually, install Pa11y:")
    print("    npm install -g pa11y")
    print("    pa11y http://localhost:8000")

    return True


def main():
    parser = argparse.ArgumentParser(description='Validate generated site')
    parser.add_argument('--site-dir', type=Path, default=Path('site'))
    args = parser.parse_args()

    site_dir = args.site_dir
    if not site_dir.exists():
        print(f"ERROR: Site directory not found: {site_dir}")
        sys.exit(1)

    print(f"Validating site: {site_dir}")
    print("=" * 60)

    json_valid = validate_json_files(site_dir)
    links_valid = check_internal_links(site_dir)
    a11y_valid = check_accessibility(site_dir)

    print("\n" + "=" * 60)
    if json_valid and links_valid and a11y_valid:
        print("✓ All validations passed")
        sys.exit(0)
    else:
        print("⚠ Some validations failed")
        sys.exit(1)


if __name__ == '__main__':
    main()
