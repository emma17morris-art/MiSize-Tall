import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

def extract_asos(url: str):
    """
    Scraper for ASOS women's size chart.
    (currently may timeout, but function is here)
    """
    resp = requests.get(url, headers=HEADERS, timeout=60)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    tables = soup.find_all("table")
    if not tables:
        return {"sizes": []}

    sizes = []
    for table in tables:
        headers = [th.get_text(strip=True) for th in table.find_all("th")]
        for row in table.find_all("tr")[1:]:
            cols = [td.get_text(strip=True) for td in row.find_all("td")]
            if not cols:
                continue
            size_info = dict(zip(headers, cols))
            sizes.append(size_info)

    return {"sizes": sizes}


def extract_next(url: str):
    """
    Scraper for Next women's size chart.
    Returns dict with sizes + measurements.
    """
    resp = requests.get(url, headers=HEADERS, timeout=60)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    sizes = []

    table = soup.find("table")
    if not table:
        return {"sizes": []}

    headers = [th.get_text(strip=True) for th in table.find_all("th")]
    rows = table.find_all("tr")

    for row in rows[1:]:  # skip header
        cols = [td.get_text(strip=True) for td in row.find_all("td")]
        if not cols:
            continue
        size_info = dict(zip(headers, cols))
        sizes.append(size_info)

    return {"sizes": sizes}
