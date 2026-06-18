import time
import random
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

BASE_URL = "https://riyasewana.com/search/cars"
MAX_PAGES = 396

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

all_listings = []

for page in range(1, MAX_PAGES + 1):
    url = f"{BASE_URL}?page={page}"
    print(f"Scraping page {page}: {url}")

    try:
        response = requests.get(url, headers=headers, timeout=20)
        print("Status:", response.status_code)

        if response.status_code != 200:
            print("Stopped because status was not 200")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.select("li.v-card")

        if not cards:
            print("No cards found. Stopping.")
            break

        for card in cards:
            title_tag = card.select_one(".v-card-title a")
            price_tag = card.select_one(".v-card-price")
            year_tag = card.select_one(".v-card-year")
            meta_tag = card.select_one(".v-card-meta")
            date_tag = card.select_one(".v-card-date")

            title = title_tag.get_text(strip=True) if title_tag else None
            listing_url = title_tag["href"] if title_tag and title_tag.has_attr("href") else None
            price = price_tag.get_text(strip=True) if price_tag else None
            year = year_tag.get_text(strip=True) if year_tag else None
            meta = meta_tag.get_text(" ", strip=True) if meta_tag else ""
            posted_time = date_tag.get_text(strip=True) if date_tag else None

            city = None
            mileage = None

            if "·" in meta:
                parts = [part.strip() for part in meta.split("·")]
                city = parts[0]
                mileage = parts[1] if len(parts) > 1 else None
            else:
                city = meta.strip() if meta else None

            all_listings.append({
                "title": title,
                "price": price,
                "year": year,
                "city": city,
                "mileage": mileage,
                "posted_time": posted_time,
                "listing_url": listing_url,
                "scraped_at": datetime.now()
            })

        delay = random.uniform(3, 6)
        print(f"Waiting {delay:.2f} seconds...\n")
        time.sleep(delay)

    except Exception as e:
        print("Error:", e)
        break

df = pd.DataFrame(all_listings)
df = df.drop_duplicates(subset=["listing_url"])

print(df.head())
print("Total listings:", len(df))

df.to_csv("riyasewana_all_listings.csv", index=False)