#!/usr/bin/env python3
"""
Cache Manager for Weather App
This script provides utilities for managing the SQLite cache database.
"""

import sqlite3
import argparse
from datetime import datetime
import os
from pathlib import Path

# Database path
DB_PATH = "app/data/weather_cache.db"

def ensure_db_exists():
    """Check if the database exists, create directory if needed"""
    if not os.path.exists(DB_PATH):
        db_dir = os.path.dirname(DB_PATH)
        Path(db_dir).mkdir(exist_ok=True, parents=True)
        print(f"Database not found at {DB_PATH}. It will be created when the app is first run.")
        return False
    return True

def view_cache():
    """Display information about the cache"""
    if not ensure_db_exists():
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("\n=== Weather Cache Status ===\n")
    
    # Check weather cache
    cursor.execute("SELECT COUNT(*) FROM weather_cache")
    count = cursor.fetchone()[0]
    print(f"Current weather entries: {count}")
    
    # Check forecast cache
    cursor.execute("SELECT COUNT(*) FROM forecast_cache")
    count = cursor.fetchone()[0]
    print(f"Forecast entries: {count}")
    
    # Get total size
    cursor.execute("SELECT page_count * page_size FROM pragma_page_count(), pragma_page_size()")
    db_size = cursor.fetchone()[0]
    print(f"Database size: {db_size/1024:.2f} KB")
    
    print("\n=== Recent Weather Cache Entries ===\n")
    cursor.execute(
        "SELECT city, timestamp FROM weather_cache ORDER BY timestamp DESC LIMIT 10"
    )
    entries = cursor.fetchall()
    
    if entries:
        for city, timestamp in entries:
            time_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
            expiry = timestamp + 3600  # 1 hour cache
            expiry_str = datetime.fromtimestamp(expiry).strftime("%Y-%m-%d %H:%M:%S")
            now = datetime.now().timestamp()
            status = "Valid" if now < expiry else "Expired"
            
            print(f"City: {city}")
            print(f"  Cached at: {time_str}")
            print(f"  Expires at: {expiry_str}")
            print(f"  Status: {status}")
            print()
    else:
        print("No entries found in the cache.")
    
    conn.close()

def clear_cache():
    """Clear all entries from the cache"""
    if not ensure_db_exists():
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM weather_cache")
    weather_count = cursor.rowcount
    
    cursor.execute("DELETE FROM forecast_cache")
    forecast_count = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    print(f"Cache cleared: {weather_count} weather entries and {forecast_count} forecast entries deleted.")

def main():
    parser = argparse.ArgumentParser(description="Weather App Cache Manager")
    parser.add_argument("action", choices=["view", "clear"], help="Action to perform on the cache")
    
    args = parser.parse_args()
    
    if args.action == "view":
        view_cache()
    elif args.action == "clear":
        clear_cache()

if __name__ == "__main__":
    main()
