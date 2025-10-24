#!/usr/bin/env python3
"""
Validate Runestaves TSV data files.

Validates all input TSV files against schemas, checking for:
- Required fields present
- Data types correct
- Value ranges valid
- Referential integrity between files

Runs as part of site-prepare pipeline.
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

from schemas import (
    ValidationConfig,
    feast_canonical_schema,
    gazetteer_schema,
    individual_schema,
    inventory_schema,
    symbol_instances_schema,
    symbol_types_schema,
    validate_dataframe,
)


def load_tsv(path: Path, name: str) -> pd.DataFrame:
    """Load a TSV file with standard settings."""
    if not path.exists():
        print(f"⚠ {name} not found: {path}")
        return pd.DataFrame()

    df = pd.read_csv(path, sep='\t', dtype=str, keep_default_na=False)
    print(f"  Loaded {name}: {len(df)} rows, {len(df.columns)} columns")
    return df


def check_referential_integrity(
    inventory: pd.DataFrame,
    individual: pd.DataFrame,
    gazetteer: pd.DataFrame,
    symbol_instances: pd.DataFrame,
) -> bool:
    """Check that foreign key relationships are valid."""
    print("\nChecking referential integrity...")
    all_valid = True

    # Check individual.cal_id → inventory.id
    if not individual.empty and not inventory.empty:
        individual_ids = set(individual['cal_id'].unique())
        inventory_ids = set(inventory['id'].unique())
        orphan_ids = individual_ids - inventory_ids

        if orphan_ids:
            print(f"  ⚠ Found {len(orphan_ids)} calendar IDs in individual.tsv not in inventory.tsv")
            print(f"    Examples: {list(orphan_ids)[:5]}")
            all_valid = False
        else:
            print(f"  ✓ All individual entries reference valid calendars")

    # Check symbol_instances.cal_id → inventory.id
    if not symbol_instances.empty and not inventory.empty:
        symbol_ids = set(symbol_instances['cal_id'].unique())
        orphan_ids = symbol_ids - inventory_ids

        if orphan_ids:
            print(f"  ⚠ Found {len(orphan_ids)} calendar IDs in symbol_instances.tsv not in inventory.tsv")
            all_valid = False
        else:
            print(f"  ✓ All symbol instances reference valid calendars")

    # Check inventory.location_id → gazetteer.geoid
    if not inventory.empty and not gazetteer.empty:
        inv_locations = set(inventory['location_id'].dropna().unique())
        gaz_locations = set(gazetteer['geoid'].unique())
        missing_locations = inv_locations - gaz_locations

        if missing_locations:
            print(f"  ⚠ Found {len(missing_locations)} location IDs in inventory not in gazetteer")
            print(f"    Examples: {list(missing_locations)[:5]}")
            all_valid = False
        else:
            print(f"  ✓ All inventory locations found in gazetteer")

    return all_valid


def main():
    parser = argparse.ArgumentParser(description='Validate Runestaves data files')
    parser.add_argument(
        '--data-dir',
        type=Path,
        default=Path('../runestaves_data/zenodo/data'),
        help='Path to data directory containing TSV files',
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Fail on any validation error (default: warn and continue)',
    )
    args = parser.parse_args()

    data_dir = args.data_dir
    if not data_dir.exists():
        print(f"ERROR: Data directory not found: {data_dir}")
        sys.exit(1)

    print(f"Validating data from: {data_dir}")
    print("=" * 60)

    # Load all TSV files
    print("\nLoading TSV files...")
    inventory = load_tsv(data_dir / 'inventory.tsv', 'inventory')
    individual = load_tsv(data_dir / 'individual.tsv', 'individual')
    gazetteer = load_tsv(data_dir / 'gazetteer.tsv', 'gazetteer')
    symbol_instances = load_tsv(data_dir / 'generated' / 'symbol_instances.tsv', 'symbol_instances')

    # Load lookup tables
    symbol_types = load_tsv(data_dir / 'lookups' / 'symbol_types.tsv', 'symbol_types')
    feast_canonical = load_tsv(data_dir / 'lookups' / 'feast_canonical.tsv', 'feast_canonical')

    # Validate schemas
    print("\nValidating schemas...")
    all_valid = True

    try:
        inventory = validate_dataframe(inventory, inventory_schema, 'inventory', args.strict)
        individual = validate_dataframe(individual, individual_schema, 'individual', args.strict)
        gazetteer = validate_dataframe(gazetteer, gazetteer_schema, 'gazetteer', args.strict)
        symbol_instances = validate_dataframe(
            symbol_instances, symbol_instances_schema, 'symbol_instances', args.strict
        )

        if not symbol_types.empty:
            symbol_types = validate_dataframe(
                symbol_types, symbol_types_schema, 'symbol_types', args.strict
            )

        if not feast_canonical.empty:
            feast_canonical = validate_dataframe(
                feast_canonical, feast_canonical_schema, 'feast_canonical', args.strict
            )

    except Exception as e:
        print(f"\n❌ Schema validation failed: {e}")
        sys.exit(1)

    # Check referential integrity
    integrity_valid = check_referential_integrity(inventory, individual, gazetteer, symbol_instances)

    if not integrity_valid and args.strict:
        print("\n❌ Referential integrity check failed")
        sys.exit(1)

    # Summary
    print("\n" + "=" * 60)
    print("Validation Summary:")
    print(f"  Calendars: {len(inventory)}")
    print(f"  Daily entries: {len(individual)}")
    print(f"  Locations: {len(gazetteer)}")
    print(f"  Symbol instances: {len(symbol_instances)}")

    if gazetteer.empty or 'latitude' not in gazetteer.columns:
        print(f"  ⚠ Gazetteer missing or incomplete")
    else:
        valid_coords = gazetteer[
            gazetteer['latitude'].notna() & gazetteer['longitude'].notna()
        ]
        print(f"  Locations with coordinates: {len(valid_coords)}/{len(gazetteer)}")

    if all_valid and integrity_valid:
        print("\n✓ All validations passed")
        sys.exit(0)
    else:
        print("\n⚠ Some validations failed (continuing anyway)")
        sys.exit(0 if not args.strict else 1)


if __name__ == '__main__':
    main()
