import requests
import pandas as pd

url = "https://liquipedia.net/counterstrike/Majors"

headers = {
    "User-Agent": "Mozilla/5.0"
}

session = requests.Session()
response = session.get(url, headers=headers)

if response.status_code != 200:
    print("Failed to fetch page")
    exit()

tables = pd.read_html(response.text, flavor="lxml")

# Find correct table dynamically
df = None
for table in tables:
    if "Tournament" in table.columns:
        df = table
        break

if df is None:
    print("Target table not found")
    exit()

# Clean columns
df.columns = [' '.join(col).strip() if isinstance(col, tuple) else col for col in df.columns]

# Clean data
df = df.dropna(how="all")
df = df.replace(r'\[.*?\]', '', regex=True)

# Save
df.to_csv("majors_full.csv", index=False, encoding="utf-8-sig")

print("✅ Saved to majors_full.csv")
print(df.head())