import pandas as pd

url = "https://liquipedia.net/counterstrike/Majors"

tables = pd.read_html(url)

print(len(tables))
print(tables[2])  # main majors table