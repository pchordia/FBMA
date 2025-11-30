#!/usr/bin/env python3
"""
Test basic AppsFlyer API connectivity
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('APPSFLYER_API_KEY')
app_id = os.getenv('APPSFLYER_APP_ID')

print("Testing AppsFlyer API...")
print("=" * 80)
print(f"App ID: {app_id}")
print(f"API Key: {api_key[:20]}..." if api_key else "No API key")
print("=" * 80)

# Try getting app info first
print("\n1. Testing basic app endpoint...")
url = f"https://hq1.appsflyer.com/api/agg/v2/app/{app_id}"

headers = {
    'Authorization': f'Bearer {api_key}',
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ App endpoint works!")
        print(response.text[:500])
    else:
        print(f"Response: {response.text[:500]}")
except Exception as e:
    print(f"Error: {e}")

# Try partners endpoint with different versions
print("\n2. Testing partners endpoint (v5)...")
url = f"https://hq1.appsflyer.com/api/agg/v2/data/app/{app_id}"

params = {
    'from': '2025-11-27',
    'to': '2025-11-27',
}

headers = {
    'Authorization': f'Bearer {api_key}',
    'Accept': 'application/json'
}

try:
    response = requests.get(url, headers=headers, params=params, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:500]}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 80)
print("\nPlease share the AppsFlyer API documentation link or:")
print("1. The exact endpoint URL from AppsFlyer docs")
print("2. Any example API calls from AppsFlyer dashboard")



