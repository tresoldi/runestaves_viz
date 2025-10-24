"""
Data validation schemas for Runestaves data files.

Uses Pandera for robust TSV validation with clear error reporting.
Critical fields are strictly validated; optional fields allow nulls.
"""

import pandera as pa
from pandera import Column, DataFrameSchema, Check


# Inventory schema - core calendar metadata
inventory_schema = DataFrameSchema(
    {
        # Critical identification fields
        "id": Column(str, nullable=False, unique=True),
        "cal_label": Column(str, nullable=False),

        # Provenance (critical)
        "institute": Column(str, nullable=True),
        "location_id": Column(str, nullable=True),
        "diocese_id": Column(str, nullable=True),

        # Estimation flags
        "location_estimate": Column(pa.Bool, nullable=True, coerce=True),
        "socken_estimate": Column(pa.Bool, nullable=True, coerce=True),
        "diocese_estimate": Column(pa.Bool, nullable=True, coerce=True),

        # Physical attributes
        "shape": Column(str, nullable=True),
        "sides": Column(pa.Int, nullable=True, checks=Check.in_range(1, 8)),
        "material_primary": Column(str, nullable=True),
        "material_secondary1": Column(str, nullable=True),
        "material_secondary2": Column(str, nullable=True),

        # Dating
        "year": Column(str, nullable=True),
        "year_estimate": Column(pa.Bool, nullable=True, coerce=True),

        # Notation systems
        "solar": Column(str, nullable=True),
        "solar_a": Column(str, nullable=True),
        "solar_b": Column(str, nullable=True),

        # Data quality
        "completed": Column(str, nullable=True),
        "f_corr": Column(str, nullable=True),
        "damage": Column(str, nullable=True),
    },
    strict=False,  # Allow additional columns
    coerce=True,
)


# Individual (daily entries) schema
individual_schema = DataFrameSchema(
    {
        # Critical: links to calendar
        "cal_id": Column(str, nullable=False),

        # Date identification
        "month": Column(pa.Int, nullable=True, checks=Check.in_range(1, 12)),
        "day": Column(pa.Int, nullable=True, checks=Check.in_range(1, 31)),
        "day_of_year": Column(pa.Int, nullable=True, checks=Check.in_range(1, 366)),

        # Feast information
        "fest": Column(str, nullable=True),
        "fest_canonical_id": Column(str, nullable=True),
        "fest_canonical": Column(str, nullable=True),
        "fest_type": Column(str, nullable=True),

        # Calendar systems
        "golden_number": Column(str, nullable=True),
        "sunday_letter": Column(str, nullable=True),
        "rune": Column(str, nullable=True),
        "fest_mark": Column(str, nullable=True),

        # Notes
        "notes": Column(str, nullable=True),
    },
    strict=False,
    coerce=True,
)


# Symbol instances schema
symbol_instances_schema = DataFrameSchema(
    {
        "symbol_id": Column(str, nullable=False),
        "cal_id": Column(str, nullable=False),
        "original_index": Column(str, nullable=True),
        "position": Column(str, nullable=True),
        "presentation": Column(str, nullable=True),
        "symbol_type": Column(str, nullable=True),
        "primary_modifier": Column(str, nullable=True),
        "secondary_modifier": Column(str, nullable=True),
        "tertiary_modifier": Column(str, nullable=True),
        "writing_text": Column(str, nullable=True),
    },
    strict=False,
    coerce=True,
)


# Gazetteer schema - location data with coordinates
gazetteer_schema = DataFrameSchema(
    {
        "geoid": Column(str, nullable=False, unique=True),
        "name": Column(str, nullable=False),
        "level": Column(str, nullable=True),
        "latitude": Column(pa.Float, nullable=True, checks=Check.in_range(-90, 90)),
        "longitude": Column(pa.Float, nullable=True, checks=Check.in_range(-180, 180)),
        "coord_source": Column(str, nullable=True),
        "accuracy": Column(str, nullable=True),  # exact, estimated, unknown
    },
    strict=False,
    coerce=True,
)


# Symbol types lookup with categories
symbol_types_schema = DataFrameSchema(
    {
        "symbol_type": Column(str, nullable=False, unique=True),
        "category": Column(str, nullable=True),  # religious, agricultural, etc.
        "description": Column(str, nullable=True),
        "frequency": Column(str, nullable=True),
        "status": Column(str, nullable=True),
    },
    strict=False,
    coerce=True,
)


# Feast canonical lookup
feast_canonical_schema = DataFrameSchema(
    {
        "canonical_id": Column(str, nullable=False, unique=True),
        "canonical_name": Column(str, nullable=False),
        "primary_saint": Column(str, nullable=True),
        "alternative_saints": Column(str, nullable=True),
        "vernacular": Column(str, nullable=True),
        "latin": Column(str, nullable=True),
        "feast_type": Column(str, nullable=True),
        "wikidata_id": Column(str, nullable=True),
        "num_variants": Column(str, nullable=True),
    },
    strict=False,
    coerce=True,
)


# Configuration for validation behavior
class ValidationConfig:
    """Controls validation strictness and error handling."""

    # Critical fields that must be valid
    CRITICAL_SCHEMAS = {
        'inventory': ['id', 'cal_label'],
        'individual': ['cal_id'],
        'gazetteer': ['geoid', 'name'],
    }

    # Symbol categories for classification
    SYMBOL_CATEGORIES = [
        'religious',
        'liturgical',
        'royal',
        'agricultural',
        'tools',
        'occupational',
        'drinking',
        'animals',
        'human',
        'plants',
        'geometric',
        'natural_phenomena',
        'text',
        'notation',
        'generic',
    ]

    # Period buckets for dating
    PERIOD_BUCKETS = [
        ('Medieval', 'Medeltid', 0, 1527),
        ('16th century', '1500-talet', 1528, 1600),
        ('17th century', '1600-talet', 1601, 1700),
        ('18th century', '1700-talet', 1701, 1800),
        ('19th century', '1800-talet', 1801, 1900),
        ('Unknown', 'Okänt', None, None),
    ]


def validate_dataframe(df, schema, name: str, strict: bool = False):
    """
    Validate a DataFrame against a schema.

    Args:
        df: DataFrame to validate
        schema: Pandera schema
        name: Name for error messages
        strict: If True, raise on any error; if False, warn and continue

    Returns:
        Validated DataFrame (potentially coerced)

    Raises:
        pa.errors.SchemaError: If strict=True and validation fails
    """
    try:
        validated = schema.validate(df, lazy=True)
        print(f"✓ {name} validated successfully ({len(df)} rows)")
        return validated
    except pa.errors.SchemaErrors as err:
        print(f"⚠ {name} validation warnings:")
        print(err.failure_cases)

        if strict:
            raise
        else:
            print(f"  Continuing with {len(df)} rows (some may have issues)")
            return df
