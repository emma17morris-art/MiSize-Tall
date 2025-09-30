# MiSize Data Scraper Guide

This repository contains the MiSize single-page demo (`index.html`) and a small
Python helper (`scraper.py`) that can either export the embedded
`BRAND_SIZE_DATABASE` object or guide you through manually entering authentic
measurements. The current database values are illustrative **demo** numbers; the
extractor does not crawl any brand website. Use this guide to understand how to
run the available commands, how to verify the generated `uk_brands.json`, and
what to tackle next once you have fresh data.

## 1. Prerequisites

* Python 3.9+ (the script only depends on the standard library)
* The `index.html` file with the up-to-date `BRAND_SIZE_DATABASE`
* Write access to the repository so the generated `uk_brands.json` can be saved

## 2. Running the scraper

```bash
python scraper.py --help                         # view available commands
python scraper.py extract                        # export data from index.html
python scraper.py extract --input other.html --output data.json
python scraper.py extract --check-demo-data      # highlight placeholder copy
python scraper.py manual                         # enter real measurements
python scraper.py manual --output authentic.json # choose where to save results
```

Both commands report how many brands were saved. Re-run `extract` whenever the
inline JavaScript data changes, and use `manual` whenever you collect new
measurements from official sources.

## 3. Capturing authentic measurements manually

1. Launch `python scraper.py manual`.
2. Follow the prompts for each brand. You will be asked for the brand name,
   categories (e.g. "Women's Jeans"), sizes, and the measurements that apply to
   each size. All values are stored as numbers in the resulting JSON.
3. Provide the verification details when prompted: a timestamp (defaulting to
   the current UTC time), the source URL, publication date, and any fit notes.
4. Repeat the process for as many brands as you need, then press Enter at the
   brand prompt to finish. The tool will merge the entries with any existing
   data in `uk_brands.json`.

You can interrupt the session with `Ctrl+C`—all information collected up to that
point will still be saved when you exit the prompts.

## 4. Validating the output

1. Inspect the top of `uk_brands.json` to confirm the top-level brand keys look
   correct.
2. Run the MiSize app (open `index.html` in a browser). Use the developer tools
   network tab and confirm a request for `uk_brands.json` returns HTTP 200.
3. Trigger a size lookup in the UI and ensure results still appear.

If any of these checks fail, delete the JSON file and regenerate it after fixing
issues in `index.html`.

## 5. Keeping the dataset stable

`index.html` defines `updatedAt: new Date().toISOString()` for each brand. When
you run the scraper this is converted to a timestamp captured at the time of
extraction. To avoid noisy commits:

* Run the scraper only when the underlying measurements actually change.
* Commit the regenerated JSON together with the `index.html` edits that
  motivated it so reviewers can see both sides of the update.

## 6. Suggested next steps

* Replace placeholder measurements with real brand data before exporting.
* Extend the scraper to emit additional metadata (e.g. regional availability or
  footnotes) if you add them to `index.html`.
* Add automated tests (for example with `pytest`) that compare the scraped data
  against a schema to catch accidental format changes early.

## 7. Preparing authentic data

The included dataset should be treated as a template. To ship real
recommendations:

1. **Collect sources:** Visit each brand's official size guide and capture the
   measurement tables for the categories you want to support. Record the source
   URL and the publication date.
2. **Normalise units:** Convert all measurements to the same unit system (e.g.
   centimetres) and round only when necessary. Document any assumptions you
   apply when translating between unit systems or between body and garment
   measurements.
3. **Update `index.html`:** Replace the demo values in `BRAND_SIZE_DATABASE`
   with the verified measurements, including metadata such as `sourceUrl` and
   `sourceDate` so future maintainers can revalidate the entries.
4. **Export and review:** Run `python scraper.py --check-demo-data` to write a
   new JSON export and surface any lingering demo placeholders. Review the
   diff to ensure the new figures match your sources.
5. **Archive evidence:** Keep a copy of the original brand size guide (PDF or
   screenshot) alongside the commit so auditors can trace the numbers back to
   their origin.

Following this process transforms the demo extractor into a reliable bridge
between official brand data and the MiSize experience.

Following these steps should leave you with a clean JSON dataset that the MiSize
UI can load without relying on the inline script blob.

## 8. Updating your repository with these changes

This workspace does not push commits directly to your own Git hosting service.
To incorporate the updated scraper workflow and documentation into your
repository:

1. **Fetch the patch:** download the generated diff or copy the relevant file
   changes (for example by copying the updated `scraper.py`, `uk_brands.json`,
   and this README section).
2. **Apply the edits locally:** paste the copied content into the matching files
   within your local checkout or use `git apply <patch-file>` if you saved the
   diff output as a patch.
3. **Review the changes:** run `git status` and `git diff` to make sure the
   updates look correct and no unrelated files were touched.
4. **Test the workflow:** execute `python scraper.py`, `python scraper.py
   manual`, or any other relevant command to confirm everything works in your
   environment.
5. **Commit and push:** stage the files (`git add README.md scraper.py
   uk_brands.json`), create a commit message, and push it to your remote so the
   rest of your team can review or deploy the update.

Keeping your local repository in sync with these steps ensures you stay in
control of when the new scraper functionality lands in production.
