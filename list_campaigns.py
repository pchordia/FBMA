#!/usr/bin/env python3
"""
Script to list all active campaigns from Facebook Ad Account
"""

import os
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

print(f"Fetching campaigns from ad account: {ad_account_id}")
print("=" * 80)

try:
    # Get ad account
    account = AdAccount(ad_account_id)
    
    # Fetch campaigns with relevant fields
    campaigns = account.get_campaigns(fields=[
        'id',
        'name',
        'status',
        'objective',
        'daily_budget',
        'lifetime_budget',
        'budget_remaining',
        'spend_cap',
        'created_time',
        'start_time',
        'stop_time',
        'updated_time',
    ])
    
    active_campaigns = []
    paused_campaigns = []
    other_campaigns = []
    
    for campaign in campaigns:
        status = campaign.get('status', 'UNKNOWN')
        if status == 'ACTIVE':
            active_campaigns.append(campaign)
        elif status == 'PAUSED':
            paused_campaigns.append(campaign)
        else:
            other_campaigns.append(campaign)
    
    # Display Active Campaigns
    if active_campaigns:
        print(f"\n🟢 ACTIVE CAMPAIGNS ({len(active_campaigns)}):")
        print("-" * 80)
        for campaign in active_campaigns:
            print(f"\nName: {campaign.get('name', 'N/A')}")
            print(f"  ID: {campaign.get('id', 'N/A')}")
            print(f"  Status: {campaign.get('status', 'N/A')}")
            print(f"  Objective: {campaign.get('objective', 'N/A')}")
            
            daily_budget = campaign.get('daily_budget')
            lifetime_budget = campaign.get('lifetime_budget')
            
            if daily_budget:
                print(f"  Daily Budget: ${int(daily_budget) / 100:.2f}")
            if lifetime_budget:
                print(f"  Lifetime Budget: ${int(lifetime_budget) / 100:.2f}")
            
            budget_remaining = campaign.get('budget_remaining')
            if budget_remaining:
                print(f"  Budget Remaining: ${int(budget_remaining) / 100:.2f}")
            
            print(f"  Created: {campaign.get('created_time', 'N/A')}")
            if campaign.get('start_time'):
                print(f"  Start Time: {campaign.get('start_time')}")
            if campaign.get('stop_time'):
                print(f"  Stop Time: {campaign.get('stop_time')}")
    else:
        print("\n🟢 ACTIVE CAMPAIGNS: None")
    
    # Display Paused Campaigns
    if paused_campaigns:
        print(f"\n\n⏸️  PAUSED CAMPAIGNS ({len(paused_campaigns)}):")
        print("-" * 80)
        for campaign in paused_campaigns:
            print(f"\nName: {campaign.get('name', 'N/A')}")
            print(f"  ID: {campaign.get('id', 'N/A')}")
            print(f"  Status: {campaign.get('status', 'N/A')}")
            print(f"  Objective: {campaign.get('objective', 'N/A')}")
    
    # Display Other Campaigns
    if other_campaigns:
        print(f"\n\n⚪ OTHER CAMPAIGNS ({len(other_campaigns)}):")
        print("-" * 80)
        for campaign in other_campaigns:
            print(f"\nName: {campaign.get('name', 'N/A')}")
            print(f"  ID: {campaign.get('id', 'N/A')}")
            print(f"  Status: {campaign.get('status', 'N/A')}")
            print(f"  Objective: {campaign.get('objective', 'N/A')}")
    
    # Summary
    print("\n" + "=" * 80)
    total = len(active_campaigns) + len(paused_campaigns) + len(other_campaigns)
    print(f"Total Campaigns: {total}")
    print(f"  Active: {len(active_campaigns)}")
    print(f"  Paused: {len(paused_campaigns)}")
    print(f"  Other: {len(other_campaigns)}")
    print("=" * 80)
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)

