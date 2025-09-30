# MiSize Data Scraper Guide

This repository contains the MiSize single-page demo (`index.html`) and a small
Python helper (`scraper.py`) that can extract the embedded
`BRAND_SIZE_DATABASE` object into a standalone JSON file. Use this guide to
understand when and how to run the scraper, how to verify the generated
`uk_brands.json`, and what to tackle next once you have fresh data.

## 1. Prerequisites

* Python 3.9+ (the script only depends on the standard library)
* The `index.html` file with the up-to-date `BRAND_SIZE_DATABASE`
* Write access to the repository so the generated `uk_brands.json` can be saved

## 2. Running the scraper

```bash
python scraper.py            # reads index.html and writes uk_brands.json
python scraper.py --help     # view optional flags
python scraper.py --input other.html --output data.json
```

The script reports how many brands were exported. Re-run it whenever the inline
JavaScript data changes.

## 3. Validating the output

1. Inspect the top of `uk_brands.json` to confirm the top-level brand keys look
   correct.
2. Run the MiSize app (open `index.html` in a browser). Use the developer tools
   network tab and confirm a request for `uk_brands.json` returns HTTP 200.
3. Trigger a size lookup in the UI and ensure results still appear.

If any of these checks fail, delete the JSON file and regenerate it after fixing
issues in `index.html`.

## 4. Keeping the dataset stable

`index.html` defines `updatedAt: new Date().toISOString()` for each brand. When
you run the scraper this is converted to a timestamp captured at the time of
extraction. To avoid noisy commits:

* Run the scraper only when the underlying measurements actually change.
* Commit the regenerated JSON together with the `index.html` edits that
  motivated it so reviewers can see both sides of the update.

## 5. Suggested next steps

* Replace placeholder measurements with real brand data before exporting.
* Extend the scraper to emit additional metadata (e.g. regional availability or
  footnotes) if you add them to `index.html`.
* Add automated tests (for example with `pytest`) that compare the scraped data
  against a schema to catch accidental format changes early.

Following these steps should leave you with a clean JSON dataset that the MiSize
UI can load without relying on the inline script blob.
