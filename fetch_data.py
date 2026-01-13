from curl_cffi import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

all_laptops=[]
processor, ram, os, ssd, display = "N/A", "N/A", "N/A", "N/A", "N/A"

for i in range(1,26):
    flipkart_url=f"https://www.flipkart.com/search?q=gaming+laptop&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_5_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_5_na_na_na&as-pos=1&as-type=RECENT&suggestionId=gaming+laptop%7CLaptops&requestId=e627cfb6-0eb4-4205-86a8-cc0f81d32495&as-searchtext=gamin&page={i}"


    print("Fetching data...")
    print(f"Page:{i}")

    try:
        # 1. Fetch with Browser Fingerprint
        response = requests.get(flipkart_url, impersonate="chrome110", timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")

        cards = soup.find_all("div", attrs={"data-id": True})
        
        print(f"Found {len(cards)} product cards.")

        valid_items = 0

        for card in cards:
            title_tag = card.select_one("div.RG5Slk") or card.select_one("div._4rR01T")
            
            price_tag = card.select_one("div.hZ3P6w.DeU9vF") or card.select_one("div._30jeq3")

            specs=card.select_one(selector="ul.HwRTzP")
            
            if specs:
                spec=specs.find_all("li")
                processor=spec[0].getText().strip()
                ram=spec[1].getText().strip()
                os=spec[2].getText().strip()
                ssd=spec[3].getText().strip()
                display=spec[4].getText().strip()

            if title_tag and price_tag:
                title = title_tag.get_text().strip()
                price = price_tag.get_text().strip().replace("₹", "").replace(",", "")
                
                all_laptops.append(
                    {
                        "title": title,
                        "price": float(price),
                        "processor":processor,
                        "ram":ram,
                        "ssd":ssd,
                        "display":display,
                        "os":os,
                    }
                )
        time.sleep(10)
    except Exception as e:
        print(f"Error: {e}")

filename="C:/Users/ranab/OneDrive/Desktop/Arbitrage Hunter/laptop_data.csv"

df=pd.DataFrame(all_laptops)

df.drop_duplicates(inplace=True)
df.to_csv(filename,index=False)

print(f"Success! Saved {len(df)} rows to '{filename}'")
print(df.head()) # Show first 5 rows