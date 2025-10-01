import csv
import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time

class TallSizesScraper:
    def __init__(self, csv_file='Tall_Sizes_Master.csv', output_file='tall_sizes_complete.json'):
        self.csv_file = csv_file
        self.output_file = output_file
        self.result = {}
    
    def load_existing_data(self):
        """Load existing JSON data if it exists"""
        try:
            with open(self.output_file, 'r', encoding='utf-8') as f:
                self.result = json.load(f)
            print(f"✅ Loaded existing data for {len(self.result)} brands")
        except FileNotFoundError:
            print("ℹ️  No existing data file found, starting fresh")
    
    def import_from_csv(self):
        """Import data from CSV with metadata"""
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                brand = row.get('Brand', '').strip()
                if not brand:
                    continue
                
                # Initialize brand with metadata if not exists
                if brand not in self.result:
                    self.result[brand] = {
                        "name": brand,
                        "authenticity": "manual",
                        "sourceNote": f"Imported from {self.csv_file} on {datetime.now().strftime('%Y-%m-%d')}",
                        "categories": {},
                        "notes": {},
                        "lastUpdated": datetime.now().isoformat()
                    }
                
                # Determine category
                gender = row.get('Gender', '').strip()
                section = row.get('Section', '').strip()
                
                if gender == 'Women' or section == 'WOMEN':
                    category = "Women's Tall Jeans"
                elif gender == 'Men' or section == 'MEN':
                    category = "Men's Tall Jeans"
                else:
                    continue
                
                # Initialize category if not exists
                if category not in self.result[brand]["categories"]:
                    self.result[brand]["categories"][category] = {}
                
                # Process size data
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
                
                # Add size data if any measurements found
                if size_data:
                    self.result[brand]["categories"][category][size_label] = size_data
        
        print(f"✅ Imported data for {len(self.result)} brands from CSV")
    
    def scrape_brand(self, brand_name, url, categories=None):
        """
        Scrape a brand's website for tall sizes
        
        Args:
            brand_name: Name of the brand
            url: URL to scrape
            categories: List of categories to scrape (e.g., ["Women's Tall Jeans", "Men's Tall Jeans"])
        """
        try:
            print(f"🔍 Scraping {brand_name} from {url}...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Initialize or update brand data
            if brand_name not in self.result:
                self.result[brand_name] = {
                    "name": brand_name,
                    "authenticity": "scraped",
                    "sourceNote": f"Scraped from {url} on {datetime.now().strftime('%Y-%m-%d')}",
                    "categories": {},
                    "notes": {},
                    "lastUpdated": datetime.now().isoformat()
                }
            else:
                # Update existing brand
                self.result[brand_name]["authenticity"] = "verified"
                self.result[brand_name]["sourceNote"] = f"Verified by scraping {url} on {datetime.now().strftime('%Y-%m-%d')}"
                self.result[brand_name]["lastUpdated"] = datetime.now().isoformat()
            
            # TODO: Add your specific scraping logic here
            # This is brand-specific and would need to be customized
            # Example structure:
            """
            scraped_data = self.parse_tall_sizes(soup, categories)
            for category, sizes in scraped_data.items():
                if category not in self.result[brand_name]["categories"]:
                    self.result[brand_name]["categories"][category] = {}
                self.result[brand_name]["categories"][category].update(sizes)
            """
            
            print(f"✅ Successfully scraped {brand_name}")
            return True
            
        except requests.RequestException as e:
            print(f"❌ Error scraping {brand_name}: {e}")
            self.result[brand_name]["notes"]["scraping_error"] = str(e)
            return False
    
    def parse_tall_sizes(self, soup, categories):
        """
        Parse tall sizes from the page HTML
        This needs to be customized per website
        """
        # Example implementation - customize based on actual website structure
        sizes_data = {}
        
        # Look for size tables, divs, or other elements
        # This is highly website-specific
        
        return sizes_data
    
    def add_manual_entry(self, brand_name, category, sizes_dict, notes=None):
        """
        Manually add or update a brand entry
        
        Args:
            brand_name: Name of the brand
            category: Category (e.g., "Women's Tall Jeans")
            sizes_dict: Dictionary of sizes {size_label: {measurements}}
            notes: Optional notes about the brand
        """
        if brand_name not in self.result:
            self.result[brand_name] = {
                "name": brand_name,
                "authenticity": "manual",
                "sourceNote": f"Manually added on {datetime.now().strftime('%Y-%m-%d')}",
                "categories": {},
                "notes": {},
                "lastUpdated": datetime.now().isoformat()
            }
        
        if category not in self.result[brand_name]["categories"]:
            self.result[brand_name]["categories"][category] = {}
        
        self.result[brand_name]["categories"][category].update(sizes_dict)
        
        if notes:
            self.result[brand_name]["notes"].update(notes)
        
        self.result[brand_name]["lastUpdated"] = datetime.now().isoformat()
        
        print(f"✅ Manually added/updated {brand_name}")
    
    def save(self):
        """Save results to JSON file"""
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(self.result, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved {len(self.result)} brands to {self.output_file}")
    
    def get_brands_needing_update(self, days_old=30):
        """Find brands that haven't been updated recently"""
        needs_update = []
        cutoff = datetime.now().timestamp() - (days_old * 86400)
        
        for brand_name, brand_data in self.result.items():
            last_updated = datetime.fromisoformat(brand_data["lastUpdated"]).timestamp()
            if last_updated < cutoff:
                needs_update.append(brand_name)
        
        return needs_update


# Example usage:
if __name__ == "__main__":
    scraper = TallSizesScraper()
    
    # Option 1: Import from CSV
    scraper.import_from_csv()
    
    # Option 2: Scrape specific brands
    # scraper.scrape_brand("ASOS", "https://www.asos.com/tall/", ["Women's Tall Jeans", "Men's Tall Jeans"])
    # time.sleep(2)  # Be polite, don't hammer servers
    # scraper.scrape_brand("Long Tall Sally", "https://www.longtallsally.com/", ["Women's Tall Jeans"])
    
    # Option 3: Manually add a brand
    # scraper.add_manual_entry(
    #     "Example Brand",
    #     "Women's Tall Jeans",
    #     {
    #         "8 Tall": {"waist": 26.0, "hips": 36.0, "inseam": 36.0},
    #         "10 Tall": {"waist": 28.0, "hips": 38.0, "inseam": 36.0}
    #     },
    #     notes={"availability": "Online only", "ships_to_uk": True}
    # )
    
    # Save results
    scraper.save()
    
    # Check which brands need updating
    old_brands = scraper.get_brands_needing_update(days_old=90)
    if old_brands:
        print(f"\n⚠️  {len(old_brands)} brands haven't been updated in 90+ days:")
        for brand in old_brands[:5]:
            print(f"   - {brand}")