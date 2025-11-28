#!/usr/bin/env python3
"""
Script to find ad sets with specific budget amount
"""

import os
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
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

# Ad Account ID
ad_account_id = 'act_24590952'

# Budget to search for (in cents)
TARGET_BUDGET = 5000  # $50.00 = 5000 cents

print(f"Searching for ad sets with ${TARGET_BUDGET/100:.2f} budget...")
print("=" * 80)

try:
    # Get ad account
    account = AdAccount(ad_account_id)
    
    # Fetch all ad sets with budget fields
    adsets = account.get_ad_sets(fields=[
        'id',
        'name',
        'status',
        'daily_budget',
        'lifetime_budget',
        'budget_remaining',
        'campaign_id',
        'campaign',
        'start_time',
        'end_time',
        'optimization_goal',
        'billing_event',
        'bid_amount',
    ])
    
    matching_adsets = []
    
    for adset in adsets:
        daily_budget = adset.get('daily_budget')
        lifetime_budget = adset.get('lifetime_budget')
        
        # Check if either daily or lifetime budget matches
        if (daily_budget and int(daily_budget) == TARGET_BUDGET) or \
           (lifetime_budget and int(lifetime_budget) == TARGET_BUDGET):
            matching_adsets.append(adset)
    
    if matching_adsets:
        print(f"\n✅ Found {len(matching_adsets)} ad set(s) with ${TARGET_BUDGET/100:.2f} budget:\n")
        print("-" * 80)
        
        for adset in matching_adsets:
            print(f"\nAd Set Name: {adset.get('name', 'N/A')}")
            print(f"  Ad Set ID: {adset.get('id', 'N/A')}")
            print(f"  Status: {adset.get('status', 'N/A')}")
            print(f"  Campaign: {adset.get('campaign', {}).get('name', 'N/A')}")
            print(f"  Campaign ID: {adset.get('campaign_id', 'N/A')}")
            
            daily_budget = adset.get('daily_budget')
            lifetime_budget = adset.get('lifetime_budget')
            
            if daily_budget:
                print(f"  Daily Budget: ${int(daily_budget) / 100:.2f}")
            if lifetime_budget:
                print(f"  Lifetime Budget: ${int(lifetime_budget) / 100:.2f}")
            
            budget_remaining = adset.get('budget_remaining')
            if budget_remaining:
                print(f"  Budget Remaining: ${int(budget_remaining) / 100:.2f}")
            
            print(f"  Optimization Goal: {adset.get('optimization_goal', 'N/A')}")
            print(f"  Billing Event: {adset.get('billing_event', 'N/A')}")
            
            bid_amount = adset.get('bid_amount')
            if bid_amount:
                print(f"  Bid Amount: ${int(bid_amount) / 100:.2f}")
            
            print(f"  Start Time: {adset.get('start_time', 'N/A')}")
            if adset.get('end_time'):
                print(f"  End Time: {adset.get('end_time')}")
            
            print("-" * 80)
    else:
        print(f"\n❌ No ad sets found with ${TARGET_BUDGET/100:.2f} budget")
        print("\nSearching for ad sets with budgets close to $50...")
        
        # Show ad sets with budgets between $40-$60
        close_adsets = []
        adsets = account.get_ad_sets(fields=[
            'id',
            'name',
            'status',
            'daily_budget',
            'lifetime_budget',
        ])
        
        for adset in adsets:
            daily_budget = adset.get('daily_budget')
            lifetime_budget = adset.get('lifetime_budget')
            
            if daily_budget:
                daily_amount = int(daily_budget) / 100
                if 40 <= daily_amount <= 60:
                    close_adsets.append({
                        'adset': adset,
                        'budget_type': 'Daily',
                        'amount': daily_amount
                    })
            
            if lifetime_budget:
                lifetime_amount = int(lifetime_budget) / 100
                if 40 <= lifetime_amount <= 60:
                    close_adsets.append({
                        'adset': adset,
                        'budget_type': 'Lifetime',
                        'amount': lifetime_amount
                    })
        
        if close_adsets:
            print(f"\nFound {len(close_adsets)} ad set(s) with budget between $40-$60:\n")
            for item in close_adsets[:10]:  # Show first 10
                adset = item['adset']
                print(f"  {adset.get('name')} - {item['budget_type']}: ${item['amount']:.2f} - Status: {adset.get('status')}")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)

