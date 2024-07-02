import requests
from bs4 import BeautifulSoup
import json

url = "https://www.cardekho.com/tata/punch-ev"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

vehicle_name = soup.find('h1', class_='displayInlineBlock').get_text(strip=True)

# Extract the price range and clean up the text
price_div = soup.find('div', class_='price')
price_range = price_div.get_text(strip=True).split('*')[0]

key_specs_section = soup.find('div', class_='qccontent')
key_specs = []
for row in key_specs_section.find_all('tr'):
    spec_name = row.find('td', class_='iconsHold').get_text(strip=True)
    spec_value = row.find('td', class_='iconsname').get_text(strip=True)
    key_specs.append(f"{spec_name}: {spec_value}")

top_features_section = key_specs_section.find_next('ul')
top_features = [feature.find('span', class_='iconsname').get_text(strip=True) for feature in top_features_section.find_all('li')]

data = {
    "Vehicle Name": vehicle_name,
    "Price Range": price_range,
    "Key Specifications": key_specs,
    "Top Features": top_features
}

with open('tata_punch_ev.json', 'w') as file:
    json.dump(data, file, indent=4)

print("Data scraped and saved successfully.")
