import csv
import json
from datetime import datetime

# Category mapping from CSV to proper categories
CATEGORY_MAPPING = {
    # Women's categories
    'Women Jeans': "Women's Tall Jeans",
    'Women Dresses': "Women's Dresses",
    'Women Tops': "Women's Tops",
    'Women Shirts': "Women's Shirts",
    'Women Jumpers': "Women's Jumpers",
    'Women Skirts': "Women's Skirts",
    
    # Men's categories
    'Men Jeans': "Men's Tall Jeans",
    'Men Shirts': "Men's Shirts",
    'Men T-Shirts': "Men's T-Shirts",
    'Men Tops': "Men's Tops",
    'Men Jumpers': "Men's Jumpers",
}

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
        
        # Determine gender and category
        gender = row.get('Gender', '').strip()
        label_type = row.get('Label/Type', '').strip()
        
        # Map to proper category
        category = None
        if gender == 'Women':
            if 'Jean' in label_type or 'Trouser' in label_type:
                category = "Women's Tall Jeans"
            elif 'Dress' in label_type:
                category = "Women's Dresses"
            elif 'Top' in label_type or 'Blouse' in label_type:
                category = "Women's Tops"
            elif 'Shirt' in label_type:
                category = "Women's Shirts"
            elif 'Jumper' in label_type or 'Sweater' in label_type:
                category = "Women's Jumpers"
            elif 'Skirt' in label_type:
                category = "Women's Skirts"
            else:
                category = "Women's Tall Jeans"  # Default
                
        elif gender == 'Men':
            if 'Jean' in label_type or 'Trouser' in label_type:
                category = "Men's Tall Jeans"
            elif 'Shirt' in label_type and 'T-Shirt' not in label_type:
                category = "Men's Shirts"
            elif 'T-Shirt' in label_type or 'Tee' in label_type:
                category = "Men's T-Shirts"
            elif 'Top' in label_type:
                category = "Men's Tops"
            elif 'Jumper' in label_type or 'Sweater' in label_type:
                category = "Men's Jumpers"
            else:
                category = "Men's Tall Jeans"  # Default
        
        if not category:
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
                size_data["chest"] = round(bust, 1)  # Add both names
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
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"✅ Updated {len(result)} brands in tall_sizes_complete.json")

# Print summary of categories found
all_categories = set()
for brand_data in result.values():
    if 'categories' in brand_data:
        all_categories.update(brand_data['categories'].keys())

print(f"\n📊 Categories in database:")
for cat in sorted(all_categories):
    count = sum(1 for b in result.values() if cat in b.get('categories', {}))
    print(f"  - {cat}: {count} brands")
