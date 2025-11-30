#!/usr/bin/env python3
"""
Download AppsFlyer data using Aggregate Pull API V2 (Partners by date)
"""

import os
import json
import csv
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv

load_dotenv()

class AppsFlyerDataDownloader:
    def __init__(self, app_id=None):
        self.api_key = os.getenv('APPSFLYER_API_KEY')
        if not self.api_key:
            raise Exception("APPSFLYER_API_KEY not found in .env file")
        
        # App ID - will need to be configured
        self.app_id = app_id or os.getenv('APPSFLYER_APP_ID')
        if not self.app_id:
            raise Exception("APPSFLYER_APP_ID not found. Pass as parameter or set in .env")
        
        self.base_url = "https://hq1.appsflyer.com/api/aggregate-data/app"
    
    def get_partners_by_date(self, from_date, to_date, media_source='facebook'):
        """
        Pull AppsFlyer Partners by Date report
        
        Args:
            from_date: 'YYYY-MM-DD'
            to_date: 'YYYY-MM-DD'
            media_source: 'facebook' or specific partner
        """
        endpoint = f"{self.base_url}/{self.app_id}/partners-by-date-report/v5"
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'text/csv'  # Request CSV format
        }
        
        params = {
            'from': from_date,
            'to': to_date,
            'media_source': media_source,
            'timezone': 'America/Los_Angeles',
            'maximum_rows': 100000,
            # Request campaign/adset/ad level breakdown
            'groupings': 'pid,c,af_c_id,af_adset_id,af_ad_id'
        }
        
        print(f"Fetching AppsFlyer data: {from_date} to {to_date}")
        print(f"  Media Source: {media_source}")
        print(f"  Groupings: campaign, adset, ad level")
        
        try:
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            
            # Parse CSV response
            lines = response.text.strip().split('\n')
            if len(lines) <= 1:
                print(f"  ⚠️  No data returned")
                return []
            
            # Parse CSV
            reader = csv.DictReader(lines)
            data = list(reader)
            
            print(f"  ✅ Downloaded {len(data)} rows")
            return data
            
        except requests.exceptions.HTTPError as e:
            print(f"  ❌ HTTP Error: {e}")
            print(f"  Response: {e.response.text if e.response else 'N/A'}")
            return []
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            return []
    
    def save_to_csv(self, data, filename):
        """Save AppsFlyer data to CSV"""
        if not data:
            print(f"⚠️  No data to save for {filename}")
            return None
        
        filepath = f"data/{filename}"
        os.makedirs('data', exist_ok=True)
        
        # Check if file already exists
        if os.path.exists(filepath):
            print(f"⏭️  File already exists: {filepath} - skipping")
            return filepath
        
        fieldnames = data[0].keys()
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"✅ Saved to {filepath} ({len(data)} rows)")
        return filepath
    
    def download_daily_report(self, days_ago=1):
        """Download AppsFlyer data for a specific day"""
        target_date = datetime.now().date() - timedelta(days=days_ago)
        date_str = target_date.strftime('%Y-%m-%d')
        date_file_str = target_date.strftime('%Y%m%d')
        
        print("=" * 80)
        print(f"📊 Downloading AppsFlyer Data for {date_str}")
        print("=" * 80)
        
        # Download data
        data = self.get_partners_by_date(
            from_date=date_str,
            to_date=date_str,
            media_source='facebook'
        )
        
        if not data:
            print("❌ No data downloaded")
            return None
        
        # Save to CSV
        filepath = self.save_to_csv(data, f'appsflyer_fb_{date_file_str}.csv')
        
        print("=" * 80)
        print(f"✅ AppsFlyer download complete!")
        print("=" * 80)
        
        return filepath
    
    def download_weekly_report(self):
        """Download AppsFlyer data for last 7 days"""
        print("=" * 80)
        print("📊 DOWNLOADING LAST 7 DAYS OF APPSFLYER DATA")
        print("=" * 80)
        
        files_created = []
        
        for days_ago in range(1, 8):
            filepath = self.download_daily_report(days_ago)
            if filepath:
                files_created.append(filepath)
        
        print("\n" + "=" * 80)
        print(f"✅ 7-DAY APPSFLYER DOWNLOAD COMPLETE")
        print(f"Files created: {len(files_created)}")
        print("=" * 80)
        
        return files_created

def main():
    """
    Usage:
    1. Set APPSFLYER_API_KEY in .env
    2. Set APPSFLYER_APP_ID in .env (your app's AppsFlyer ID)
    3. Run this script
    """
    try:
        # You'll need to set your app ID - get it from AppsFlyer dashboard
        downloader = AppsFlyerDataDownloader()
        
        # Download yesterday's data
        downloader.download_daily_report(days_ago=1)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nMake sure you have set:")
        print("  - APPSFLYER_API_KEY in .env")
        print("  - APPSFLYER_APP_ID in .env")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main()

