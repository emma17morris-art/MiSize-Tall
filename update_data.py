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
        
        # Initialize brand if new OR add missing metadata fields if existing
        if brand not in result:
            result[brand] = {
                "name": brand,
                "authenticity": "manual",
                "sourceNote": f"Imported from Tall_Sizes_Master.csv on {datetime.now().strftime('%Y-%m-%d')}",
                "categories": {},
                "notes": {},
                "lastUpdated": datetime.now().isoformat()
            }
        else:
            # Add missing metadata fields to existing brands
            if "authenticity" not in result[brand]:
                result[brand]["authenticity"] = "manual"
            if "sourceNote" not in result[brand]:
                result[brand]["sourceNote"] = f"Imported from Tall_Sizes_Master.csv on {datetime.now().strftime('%Y-%m-%d')}"
            if "notes" not in result[brand]:
                result[brand]["notes"] = {}
            result[brand]["lastUpdated"] = datetime.now().isoformat()
        
        gender = row.get('Gender', '').strip()
        section = row.get('Section', '').strip()
        
        if gender == 'Women' or section == 'WOMEN':
            category = "Women's Tall Jeans"
        elif gender == 'Men' or section == 'MEN':
            category = "Men's Tall Jeans"
        else:
            continue
        
        if "categories" not in result[brand]:
            result[brand]["categories"] = {}
            
        if category not in result[brand]["categories"]:
            result[brand]["categories"][category] = {}
        
        uk_size = row.get('UK Size', '').strip()
        if not uk_size:
            continue
        
        size_label = f"{uk_size} Tall"
        size_data = {}
        
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
        
        inseam_str = row.get('Inside Leg (in)', '')
        if inseam_str:
            import re
            numbers = [float(n) for n in re.findall(r'\d+(?:\.\d+)?', inseam_str)]
            if numbers:
                size_data["inseam"] = round(max(numbers), 1)
        
        if size_data:
            result[brand]["categories"][category][size_label] = size_data

# Save
with open('tall_sizes_complete.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2)

print(f"✅ Updated {len(result)} brands in tall_sizes_complete.json")
