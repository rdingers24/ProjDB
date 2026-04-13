import sqlite3
import pandas as pd 

conn = sqlite3.connect('majors.db')
cursor = conn.cursor()
df = pd.read_csv('majors.csv')
df.to_sql('majors',conn, if_exists= 'replace', index = False)
conn.commit()
conn.close()