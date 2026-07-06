# SDG Scraper

Archived research automation for checking journal availability in Saint Joseph's University Primo and collecting article metadata for SDG-oriented analysis.

This was an early end-to-end scraper that combined journal lists, ISSN search, browser automation, Primo export workflows, and CSV/JSON compilation. It is preserved as a portfolio artifact because it shows the practical machinery behind a real research workflow: brittle web systems, pagination, exported records, metadata normalization, and downstream scoring inputs.

## What It Does

- Searches SJU Primo by print ISSN or E-ISSN for journal availability.
- Automates Primo result navigation with Selenium.
- Exports article search results for later analysis.
- Merges exported CSV files into normalized article metadata tables.
- Uses Scopus journal lists as the source set for availability checks.

## Repository Layout

- `scraper.py` - first version using `requests-html` for ISSN availability checks.
- `scraperv2.py` - Selenium-based scraper/export workflow and CSV merge helpers.
- `scopusjournals.csv` - source journal list with print ISSN and E-ISSN fields.
- `journals.csv` - smaller journal query list used during development.

Generated exports such as `output.csv`, `results.json`, browser downloads, and directory data are intentionally not tracked.

## Requirements

Python 3.10+ is recommended.

Install dependencies with:

```bash
pip install -r requirements.txt
```

The Selenium workflow requires Chrome and a compatible ChromeDriver. `webdriver-manager` can install the driver automatically.

## Configuration

Copy `.env.example` to `.env` if you want to override local paths:

```bash
cp .env.example .env
```

Supported variables:

- `SDG_DOWNLOAD_DIR` - directory where browser exports should be downloaded.
- `SDG_MERGE_INPUT_DIR` - directory containing exported CSVs to merge.

## Usage Notes

This repository is an archived project, not a maintained package. The scripts target SJU Primo pages and XPath selectors as they existed during the original project, so the selectors may need updates before running against the current site.

The public version excludes credentials, student directory scraping code, generated exports, and any directory output containing personal information.

## Status

Archived. Published to show the implementation approach and project shape.
