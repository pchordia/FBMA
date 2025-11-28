#!/usr/bin/env python3
"""
Budget Scheduler V2 - Automatically adjusts campaign/ad set budgets based on time of day
Now with smart budget restoration - remembers original budgets and restores them
"""

import os
import json
from datetime import datetime
import pytz
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet

# Load environment variables
load_dotenv()

class BudgetScheduler:
    def __init__(self, config_path='config.json', state_path='budget_state.json'):
        self.config = self.load_config(config_path)
        self.state_path = state_path
        self.state = self.load_state()
        
        self.access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        
        if not self.access_token:
            raise Exception("FACEBOOK_ACCESS_TOKEN not found in .env file")
        
        FacebookAdsApi.init(access_token=self.access_token)
        self.ad_account_id = 'act_24590952'
        self.account = AdAccount(self.ad_account_id)
        
        # Set timezone
        self.timezone = pytz.timezone(self.config['timezone'])
    
    def load_config(self, config_path):
        """Load configuration from JSON file"""
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def load_state(self):
        """Load state file (stored budgets)"""
        try:
            with open(self.state_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'original_budgets': {},
                'last_run': None,
                'last_mode': None
            }
    
    def save_state(self):
        """Save state file"""
        with open(self.state_path, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def get_current_budget_mode(self):
        """Determine which mode we should be in based on current time"""
        now = datetime.now(self.timezone)
        current_time = now.strftime("%H:%M")
        
        nightly_time = self.config['schedule']['nightly_time']
        daytime_time = self.config['schedule']['daytime_time']
        
        # Convert times to comparable format
        current_hour = now.hour
        nightly_hour = int(nightly_time.split(':')[0])
        daytime_hour = int(daytime_time.split(':')[0])
        
        # Nightly period is from nightly_time to daytime_time
        if nightly_hour <= current_hour < daytime_hour:
            return 'nightly', current_time
        else:
            return 'daytime', current_time
    
    def get_active_campaigns_and_adsets(self):
        """Fetch all active campaigns and their ad sets"""
        print("📊 Fetching active campaigns and ad sets...")
        
        campaigns = self.account.get_campaigns(
            fields=['id', 'name', 'status', 'daily_budget', 'lifetime_budget'],
            params={'effective_status': ['ACTIVE']}
        )
        
        results = {
            'campaign_budgets': [],  # Campaigns with budget at campaign level
            'adset_budgets': []      # Ad sets with budget at ad set level
        }
        
        for campaign in campaigns:
            campaign_id = campaign.get('id')
            campaign_name = campaign.get('name')
            campaign_daily_budget = campaign.get('daily_budget')
            
            # Check if excluded
            if campaign_id in self.config['excluded_campaigns']:
                print(f"  ⏭️  Skipping excluded campaign: {campaign_name}")
                continue
            
            # If campaign has budget set at campaign level
            if campaign_daily_budget:
                results['campaign_budgets'].append({
                    'id': campaign_id,
                    'name': campaign_name,
                    'current_budget': int(campaign_daily_budget),
                    'type': 'campaign'
                })
            else:
                # Check ad sets within this campaign
                campaign_obj = Campaign(campaign_id)
                adsets = campaign_obj.get_ad_sets(
                    fields=['id', 'name', 'status', 'daily_budget', 'lifetime_budget'],
                    params={'effective_status': ['ACTIVE']}
                )
                
                for adset in adsets:
                    adset_id = adset.get('id')
                    adset_name = adset.get('name')
                    adset_daily_budget = adset.get('daily_budget')
                    
                    # Check if excluded
                    if adset_id in self.config['excluded_adsets']:
                        print(f"  ⏭️  Skipping excluded ad set: {adset_name}")
                        continue
                    
                    if adset_daily_budget:
                        results['adset_budgets'].append({
                            'id': adset_id,
                            'name': adset_name,
                            'campaign_name': campaign_name,
                            'current_budget': int(adset_daily_budget),
                            'type': 'adset'
                        })
        
        return results
    
    def apply_nightly_budgets(self):
        """Lower budgets to nightly amount and store originals"""
        nightly_amount = self.config['budgets']['nightly_amount']
        results = self.get_active_campaigns_and_adsets()
        
        updates_made = []
        
        print(f"\n💤 Applying nightly budgets (${nightly_amount/100:.2f})...")
        print("   (Storing original budgets for morning restoration)")
        
        # Process campaign-level budgets
        for item in results['campaign_budgets']:
            obj_id = item['id']
            current_budget = item['current_budget']
            
            # Store original budget if not already stored or if it changed
            if obj_id not in self.state['original_budgets'] or \
               self.state['original_budgets'][obj_id] != current_budget:
                self.state['original_budgets'][obj_id] = current_budget
                print(f"  💾 Stored original budget for campaign '{item['name']}': ${current_budget/100:.2f}")
            
            # Only update if current budget is different from nightly
            if current_budget != nightly_amount:
                updates_made.append(self.update_single_budget(
                    obj_id,
                    item['name'],
                    current_budget,
                    nightly_amount,
                    'campaign'
                ))
        
        # Process ad set-level budgets
        for item in results['adset_budgets']:
            obj_id = item['id']
            current_budget = item['current_budget']
            
            # Store original budget if not already stored or if it changed
            if obj_id not in self.state['original_budgets'] or \
               self.state['original_budgets'][obj_id] != current_budget:
                self.state['original_budgets'][obj_id] = current_budget
                print(f"  💾 Stored original budget for ad set '{item['name']}': ${current_budget/100:.2f}")
            
            # Only update if current budget is different from nightly
            if current_budget != nightly_amount:
                updates_made.append(self.update_single_budget(
                    obj_id,
                    item['name'],
                    current_budget,
                    nightly_amount,
                    'adset'
                ))
        
        # Save state after storing originals
        self.save_state()
        
        return updates_made
    
    def apply_daytime_budgets(self):
        """Restore budgets to their original amounts"""
        results = self.get_active_campaigns_and_adsets()
        
        updates_made = []
        
        print(f"\n☀️  Applying daytime budgets (restoring to originals)...")
        
        # Process campaign-level budgets
        for item in results['campaign_budgets']:
            obj_id = item['id']
            current_budget = item['current_budget']
            
            # Get original budget from state
            original_budget = self.state['original_budgets'].get(obj_id)
            
            if original_budget is None:
                # No stored original, keep current
                print(f"  ⚠️  No stored budget for campaign '{item['name']}', keeping current: ${current_budget/100:.2f}")
                continue
            
            # Only update if current is different from original
            if current_budget != original_budget:
                updates_made.append(self.update_single_budget(
                    obj_id,
                    item['name'],
                    current_budget,
                    original_budget,
                    'campaign'
                ))
        
        # Process ad set-level budgets
        for item in results['adset_budgets']:
            obj_id = item['id']
            current_budget = item['current_budget']
            
            # Get original budget from state
            original_budget = self.state['original_budgets'].get(obj_id)
            
            if original_budget is None:
                # No stored original, keep current
                print(f"  ⚠️  No stored budget for ad set '{item['name']}', keeping current: ${current_budget/100:.2f}")
                continue
            
            # Only update if current is different from original
            if current_budget != original_budget:
                updates_made.append(self.update_single_budget(
                    obj_id,
                    item['name'],
                    current_budget,
                    original_budget,
                    'adset'
                ))
        
        return updates_made
    
    def update_single_budget(self, obj_id, name, current_budget, new_budget, obj_type):
        """Update budget for a single campaign or ad set"""
        dry_run = self.config.get('dry_run', True)
        
        update_info = {
            'id': obj_id,
            'name': name,
            'type': obj_type,
            'old_budget': current_budget / 100,
            'new_budget': new_budget / 100,
            'success': False
        }
        
        if dry_run:
            print(f"  🔄 [DRY RUN] Would update {obj_type} '{name}': ${current_budget/100:.2f} → ${new_budget/100:.2f}")
            update_info['success'] = True
            update_info['dry_run'] = True
        else:
            try:
                if obj_type == 'campaign':
                    obj = Campaign(obj_id)
                else:
                    obj = AdSet(obj_id)
                
                obj.api_update(params={'daily_budget': new_budget})
                print(f"  ✅ Updated {obj_type} '{name}': ${current_budget/100:.2f} → ${new_budget/100:.2f}")
                update_info['success'] = True
            except Exception as e:
                print(f"  ❌ Failed to update {obj_type} '{name}': {str(e)}")
                update_info['error'] = str(e)
        
        return update_info
    
    def run(self):
        """Main execution - check time and update budgets accordingly"""
        print("=" * 80)
        print("🕐 Facebook Budget Scheduler V2 Running...")
        print("=" * 80)
        
        mode, current_time = self.get_current_budget_mode()
        
        print(f"\n📅 Current Time: {current_time} ({self.config['timezone']})")
        print(f"🌙☀️  Current Mode: {mode.upper()}")
        
        if self.config.get('dry_run', True):
            print("\n⚠️  DRY RUN MODE - No actual changes will be made")
        
        print("\n" + "-" * 80)
        
        # Check if we need to make changes based on mode
        if mode == 'nightly':
            if self.state.get('last_mode') != 'nightly':
                updates = self.apply_nightly_budgets()
                self.state['last_mode'] = 'nightly'
                self.state['last_run'] = datetime.now(self.timezone).isoformat()
                self.save_state()
            else:
                print("\n✅ Already in nightly mode, no changes needed")
                updates = []
        else:  # daytime
            if self.state.get('last_mode') != 'daytime':
                updates = self.apply_daytime_budgets()
                self.state['last_mode'] = 'daytime'
                self.state['last_run'] = datetime.now(self.timezone).isoformat()
                self.save_state()
            else:
                print("\n✅ Already in daytime mode, no changes needed")
                updates = []
        
        print("\n" + "=" * 80)
        print(f"✅ Scheduler completed: {len(updates)} budget(s) processed")
        if self.state.get('last_run'):
            print(f"📝 Last run: {self.state['last_run']}")
        print("=" * 80)
        
        return updates

def main():
    try:
        scheduler = BudgetScheduler()
        scheduler.run()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main()

