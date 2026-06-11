import sqlite3
import csv

print("--- Opening the Safe ---")
# 1. Connect to the database
conn = sqlite3.connect("crypto_portfolio.db")
cursor = conn.cursor()

# 2. Grab all the data and the column names
cursor.execute("SELECT * FROM crypto_prices")
rows = cursor.fetchall()
headers = [description[0] for description in cursor.description]

# 3. Write it to a brand new CSV file
print("--- Exporting to CSV ---")
with open("crypto_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(headers)  # Write the column names at the top
    writer.writerows(rows)    # Write the actual data

print("--- Success! crypto_data.csv created ---")