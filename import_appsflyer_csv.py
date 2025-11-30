#!/usr/bin/env python3
"""
Import manually exported AppsFlyer CSV files
Use this until API access is working
"""

import os
import sys
import shutil
from datetime import datetime, timedelta

def import_appsflyer_csv(source_file, date_str=None):
    """
    Import an AppsFlyer CSV export
    
    Args:
        source_file: Path to the CSV file you downloaded from AppsFlyer
        date_str: Optional date string (YYYYMMDD). If not provided, will prompt.
    """
    
    if not os.path.exists(source_file):
        print(f"❌ File not found: {source_file}")
        return False
    
    # Get date
    if not date_str:
        print(f"\nImporting: {source_file}")
        date_input = input("Enter date for this data (YYYYMMDD), or press Enter for yesterday: ").strip()
        
        if date_input:
            date_str = date_input
        else:
            yesterday = datetime.now().date() - timedelta(days=1)
            date_str = yesterday.strftime('%Y%m%d')
    
    # Validate date format
    try:
        datetime.strptime(date_str, '%Y%m%d')
    except ValueError:
        print(f"❌ Invalid date format: {date_str}. Use YYYYMMDD (e.g., 20251127)")
        return False
    
    # Copy to data folder
    os.makedirs('data', exist_ok=True)
    target_file = f'data/appsflyer_fb_{date_str}.csv'
    
    shutil.copy2(source_file, target_file)
    print(f"✅ Imported: {target_file}")
    
    return True

def print_usage():
    print("""
📥 AppsFlyer CSV Import Tool

Usage:
    python import_appsflyer_csv.py <path_to_csv> [date]

Examples:
    python import_appsflyer_csv.py ~/Downloads/appsflyer_export.csv 20251127
    python import_appsflyer_csv.py ~/Downloads/partners_report.csv

Steps to export from AppsFlyer:
    1. Go to Reports → Partners (or Overview → Partners)
    2. Set date range (single day recommended)
    3. Filter to: Media Source = Facebook
    4. Export as CSV
    5. Run this script with the downloaded file
    """)

def main():
    if len(sys.argv) < 2:
        print_usage()
        return
    
    source_file = sys.argv[1]
    date_str = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = import_appsflyer_csv(source_file, date_str)
    
    if success:
        print("\n✅ Import complete!")
        print("\nNext steps:")
        print("  1. Import data for other dates (if needed)")
        print("  2. Run comparison: python compare_fb_af.py")

if __name__ == "__main__":
    main()

