import yaml
import importlib
import json
import csv
import os
from datetime import date, datetime
from collections import defaultdict

# Load brand manifest
with open("brands.yml") as f:
    config = yaml.safe_load(f)

all_rows = []

# Run extractor for each brand and gather rows
for brand in config["brands"]:
    module_name, func_name = brand["extractor"].rsplit(".", 1)
    module = importlib.import_module(f"extractors.{module_name}")
    extractor = getattr(module, func_name)
    rows = extractor()
    for r in rows:
        r["source_accessed_date"] = str(date.today())
        all_rows.append(r)

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# Write flat JSON
with open("data/uk_brand_size_charts_master.json", "w", encoding="utf-8") as f:
    json.dump(all_rows, f, indent=2)

# Write flat CSV
if all_rows:
    with open("data/uk_brand_size_charts_master.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_rows[0].keys())
        writer.writeheader()
        writer.writerows(all_rows)

print(f"Wrote {len(all_rows)} rows")

# Transform flat data to nested brands/categories/sizes format
def transform_rows_to_brand_json(rows):
    brands = {}

    for r in rows:
        brand = r.get("brand")
        category = r.get("category")
        size = r.get("uk_size")

        if not (brand and category and size):
            continue  # skip incomplete rows

        if brand not in brands:
            brands[brand] = {
                "name": brand,
                "categories": {},
                "notes": {},
                "lastUpdated": datetime.utcnow().isoformat() + "Z"
            }

        if category not in brands[brand]["categories"]:
            brands[brand]["categories"][category] = {}

        measurements = {}
        for key in r:
            if key not in ("brand", "category", "uk_size"):
                measurements[key] = r[key]

        brands[brand]["categories"][category][size] = measurements

    return brands

# Apply transformation
brand_json = transform_rows_to_brand_json(all_rows)

# Save transformed JSON for frontend
with open("data/uk_brands.json", "w", encoding="utf-8") as f:
    json.dump(brand_json, f, indent=2)

print(f"Created uk_brands.json with {len(brand_json)} brands")