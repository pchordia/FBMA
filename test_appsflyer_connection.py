#!/usr/bin/env python3
"""
Test AppsFlyer API connection with different app ID formats
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('APPSFLYER_API_KEY')
app_id_from_env = os.getenv('APPSFLYER_APP_ID')

if not api_key:
    print("❌ APPSFLYER_API_KEY not found in .env")
    exit(1)

print("Testing AppsFlyer API connection...")
print("=" * 80)

# Try different app ID formats
app_id_variants = [
    app_id_from_env,  # As entered: id6752788715
    '6752788715',     # Without 'id' prefix
    'id6752788715',   # With 'id' prefix (explicit)
]

for app_id in app_id_variants:
    print(f"\nTrying App ID format: {app_id}")
    
    url = f"https://hq1.appsflyer.com/api/aggregate-data/app/{app_id}/partners-by-date-report/v5"
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'text/csv'
    }
    
    params = {
        'from': '2025-11-27',
        'to': '2025-11-27',
        'media_source': 'facebook',
        'timezone': 'America/Los_Angeles',
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        print(f"  Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"  ✅ SUCCESS! This format works: {app_id}")
            print(f"  Data preview: {response.text[:200]}...")
            print(f"\n✅ Use this App ID: {app_id}")
            break
        elif response.status_code == 404:
            print(f"  ❌ 404 Not Found - wrong app ID format")
        elif response.status_code == 401:
            print(f"  ❌ 401 Unauthorized - check API key")
        elif response.status_code == 403:
            print(f"  ❌ 403 Forbidden - API key lacks permissions")
        else:
            print(f"  ❌ Error: {response.text[:200]}")
            
    except Exception as e:
        print(f"  ❌ Exception: {str(e)}")

print("\n" + "=" * 80)
print("\nIf none worked, check:")
print("1. App ID in AppsFlyer dashboard (Settings → My Apps)")
print("2. API token has 'Reports' or 'Aggregate Pull' permissions")
print("3. Token is a V2 token (Bearer format)")



