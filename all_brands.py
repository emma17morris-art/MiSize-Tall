#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (MiSize Scraper)"}

def clean_text(txt):
    if not txt:
        return None
    return txt.strip().replace("\xa0", " ")

def to_number(txt):
    try:
        return float(txt)
    except Exception:
        return None

def extract_asos(url: str):
    """
    Extract ASOS Women's size charts from the official page.
    Returns a dict with sizes and measurements.
    """
    resp = requests.get(url, headers=HEADERS, timeout=60)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    sizes = []

    # Find tables with size data
    tables = soup.find_all("table")
    for table in tables:
        headers = [clean_text(th.get_text()) for th in table.find_all("th")]
        rows = table.find_all("tr")[1:]  # skip header

        for row in rows:
            cols = [clean_text(td.get_text()) for td in row.find_all("td")]
            if not cols or len(cols) < 2:
                continue

            size_info = {}
            for h, c in zip(headers, cols):
                if not h or not c:
                    continue
                h_low = h.lower()

                if "uk" in h_low:
                    size_info["uk"] = c
                elif "bust" in h_low:
                    size_info["bust_cm"] = to_number(c.replace("cm", "").strip())
                elif "waist" in h_low:
                    size_info["waist_cm"] = to_number(c.replace("cm", "").strip())
                elif "hips" in h_low:
                    size_info["hips_cm"] = to_number(c.replace("cm", "").strip())
                elif "inside leg" in h_low or "inseam" in h_low:
                    size_info["inseam_cm"] = to_number(c.replace("cm", "").strip())

            if size_info:
                sizes.append(size_info)

    return {"sizes": sizes}
