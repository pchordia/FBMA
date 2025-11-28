#!/usr/bin/env python3
"""
Test script to verify Facebook access token and fetch ad account info
"""

import os
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

# Load environment variables
load_dotenv()

# Get credentials from .env
access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')

if not access_token:
    print("❌ Error: FACEBOOK_ACCESS_TOKEN not found in .env file")
    exit(1)

# Initialize the API
FacebookAdsApi.init(access_token=access_token)

# Ad Account ID (prepend 'act_' if not already present)
ad_account_id = '24590952'
if not ad_account_id.startswith('act_'):
    ad_account_id = f'act_{ad_account_id}'

print(f"Testing connection to ad account: {ad_account_id}")
print("-" * 50)

try:
    # Get ad account info
    account = AdAccount(ad_account_id)
    
    # Fetch basic account details
    account_info = account.api_get(fields=[
        'name',
        'account_id',
        'account_status',
        'currency',
        'timezone_name',
        'business_name',
        'amount_spent',
        'balance',
    ])
    
    print("✅ Token is valid! Ad Account Information:")
    print("-" * 50)
    print(f"Account Name: {account_info.get('name', 'N/A')}")
    print(f"Account ID: {account_info.get('account_id', 'N/A')}")
    print(f"Account Status: {account_info.get('account_status', 'N/A')}")
    print(f"Currency: {account_info.get('currency', 'N/A')}")
    print(f"Timezone: {account_info.get('timezone_name', 'N/A')}")
    print(f"Business Name: {account_info.get('business_name', 'N/A')}")
    print(f"Amount Spent: {account_info.get('amount_spent', 'N/A')}")
    print(f"Balance: {account_info.get('balance', 'N/A')}")
    print("-" * 50)
    print("✅ Connection successful!")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    print("\nPossible issues:")
    print("1. Invalid access token")
    print("2. Token doesn't have permission to access this ad account")
    print("3. Ad account ID is incorrect")
    print("4. Token has expired")
    exit(1)

