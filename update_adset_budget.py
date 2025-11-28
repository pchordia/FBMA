#!/usr/bin/env python3
"""
Script to update ad set budget
"""

import os
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adset import AdSet

# Load environment variables
load_dotenv()

# Get credentials from .env
access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')

if not access_token:
    print("❌ Error: FACEBOOK_ACCESS_TOKEN not found in .env file")
    exit(1)

# Initialize the API
FacebookAdsApi.init(access_token=access_token)

# Ad Set ID and new budget
ADSET_ID = '6913347655784'
NEW_DAILY_BUDGET = 5500  # $55.00 in cents

print(f"Updating ad set budget...")
print("=" * 80)

try:
    # Get the ad set
    adset = AdSet(ADSET_ID)
    
    # Get current info
    current_info = adset.api_get(fields=[
        'id',
        'name',
        'status',
        'daily_budget',
        'lifetime_budget',
        'campaign',
    ])
    
    print(f"\n📋 Current Ad Set Information:")
    print(f"  Name: {current_info.get('name', 'N/A')}")
    print(f"  ID: {current_info.get('id', 'N/A')}")
    print(f"  Campaign: {current_info.get('campaign', {}).get('name', 'N/A')}")
    print(f"  Status: {current_info.get('status', 'N/A')}")
    
    current_daily = current_info.get('daily_budget')
    if current_daily:
        print(f"  Current Daily Budget: ${int(current_daily) / 100:.2f}")
    
    print(f"\n🔄 Updating daily budget to: ${NEW_DAILY_BUDGET / 100:.2f}")
    print("-" * 80)
    
    # Update the budget
    adset.api_update(params={
        'daily_budget': NEW_DAILY_BUDGET,
    })
    
    print("✅ Budget update request sent!")
    
    # Verify the update
    updated_info = adset.api_get(fields=[
        'id',
        'name',
        'daily_budget',
        'budget_remaining',
    ])
    
    print(f"\n✅ Updated Ad Set Information:")
    print(f"  Name: {updated_info.get('name', 'N/A')}")
    print(f"  New Daily Budget: ${int(updated_info.get('daily_budget', 0)) / 100:.2f}")
    
    budget_remaining = updated_info.get('budget_remaining')
    if budget_remaining:
        print(f"  Budget Remaining: ${int(budget_remaining) / 100:.2f}")
    
    print("=" * 80)
    print("✅ Budget successfully updated!")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)

