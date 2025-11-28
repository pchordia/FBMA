#!/usr/bin/env python3
"""
Script to find ad sets with specific budget amount (efficient version - only active campaigns)
"""

import os
import time
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign

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
print("(Checking only ACTIVE campaigns to reduce API calls)")
print("=" * 80)

try:
    # Get ad account
    account = AdAccount(ad_account_id)
    
    # First, get only ACTIVE campaigns
    campaigns = account.get_campaigns(
        fields=['id', 'name', 'status'],
        params={'effective_status': ['ACTIVE']}
    )
    
    active_campaigns = list(campaigns)
    print(f"\nFound {len(active_campaigns)} active campaign(s)")
    
    if not active_campaigns:
        print("No active campaigns found. Checking all campaigns...")
        campaigns = account.get_campaigns(fields=['id', 'name'])
        active_campaigns = list(campaigns)[:5]  # Check first 5 campaigns
    
    matching_adsets = []
    all_adsets_checked = []
    
    for campaign in active_campaigns:
        print(f"\nChecking campaign: {campaign.get('name')}...")
        
        # Get ad sets for this campaign
        campaign_obj = Campaign(campaign.get('id'))
        adsets = campaign_obj.get_ad_sets(fields=[
            'id',
            'name',
            'status',
            'daily_budget',
            'lifetime_budget',
            'budget_remaining',
            'optimization_goal',
            'billing_event',
            'start_time',
            'end_time',
        ])
        
        for adset in adsets:
            daily_budget = adset.get('daily_budget')
            lifetime_budget = adset.get('lifetime_budget')
            
            # Store all ad sets for summary
            budget_info = {
                'adset': adset,
                'campaign': campaign.get('name'),
                'daily': int(daily_budget)/100 if daily_budget else 0,
                'lifetime': int(lifetime_budget)/100 if lifetime_budget else 0,
            }
            all_adsets_checked.append(budget_info)
            
            # Check if either daily or lifetime budget matches
            if (daily_budget and int(daily_budget) == TARGET_BUDGET) or \
               (lifetime_budget and int(lifetime_budget) == TARGET_BUDGET):
                matching_adsets.append({
                    'adset': adset,
                    'campaign': campaign.get('name')
                })
        
        time.sleep(0.5)  # Small delay to avoid rate limits
    
    print("\n" + "=" * 80)
    
    if matching_adsets:
        print(f"\n✅ Found {len(matching_adsets)} ad set(s) with ${TARGET_BUDGET/100:.2f} budget:\n")
        
        for item in matching_adsets:
            adset = item['adset']
            print(f"\nAd Set Name: {adset.get('name', 'N/A')}")
            print(f"  Ad Set ID: {adset.get('id', 'N/A')}")
            print(f"  Campaign: {item['campaign']}")
            print(f"  Status: {adset.get('status', 'N/A')}")
            
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
            print(f"  Start Time: {adset.get('start_time', 'N/A')}")
            if adset.get('end_time'):
                print(f"  End Time: {adset.get('end_time')}")
            
            print("-" * 80)
    else:
        print(f"\n❌ No ad sets found with exactly ${TARGET_BUDGET/100:.2f} budget")
        
        # Show all budgets found
        if all_adsets_checked:
            print(f"\n📊 Summary of ad sets checked ({len(all_adsets_checked)} total):\n")
            for info in all_adsets_checked:
                adset = info['adset']
                if info['daily'] > 0 or info['lifetime'] > 0:
                    budget_str = f"Daily: ${info['daily']:.2f}" if info['daily'] > 0 else f"Lifetime: ${info['lifetime']:.2f}"
                    print(f"  {adset.get('name')} - {budget_str} - Status: {adset.get('status')}")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    
    if "rate limit" in str(e).lower() or "too many" in str(e).lower():
        print("\n⏰ You've hit the Facebook API rate limit.")
        print("Please wait 10-15 minutes and try again.")
    
    exit(1)

