import requests
import sqlite3
from datetime import datetime

# =====================================================================
# 1. GLOBAL CONFIGURATION
# =====================================================================
# Centralized variables to easily change API settings or database names.
# Added ethereum, solana, and ripple (XRP) to the API request IDs
API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,ripple&vs_currencies=usd"
DB_NAME = "crypto_portfolio.db"
TABLE_NAME = "crypto_prices" # Changed from bitcoin to generic


# =====================================================================
# 2. DATABASE INITIALIZATION
# =====================================================================
def setup_database():
    """Initializes the database file and builds the structural table schema."""
    conn = None
    try:
        # Connect to SQLite. Creates the physical '.db' file if it doesn't exist.
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()  # The worker cursor used to execute SQL instructions

        # Create structural table inside the file if it isn't already there
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                asset_name TEXT NOT NULL,
                price_usd REAL NOT NULL
            )
        """)
        conn.commit()  # Permanently save changes to disk
        print(f"[*] Database and table '{TABLE_NAME}' verified successfully.")

    except sqlite3.Error as e:
        # Catches database-specific errors (e.g., locked files, syntax issues)
        print(f"[!] Database setup failed: {e}")

    finally:
        if conn:
            conn.close()  # Crucial: Always check out to unlock the database file


# =====================================================================
# 3. API DATA EXTRACTION (THE "E" IN ETL)
# =====================================================================
def fetch_crypto_prices():
    """Extracts live data from CoinGecko API. Returns a float or None."""
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()  # Safe-guard: Stops execution if the internet request failed (e.g., 404/500 errors)

        data = response.json()  # Converts the API's raw text response into a Python dictionary

        print("[*] Live prices extracted successfully from API.")
        return data

    except requests.exceptions.RequestException as e:
        # Catches network issues, timeouts, or API connection failures
        print(f"[!] Extraction phase failed: {e}")
        return None


# =====================================================================
# 4. DATA LOADING (THE "L" IN ETL)
# =====================================================================
def insert_price_data(crypto_data):
    """Loads the extracted data into the SQL database."""
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Method Chaining: Requests system time and immediately formats it to a readable string
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Mapping CoinGecko API IDs to clean names for your database
        coin_mapping = {
            'bitcoin': 'Bitcoin',
            'ethereum': 'Ethereum',
            'solana': 'Solana',
            'ripple': 'XRP'  # CoinGecko uses the ID 'ripple' for XRP
        }

        rows_appended = 0

        for api_id, clean_name in coin_mapping.items():
            if api_id in crypto_data:
                price = crypto_data[api_id]['usd']

                # Parameterized query (?, ?, ?) shields the database against malicious SQL Injection
                cursor.execute(f"""
                 INSERT INTO {TABLE_NAME} (timestamp, asset_name, price_usd)
                 VALUES (?, ?, ?)
                    """, (current_time, clean_name, price))
                
                rows_appended +=1
                print(f"[*] Prepared: {clean_name} -> ${price}")

        conn.commit()
        print(f"[*] Loading phase successful: {rows_appended} rows appended to '{TABLE_NAME}'.")

    except sqlite3.Error as e:
        print(f"[!] Loading phase failed: {e}")

    finally:
        if conn:
            conn.close()


# =====================================================================
# 5. MAIN SUPERVISOR
# =====================================================================
def main():
    """Controls the logical flow of the entire automated pipeline."""
    print("--- Starting Automated Crypto ETL Pipeline ---")
    
    setup_database()
    crypto_data = fetch_crypto_prices()

    if crypto_data is not None:
        insert_price_data(crypto_data)
    else:
        print("[!] Pipeline aborted: Missing target metrics.")

    print("--- Pipeline Execution Complete ---")


# Execution safeguard ensures script only fires when triggered directly, not when imported
if __name__ == "__main__":
    main()