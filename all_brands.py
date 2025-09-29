import requests
from bs4 import BeautifulSoup
from datetime import date

def extract_asos():
    url = "https://www.asos.com/discover/size-charts/women/"
    resp = requests.get(url)
    resp.raise_for_status()  # stop if request fails
    soup = BeautifulSoup(resp.text, "html.parser")

    rows = []

    # Find the first table on the page (ASOS has multiple sections, we’ll start simple)
    table = soup.find("table")
    if not table:
        print("⚠️ No table found on ASOS page")
        return []

    headers = [th.get_text(strip=True).lower() for th in table.find_all("th")]

    for tr in table.find_all("tr")[1:]:  # skip header row
        cells = [td.get_text(strip=True) for td in tr.find_all("td")]
        if not cells:
            continue

        row = {
            "brand": "ASOS",
            "category": "Women",
            "range": "Standard",
            "uk_size": cells[0] if len(cells) > 0 else None,
            "bust_cm": cells[1] if len(cells) > 1 else None,
            "waist_cm": cells[2] if len(cells) > 2 else None,
            "hip_cm": cells[3] if len(cells) > 3 else None,
            "inseam_cm": cells[4] if len(cells) > 4 else None,
            "notes": "",
            "source_url": url,
            "source_accessed_date": str(date.today())
        }
        rows.append(row)

    return rows
