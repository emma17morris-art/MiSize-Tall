import csv
import json
from datetime import datetime

# Load existing data
try:
    with open('tall_sizes_complete.json', 'r', encoding='utf-8') as f:
        result = json.load(f)
    print(f"✅ Loaded existing data for {len(result)} brands")
except FileNotFoundError:
    result = {}
    print("ℹ️  Starting fresh")

# Import from CSV
with open('Tall_Sizes_Master.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        brand = row.get('Brand', '').strip()
        if not brand:
            continue
        
        # Get authenticity and source from CSV
        authenticity = row.get('Authenticity', '').strip() or "⚠️ Generic (UK standard used)"
        source_note = row.get('Source Note', '').strip() or f"Imported from Tall_Sizes_Master.csv on {datetime.now().strftime('%Y-%m-%d')}"
        
        # Initialize brand if new
        if brand not in result:
            result[brand] = {
                "name": brand,
                "authenticity": authenticity,
                "sourceNote": source_note,
                "categories": {},
                "notes": {},
                "lastUpdated": datetime.now().isoformat()
            }
        else:
            # Update metadata for existing brands
            result[brand]["authenticity"] = authenticity
            result[brand]["sourceNote"] = source_note
            result[brand]["lastUpdated"] = datetime.now().isoformat()
        
        # Determine gender
        gender = row.get('Gender', '').strip()
        section = row.get('Section', '').strip()
        
        # For now, create all the clothing categories for each brand
        # Later you can add specific data for each type
        if gender == 'Women' or section == 'WOMEN':
            categories_to_create = [
                "Women's Tall Jeans",
                "Women's Dresses",
                "Women's Tops",
                "Women's Shirts",
                "Women's Jumpers",
                "Women's Skirts"
            ]
        elif gender == 'Men' or section == 'MEN':
            categories_to_create = [
                "Men's Tall Jeans",
                "Men's Shirts",
                "Men's T-Shirts",
                "Men's Tops",
                "Men's Jumpers"
            ]
        else:
            continue
        
        if "categories" not in result[brand]:
            result[brand]["categories"] = {}
        
        # Get size data
        uk_size = row.get('UK Size', '').strip()
        if not uk_size:
            continue
        
        size_label = f"{uk_size} Tall"
        size_data = {}
        
        # Get measurements
        try:
            waist = float(row.get('Waist (in)', 0))
            if waist:
                size_data["waist"] = round(waist, 1)
        except:
            pass
        
        try:
            hips = float(row.get('Hips (in)', 0))
            if hips:
                size_data["hips"] = round(hips, 1)
        except:
            pass
        
        try:
            bust = float(row.get('Bust (in)', 0))
            if bust:
                size_data["bust"] = round(bust, 1)
                size_data["chest"] = round(bust, 1)
        except:
            pass
        
        inseam_str = row.get('Inside Leg (in)', '')
        if inseam_str:
            import re
            numbers = [float(n) for n in re.findall(r'\d+(?:\.\d+)?', inseam_str)]
            if numbers:
                size_data["inseam"] = round(max(numbers), 1)
        
        if size_data:
            # Add the same size data to all categories for this brand
            for category in categories_to_create:
                if category not in result[brand]["categories"]:
                    result[brand]["categories"][category] = {}
                result[brand]["categories"][category][size_label] = size_data.copy()

# Save
with open('tall_sizes_complete.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"✅ Updated {len(result)} brands in tall_sizes_complete.json")

# Print summary
all_categories = {}
for brand_data in result.values():
    if 'categories' in brand_data:
        for cat in brand_data['categories'].keys():
            all_categories[cat] = all_categories.get(cat, 0) + 1

print(f"\n📊 Categories in database:")
for cat in sorted(all_categories.keys()):
    print(f"  - {cat}: {all_categories[cat]} brands")
