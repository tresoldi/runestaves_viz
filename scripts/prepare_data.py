#!/usr/bin/env python3
"""
Prepare data files for the Runestaves static website.

This script transforms TSV data into JSON/GeoJSON files optimized for
web display:
  - map_markers.geojson: All calendars with coordinates for Leaflet map
  - search_docs.json: Compact search index for Fuse.js
  - stats.json: Global statistics for charts
  - calendars/*.json: Per-calendar detailed data (if > 30KB)

Outputs are written to the site/data/ directory.
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import pandas as pd
from geojson import Feature, FeatureCollection, Point

from schemas import ValidationConfig


def assign_period_bucket(year_min: float, year_max: float) -> tuple[str, str]:
    """
    Assign period bucket based on midpoint of year range.

    Returns:
        (english_label, swedish_label)
    """
    if pd.isna(year_min) or pd.isna(year_max):
        return ('Unknown', 'Okänt')

    midpoint = (year_min + year_max) / 2

    for en_label, sv_label, min_year, max_year in ValidationConfig.PERIOD_BUCKETS:
        if min_year is None:  # Unknown bucket
            continue
        if min_year <= midpoint <= max_year:
            return (en_label, sv_label)

    return ('Unknown', 'Okänt')


def parse_year_range(year_str: str) -> tuple[float, float]:
    """
    Parse year field into min/max range.

    Examples:
        "1650" -> (1650, 1650)
        "1650-1700" -> (1650, 1700)
        "ante 1700" -> (1600, 1700)  # estimate 100 years before
        "post 1650" -> (1650, 1750)  # estimate 100 years after
    """
    if pd.isna(year_str) or not year_str or year_str.strip() == '':
        return (float('nan'), float('nan'))

    year_str = str(year_str).strip().lower()

    # Handle ranges like "1650-1700"
    if '-' in year_str and not year_str.startswith('ante') and not year_str.startswith('post'):
        parts = year_str.split('-')
        try:
            return (float(parts[0]), float(parts[1]))
        except (ValueError, IndexError):
            return (float('nan'), float('nan'))

    # Handle "ante YEAR"
    if year_str.startswith('ante'):
        try:
            year = float(year_str.replace('ante', '').strip())
            return (year - 100, year)
        except ValueError:
            return (float('nan'), float('nan'))

    # Handle "post YEAR"
    if year_str.startswith('post'):
        try:
            year = float(year_str.replace('post', '').strip())
            return (year, year + 100)
        except ValueError:
            return (float('nan'), float('nan'))

    # Single year
    try:
        year = float(year_str)
        return (year, year)
    except ValueError:
        return (float('nan'), float('nan'))


def denormalize_gazetteer(inventory: pd.DataFrame, gazetteer: pd.DataFrame) -> pd.DataFrame:
    """
    Denormalize the gazetteer to add location_name, diocese_name, and socken columns to inventory.

    The gazetteer is normalized with geoid/name pairs for all geographic entities.
    We need to look up names for location_id, diocese_id, and socken_id.

    Returns:
        inventory DataFrame with additional columns: location_name, diocese_name, socken,
        latitude, longitude, coord_source
    """
    # Create a lookup dictionary for geoid -> name
    geoid_to_name = dict(zip(gazetteer['geoid'], gazetteer['name']))
    geoid_to_lat = dict(zip(gazetteer['geoid'], gazetteer['latitude']))
    geoid_to_lon = dict(zip(gazetteer['geoid'], gazetteer['longitude']))
    geoid_to_accuracy = dict(zip(gazetteer['geoid'], gazetteer['accuracy']))

    # Make a copy to avoid modifying the original
    result = inventory.copy()

    # Add location details
    result['location_name'] = result['location_id'].map(geoid_to_name)
    result['latitude'] = result['location_id'].map(geoid_to_lat)
    result['longitude'] = result['location_id'].map(geoid_to_lon)
    result['precision'] = result['location_id'].map(geoid_to_accuracy)

    # Add diocese details
    result['diocese_name'] = result['diocese_id'].map(geoid_to_name)

    # Add socken details
    result['socken'] = result['socken_id'].map(geoid_to_name)

    return result


def compute_symbol_categories(symbol_instances: pd.DataFrame, symbol_types: pd.DataFrame) -> dict:
    """
    Compute boolean flags for each symbol category per calendar.

    Returns:
        dict: {cal_id: {category: bool}}
    """
    # Build category mapping
    if symbol_types.empty or 'category' not in symbol_types.columns:
        print("  ⚠ symbol_types.tsv missing or has no category column")
        return {}

    type_to_category = dict(zip(symbol_types['symbol_type'], symbol_types['category']))

    # Assign categories to instances
    symbol_instances['category'] = symbol_instances['symbol_type'].map(type_to_category)

    # Group by calendar and category
    result = {}
    for cal_id, group in symbol_instances.groupby('cal_id'):
        categories = group['category'].dropna().unique()
        result[cal_id] = {
            f'has_{cat}': cat in categories for cat in ValidationConfig.SYMBOL_CATEGORIES
        }

    return result


def generate_map_markers(
    inventory: pd.DataFrame,
    gazetteer: pd.DataFrame,
    individual: pd.DataFrame,
    symbol_categories: dict,
    output_path: Path,
) -> int:
    """
    Generate GeoJSON file with map markers for all calendars.

    Returns:
        Number of calendars with valid coordinates
    """
    print("Generating map_markers.geojson...")

    # Denormalize gazetteer data into inventory
    merged = denormalize_gazetteer(inventory, gazetteer)

    # Filter to calendars with valid coordinates
    valid = merged[merged['latitude'].notna() & merged['longitude'].notna()].copy()

    if len(valid) == 0:
        print("  ⚠ No calendars with valid coordinates!")
        return 0

    # Parse year ranges
    valid[['year_min', 'year_max']] = valid['year'].apply(
        lambda y: pd.Series(parse_year_range(y))
    )

    # Assign period buckets
    valid[['period_en', 'period_sv']] = valid.apply(
        lambda row: pd.Series(assign_period_bucket(row['year_min'], row['year_max'])), axis=1
    )

    # Count feasts per calendar (for row_fest detection)
    feast_counts = individual.groupby('cal_id').size().to_dict()

    features = []
    for _, row in valid.iterrows():
        cal_id = row['id']

        # Get symbol category flags
        symbol_flags = symbol_categories.get(cal_id, {})

        # Helper to convert NaN to empty string
        def safe_get(key, default=''):
            val = row.get(key, default)
            return default if pd.isna(val) else val

        properties = {
            # Identification
            'cal_id': cal_id,
            'catalog': safe_get('cal_label'),
            # Provenance
            'institute_id': safe_get('institute'),
            'location_id': safe_get('location_id'),
            'location_name': safe_get('location_name'),
            'socken': safe_get('socken'),
            'diocese_id': safe_get('diocese_id'),
            'diocese_name': safe_get('diocese_name'),
            # Location precision
            'location_precision': safe_get('precision', 'unknown'),
            # Dating
            'year': safe_get('year'),
            'year_min': row['year_min'] if not pd.isna(row['year_min']) else None,
            'year_max': row['year_max'] if not pd.isna(row['year_max']) else None,
            'period_bucket_en': row['period_en'],
            'period_bucket_sv': row['period_sv'],
            # Physical
            'material_primary': safe_get('material_primary'),
            'material_secondary': safe_get('material_secondary1'),
            'shape': safe_get('shape'),
            'sides': int(row['sides']) if pd.notna(row.get('sides')) and str(row.get('sides', '')).isdigit() else None,
            # Notation
            'row_fest': safe_get('row_fest'),
            'solar': safe_get('solar'),
            # Data quality
            'completed': safe_get('completed'),
            # Links
            'detail_url_sv': f'/kalendrar/{cal_id}.html',
            'detail_url_en': f'/en/calendars/{cal_id}.html',
        }

        # Add symbol category flags
        properties.update(symbol_flags)

        feature = Feature(
            geometry=Point((float(row['longitude']), float(row['latitude']))),
            properties=properties,
        )
        features.append(feature)

    geojson = FeatureCollection(features)

    # Write to file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, separators=(',', ':'))

    file_size = output_path.stat().st_size / 1024  # KB
    print(f"  ✓ Generated {len(features)} markers ({file_size:.1f} KB)")

    if file_size > 800:
        print(f"  ⚠ File size exceeds 800 KB target")

    return len(features)


def generate_search_index(
    inventory: pd.DataFrame,
    gazetteer: pd.DataFrame,
    individual: pd.DataFrame,
    symbol_instances: pd.DataFrame,
    feast_canonical: pd.DataFrame,
    output_path: Path,
) -> None:
    """Generate compact search index for Fuse.js."""
    print("Generating search_docs.json...")

    # Denormalize gazetteer data
    merged = denormalize_gazetteer(inventory, gazetteer)

    # Parse years
    merged[['year_min', 'year_max']] = merged['year'].apply(
        lambda y: pd.Series(parse_year_range(y))
    )
    merged[['period_en', 'period_sv']] = merged.apply(
        lambda row: pd.Series(assign_period_bucket(row['year_min'], row['year_max'])), axis=1
    )

    # Get top feasts per calendar
    feast_map = {}
    if not feast_canonical.empty and 'canonical_id' in feast_canonical.columns:
        canonical_names = dict(zip(feast_canonical['canonical_id'], feast_canonical['canonical_name']))
        for cal_id, group in individual.groupby('cal_id'):
            feast_ids = group['fest_canonical_id'].dropna()
            top_feasts = [
                canonical_names.get(fid, fid)
                for fid, _ in Counter(feast_ids).most_common(5)
            ]
            feast_map[cal_id] = top_feasts

    # Get top symbols per calendar
    symbol_map = {}
    for cal_id, group in symbol_instances.groupby('cal_id'):
        top_symbols = [sym for sym, _ in Counter(group['symbol_type'].dropna()).most_common(5)]
        symbol_map[cal_id] = top_symbols

    docs = []
    for _, row in merged.iterrows():
        cal_id = row['id']
        doc = {
            'cal_id': cal_id,
            'catalog': row.get('cal_label', ''),
            'institute_name': row.get('institute', ''),
            'diocese_name': row.get('diocese_name', ''),
            'location_name': row.get('location_name', ''),
            'socken': row.get('socken', ''),
            'year_min': row['year_min'] if not pd.isna(row['year_min']) else None,
            'year_max': row['year_max'] if not pd.isna(row['year_max']) else None,
            'period_bucket_en': row['period_en'],
            'period_bucket_sv': row['period_sv'],
            'signals_symbols': symbol_map.get(cal_id, []),
            'signals_feasts': feast_map.get(cal_id, []),
        }
        docs.append(doc)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(docs, f, ensure_ascii=False, separators=(',', ':'))

    print(f"  ✓ Generated {len(docs)} search documents")


def generate_stats(
    inventory: pd.DataFrame,
    gazetteer: pd.DataFrame,
    symbol_instances: pd.DataFrame,
    symbol_types: pd.DataFrame,
    symbol_categories: dict,
    output_path: Path,
) -> None:
    """Generate global statistics for charts."""
    print("Generating stats.json...")

    # Denormalize gazetteer data
    merged = denormalize_gazetteer(inventory, gazetteer)

    # Parse years and assign periods
    merged[['year_min', 'year_max']] = merged['year'].apply(
        lambda y: pd.Series(parse_year_range(y))
    )
    merged[['period_en', 'period_sv']] = merged.apply(
        lambda row: pd.Series(assign_period_bucket(row['year_min'], row['year_max'])), axis=1
    )

    stats = {
        'total_calendars': len(inventory),
        'by_period_en': dict(Counter(merged['period_en'])),
        'by_period_sv': dict(Counter(merged['period_sv'])),
        'by_diocese': dict(Counter(merged['diocese_name'].dropna())),
        'by_material': dict(Counter(merged['material_primary'].dropna())),
        'by_shape': dict(Counter(merged['shape'].dropna())),
    }

    # Symbol category counts
    category_counts = defaultdict(int)
    for cal_flags in symbol_categories.values():
        for category, has_it in cal_flags.items():
            if has_it:
                category_counts[category] += 1

    stats['by_symbol_category'] = dict(category_counts)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(f"  ✓ Generated statistics")


def generate_per_calendar_data(
    inventory: pd.DataFrame,
    individual: pd.DataFrame,
    symbol_instances: pd.DataFrame,
    gazetteer: pd.DataFrame,
    symbol_categories: dict,
    output_dir: Path,
    embed_threshold_kb: int = 30,
) -> dict:
    """
    Generate per-calendar JSON data.

    Returns:
        dict mapping cal_id -> JSON string (for embedding or file writing)
    """
    print(f"Generating per-calendar data (embed threshold: {embed_threshold_kb}KB)...")

    calendar_data = {}
    large_calendars = []

    for cal_id in inventory['id']:
        # Get inventory row
        inv_row = inventory[inventory['id'] == cal_id].iloc[0].to_dict()

        # Get individual rows
        individual_rows = individual[individual['cal_id'] == cal_id].fillna('').to_dict('records')

        # Get symbols
        symbols = symbol_instances[symbol_instances['cal_id'] == cal_id]

        symbol_type_counts = dict(Counter(symbols['symbol_type'].dropna()))
        category_counts = symbol_categories.get(cal_id, {})

        # Co-occurring symbols (same day)
        # NOTE: symbol_instances doesn't have day_of_year, so we can't compute co-occurrences
        # If needed in the future, we'd need to join with individual table
        top_pairs = []

        # Complex markings (tertiary modifiers)
        # NOTE: symbol_instances doesn't have day_of_year column
        complex_days = []

        # Writing texts
        writing_texts = symbols[symbols['writing_text'].notna()]['writing_text'].unique()[:25].tolist()

        # Location info
        location_info = {}
        if pd.notna(inv_row.get('location_id')):
            gaz_row = gazetteer[gazetteer['geoid'] == inv_row['location_id']]
            if not gaz_row.empty:
                gaz = gaz_row.iloc[0]
                # Also get diocese name if available
                diocese_name = ''
                if pd.notna(inv_row.get('diocese_id')):
                    diocese_row = gazetteer[gazetteer['geoid'] == inv_row['diocese_id']]
                    if not diocese_row.empty:
                        diocese_name = diocese_row.iloc[0]['name']

                location_info = {
                    'location_name': gaz.get('name', ''),
                    'diocese_name': diocese_name,
                    'latitude': float(gaz['latitude']) if pd.notna(gaz.get('latitude')) else None,
                    'longitude': float(gaz['longitude']) if pd.notna(gaz.get('longitude')) else None,
                }

        data = {
            'inventory': inv_row,
            'individual': individual_rows,
            'symbols': {
                'by_type': symbol_type_counts,
                'by_category': category_counts,
                'top_co_occurring_pairs': top_pairs,
                'complex_days': complex_days,
                'writing_texts': writing_texts,
            },
            'location': location_info,
        }

        json_str = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
        json_size_kb = len(json_str.encode('utf-8')) / 1024

        calendar_data[cal_id] = json_str

        if json_size_kb > embed_threshold_kb:
            large_calendars.append((cal_id, json_size_kb))

    # Write large calendars to separate files
    if large_calendars:
        cal_dir = output_dir / 'calendars'
        cal_dir.mkdir(parents=True, exist_ok=True)

        for cal_id, size_kb in large_calendars:
            cal_file = cal_dir / f'{cal_id}.json'
            with open(cal_file, 'w', encoding='utf-8') as f:
                f.write(calendar_data[cal_id])

        print(f"  ✓ Wrote {len(large_calendars)} large calendars to separate files")

    print(f"  ✓ Generated data for {len(calendar_data)} calendars")
    return calendar_data


def main():
    parser = argparse.ArgumentParser(description='Prepare data for static site')
    parser.add_argument('--data-dir', type=Path, required=True)
    parser.add_argument('--release-dir', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()

    data_dir = args.data_dir
    release_dir = args.release_dir
    output_dir = args.output_dir

    if not data_dir.exists():
        print(f"ERROR: Data directory not found: {data_dir}")
        sys.exit(1)

    print("Loading TSV files...")
    inventory = pd.read_csv(data_dir / 'inventory.tsv', sep='\t', dtype=str, keep_default_na=False)
    individual = pd.read_csv(data_dir / 'individual.tsv', sep='\t', dtype=str, keep_default_na=False)
    gazetteer = pd.read_csv(data_dir / 'gazetteer.tsv', sep='\t', keep_default_na=False)
    symbol_instances = pd.read_csv(
        data_dir / 'generated' / 'symbol_instances.tsv', sep='\t', dtype=str, keep_default_na=False
    )

    # Load lookups
    symbol_types = pd.read_csv(
        data_dir / 'lookups' / 'symbol_types.tsv', sep='\t', dtype=str, keep_default_na=False
    )
    feast_canonical = pd.read_csv(
        data_dir / 'lookups' / 'feast_canonical.tsv', sep='\t', dtype=str, keep_default_na=False
    )

    print(f"  Loaded {len(inventory)} calendars")
    print(f"  Loaded {len(individual)} daily entries")
    print(f"  Loaded {len(gazetteer)} locations")
    print(f"  Loaded {len(symbol_instances)} symbol instances")

    # Compute symbol categories
    print("\nComputing symbol categories...")
    symbol_categories = compute_symbol_categories(symbol_instances, symbol_types)
    print(f"  ✓ Computed categories for {len(symbol_categories)} calendars")

    # Generate outputs
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 60)
    generate_map_markers(
        inventory,
        gazetteer,
        individual,
        symbol_categories,
        output_dir / 'map_markers.geojson',
    )

    generate_search_index(
        inventory,
        gazetteer,
        individual,
        symbol_instances,
        feast_canonical,
        output_dir / 'search_docs.json',
    )

    generate_stats(
        inventory, gazetteer, symbol_instances, symbol_types, symbol_categories, output_dir / 'stats.json'
    )

    calendar_data = generate_per_calendar_data(
        inventory,
        individual,
        symbol_instances,
        gazetteer,
        symbol_categories,
        output_dir,
    )

    # Save calendar data index
    calendar_index = {
        cal_id: {
            'size_kb': len(json_str.encode('utf-8')) / 1024,
            'external': len(json_str.encode('utf-8')) / 1024 > 30,
        }
        for cal_id, json_str in calendar_data.items()
    }

    with open(output_dir / 'calendar_index.json', 'w', encoding='utf-8') as f:
        json.dump(calendar_index, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print("✓ Data preparation complete")


if __name__ == '__main__':
    main()
