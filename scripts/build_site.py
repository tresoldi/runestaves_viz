#!/usr/bin/env python3
"""
Build static HTML site from Jinja2 templates.

This script generates all HTML pages for both Swedish and English versions,
copies assets, and creates the final static site ready for deployment.
"""

import argparse
import json
import shutil
import sys
from datetime import date
from pathlib import Path

import pandas as pd
from jinja2 import Environment, FileSystemLoader
from markdown import markdown


def load_translations(lang: str, i18n_dir: Path) -> dict:
    """Load translation dictionary for given language."""
    trans_file = i18n_dir / f'{lang}.json'
    if not trans_file.exists():
        raise FileNotFoundError(f"Translation file not found: {trans_file}")

    with open(trans_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_markdown_content(lang: str, page: str, i18n_dir: Path) -> str:
    """Load and render markdown content for a page."""
    md_file = i18n_dir / lang / f'{page}.md'
    if not md_file.exists():
        return ""

    with open(md_file, 'r', encoding='utf-8') as f:
        md_text = f.read()

    return markdown(md_text, extensions=['extra', 'codehilite'])


def build_page(
    env: Environment,
    template_name: str,
    output_path: Path,
    context: dict,
) -> None:
    """Render a template and write to output file."""
    template = env.get_template(template_name)
    html = template.render(**context)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  ✓ {output_path.relative_to(output_path.parents[1])}")


def build_calendar_pages(
    env: Environment,
    inventory: pd.DataFrame,
    calendar_data_index: dict,
    calendar_data: dict,
    site_dir: Path,
    lang: str,
    translations: dict,
    version: str,
    build_date: str,
    config: dict,
    base_path: str = '',
) -> None:
    """Build individual calendar detail pages."""
    print(f"Building calendar pages ({lang})...")

    lang_path = '' if lang == 'sv' else '/en'
    base_url = f'{base_path}{lang_path}'
    lang_switch_base = f'{base_path}/en' if lang == 'sv' else base_path
    output_subdir = 'kalendrar' if lang == 'sv' else 'en/calendars'

    for _, row in inventory.iterrows():
        cal_id = row['id']

        # Determine if data should be embedded or loaded externally
        embed_data = not calendar_data_index.get(cal_id, {}).get('external', False)

        # Parse calendar data
        cal_json = calendar_data.get(cal_id, '{}')
        cal_data = json.loads(cal_json)
        inv_data = cal_data.get('inventory', {})

        # Build context
        context = {
            't': translations,
            'lang': lang,
            'base_url': base_url,
            'lang_switch_url': f'{lang_switch_base}/{output_subdir}/{cal_id}.html',
            'version': version,
            'build_date': build_date,
            'calendar': {
                'id': cal_id,
                'catalog': row.get('cal_label', cal_id),
                'institute': inv_data.get('institute', ''),
                'location_name': cal_data.get('location', {}).get('location_name', ''),
                'diocese_name': cal_data.get('location', {}).get('diocese_name', ''),
                'material_primary': inv_data.get('material_primary', ''),
                'material_secondary': inv_data.get('material_secondary1', ''),
                'shape': inv_data.get('shape', ''),
                'sides': inv_data.get('sides', ''),
                'solar': inv_data.get('solar', ''),
                'completed': inv_data.get('completed', ''),
                'year': inv_data.get('year', ''),
                'year_min': None,  # Would need parsing
                'year_max': None,
                'period': '',  # Would need computation
                'latitude': cal_data.get('location', {}).get('latitude'),
                'longitude': cal_data.get('location', {}).get('longitude'),
            },
            'embed_data': embed_data,
            'calendar_data': cal_json if embed_data else '',
            'zenodo_url': config.get('zenodo_url', '#'),
            'zenodo_doi': config.get('zenodo_doi', ''),
            'github_url': config.get('github_url', '#'),
        }

        output_path = site_dir / output_subdir / f'{cal_id}.html'
        build_page(env, 'calendar.html', output_path, context)


def main():
    parser = argparse.ArgumentParser(description='Build static site')
    parser.add_argument('--data-dir', type=Path, required=True)
    parser.add_argument('--site-dir', type=Path, required=True)
    parser.add_argument('--base-path', type=str, default='',
                        help='Base path for deployment (e.g., /runestaves_viz for GitHub Pages)')
    args = parser.parse_args()

    data_dir = args.data_dir
    site_dir = args.site_dir
    base_path = args.base_path.rstrip('/')  # Remove trailing slash if present
    project_root = Path(__file__).parent.parent

    # Load version and build date
    version_file = project_root / 'VERSION'
    version = version_file.read_text().strip() if version_file.exists() else 'dev'
    build_date = date.today().isoformat()

    # Configuration
    config = {
        'zenodo_url': 'https://zenodo.org/record/XXXXXX',  # TODO: Update with real DOI
        'zenodo_doi': '10.5281/zenodo.XXXXXX',
        'github_url': 'https://github.com/username/runestaves_data',  # TODO: Update
        'github_viz_url': 'https://github.com/username/runestaves_viz',
    }

    # Set up Jinja2 environment
    template_dir = project_root / 'templates'
    i18n_dir = project_root / 'i18n'

    env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)

    # Load data needed for building
    print("Loading data...")
    inventory = pd.read_csv(data_dir / 'inventory.tsv', sep='\t', dtype=str, keep_default_na=False)

    # Load calendar data index
    calendar_index_file = site_dir / 'data' / 'calendar_index.json'
    if calendar_index_file.exists():
        with open(calendar_index_file, 'r', encoding='utf-8') as f:
            calendar_data_index = json.load(f)
    else:
        calendar_data_index = {}

    # Load calendar data (for embedding or reference)
    calendar_data = {}
    # For now, we'll handle this in a simplified way
    # In practice, this would load from the generated JSON files

    # Build for both languages
    for lang in ['sv', 'en']:
        print(f"\n{'=' * 60}")
        print(f"Building {lang.upper()} site")
        print('=' * 60)

        translations = load_translations(lang, i18n_dir)
        # Construct base_url with deployment base path
        lang_path = '' if lang == 'sv' else '/en'
        base_url = f'{base_path}{lang_path}'
        lang_switch_base = f'{base_path}/en' if lang == 'sv' else base_path

        # Common context for all pages
        common_context = {
            't': translations,
            'lang': lang,
            'base_url': base_url,
            'version': version,
            'build_date': build_date,
        }

        # Build home page (map)
        print("Building home page...")
        home_context = {
            **common_context,
            'lang_switch_url': f'{lang_switch_base}/',
        }
        output_path = site_dir / ('' if lang == 'sv' else 'en') / 'index.html'
        build_page(env, 'home.html', output_path, home_context)

        # Build browse page
        print("Building browse page...")
        browse_subdir = 'bladdra' if lang == 'sv' else 'browse'
        browse_context = {
            **common_context,
            'lang_switch_url': f'{lang_switch_base}/{("browse" if lang == "en" else "bladdra")}/',
        }
        output_path = site_dir / ('' if lang == 'sv' else 'en') / browse_subdir / 'index.html'
        build_page(env, 'browse.html', output_path, browse_context)

        # Build methods page
        print("Building methods page...")
        methods_content = load_markdown_content(lang, 'methods', i18n_dir)
        methods_subdir = 'metod' if lang == 'sv' else 'methods'
        methods_context = {
            **common_context,
            'lang_switch_url': f'{lang_switch_base}/{("methods" if lang == "en" else "metod")}/',
            'content': methods_content,
        }
        output_path = site_dir / ('' if lang == 'sv' else 'en') / methods_subdir / 'index.html'
        build_page(env, 'methods.html', output_path, methods_context)

        # Build about page
        print("Building about page...")
        about_content = load_markdown_content(lang, 'about', i18n_dir)
        about_subdir = 'om' if lang == 'sv' else 'about'
        about_context = {
            **common_context,
            'lang_switch_url': f'{lang_switch_base}/{("about" if lang == "en" else "om")}/',
            'content': about_content,
        }
        output_path = site_dir / ('' if lang == 'sv' else 'en') / about_subdir / 'index.html'
        build_page(env, 'about.html', output_path, about_context)

        # Build data page
        print("Building data page...")
        # Load citation from data repo
        citation_file = data_dir.parent.parent / 'CITATION.cff'
        citation_text = "Citation information will be added here"
        if citation_file.exists():
            citation_text = citation_file.read_text()

        data_context = {
            **common_context,
            'lang_switch_url': f'{lang_switch_base}/data/',
            'zenodo_url': config['zenodo_url'],
            'zenodo_doi': config['zenodo_doi'],
            'github_url': config['github_url'],
            'citation': citation_text,
        }
        output_path = site_dir / ('' if lang == 'sv' else 'en') / 'data' / 'index.html'
        build_page(env, 'data.html', output_path, data_context)

        # Build calendar pages
        # build_calendar_pages(
        #     env,
        #     inventory,
        #     calendar_data_index,
        #     calendar_data,
        #     site_dir,
        #     lang,
        #     translations,
        #     version,
        #     build_date,
        #     config,
        # )

    # Copy static assets
    print(f"\n{'=' * 60}")
    print("Copying static assets...")
    print('=' * 60)

    static_src = project_root / 'static' / 'assets'
    assets_dest = site_dir / 'assets'

    if static_src.exists():
        shutil.copytree(static_src, assets_dest, dirs_exist_ok=True)
        print(f"  ✓ Copied assets to {assets_dest.relative_to(site_dir)}")

    # Copy phylogeny images from release dir
    release_dir = data_dir.parent.parent / 'release'
    if release_dir.exists():
        for img in ['phylogeny_dendrogram.png', 'phylogeny_pca.png']:
            src = release_dir / img
            if src.exists():
                dest = assets_dest / img
                shutil.copy2(src, dest)
                print(f"  ✓ Copied {img}")

    # Create .nojekyll file
    nojekyll = site_dir / '.nojekyll'
    nojekyll.touch()
    print("  ✓ Created .nojekyll")

    print(f"\n{'=' * 60}")
    print("✓ Site build complete")
    print(f"  Output: {site_dir}")
    print('=' * 60)


if __name__ == '__main__':
    main()
