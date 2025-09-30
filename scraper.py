#!/usr/bin/env python3
import importlib
import yaml
import json
import pandas as pd
from datetime import datetime
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
BRANDS_YML = BASE_DIR / "brands.yml"
OUTPUT_JSON = BASE_DIR / "uk_brands.json"
OUTPUT_CSV = BASE_DIR / "uk_brands.csv"

def load_brands():
    """Load all brands from brands.yml"""
    with open(BRANDS_YML, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("brands", [])

def run_extractor(extractor_path: str, url: str):
    """
    Dynamically import extractor from all_brands.py and run it
    Example: "all_brands.extract_asos"
    """
    module_name, func_name = extractor_path.split(".")
    module = importlib.import_module(module_name)
    extractor_func = getattr(module, func_name)
    return extractor_func(url)

def normalise_result(brand_conf, raw_result):
    """
    Ensure every extractor returns a unified schema
    """
    return {
        "brand": brand_conf["brand"],
        "category": brand_conf["category"],
        "range": brand_conf["range"],
        "url": brand_conf["url"],
        "sizes": raw_result.get("sizes", []),
        "lastUpdated": datetime.utcnow().isoformat() + "Z"
    }

def main():
    brands = load_brands()
    brand_db = {}
    csv_rows = []

    for brand_conf in brands:
        print(f"Scraping {brand_conf['brand']} ({brand_conf['category']}) ...")
        try:
            raw = run_extractor(brand_conf["extractor"], brand_conf["url"])
            normalised = normalise_result(brand_conf, raw)

            # Store in DB
            if brand_conf["brand"] not in brand_db:
                brand_db[brand_conf["brand"]] = {
                    "categories": {},
                    "lastUpdated": normalised["lastUpdated"]
                }

            brand_db[brand_conf["brand"]]["categories"][brand_conf["category"]] = {
                "range": brand_conf["range"],
                "sizes": normalised["sizes"],
                "url": brand_conf["url"]
            }

            # Flatten for CSV
            for size in normalised["sizes"]:
                row = {
                    "brand": brand_conf["brand"],
                    "category": brand_conf["category"],
                    "range": brand_conf["range"],
                    **size
                }
                csv_rows.append(row)

        except Exception as e:
            print(f"❌ Failed to scrape {brand_conf['brand']}: {e}")

    # Save JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(brand_db, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {OUTPUT_JSON}")

    # Save CSV
    if csv_rows:
        df = pd.DataFrame(csv_rows)
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"✅ Saved {OUTPUT_CSV}")

if __name__ == "__main__":
    main()

