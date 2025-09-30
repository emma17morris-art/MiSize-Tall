import os
import json
import yaml
import importlib
import pandas as pd

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BRANDS_FILE = os.path.join(BASE_DIR, "brands.yml")
JSON_FILE = os.path.join(BASE_DIR, "uk_brands.json")
CSV_FILE = os.path.join(BASE_DIR, "uk_brands.csv")

# Load brands.yml
with open(BRANDS_FILE, "r") as f:
    brands = yaml.safe_load(f)

all_data = {}

for brand in brands:
    name = brand.get("name")
    url = brand.get("url")
    extractor = brand.get("extractor")

    print(f"Scraping {name} ...")

    try:
        # dynamically import extractor
        module = importlib.import_module("all_brands")
        extract_func = getattr(module, extractor)
        result = extract_func(url)

        all_data[name] = {
            "url": url,
            "sizes": result.get("sizes", []),
        }
        print(f"✅ Success: {name}")

    except Exception as e:
        print(f"❌ Failed to scrape {name}: {e}")
        all_data[name] = {"url": url, "sizes": []}

# Save JSON
with open(JSON_FILE, "w") as f:
    json.dump(all_data, f, indent=2)

print(f"✅ Saved {JSON_FILE}")

# Save CSV (flatten sizes into a DataFrame)
rows = []
for brand, data in all_data.items():
    for size in data["sizes"]:
        row = {"brand": brand, **size}
        rows.append(row)

if rows:
    df = pd.DataFrame(rows)
    df.to_csv(CSV_FILE, index=False)
    print(f"✅ Saved {CSV_FILE}")
else:
    print("⚠️ No size data found — CSV not created")
