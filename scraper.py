import pandas as pd

url = "https://liquipedia.net/counterstrike/Majors"

# Read all tables
tables = pd.read_html(url)

# Select the correct table (your majors table)
majors_df = tables[2]

# Save to CSV
majors_df.to_csv("gpt_majors.csv", index=False)

# Optional: print to confirm
print(majors_df)
print("CSV file saved as gpt_majors.csv")