#!/usr/bin/env python3
"""
Management CLI for Budget Scheduler - Add/remove exclusions, configure budgets
"""

import json
import sys
import os
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

load_dotenv()

class SchedulerManager:
    def __init__(self, config_path='config.json'):
        self.config_path = config_path
        self.config = self.load_config()
        
        # Initialize FB API
        access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        if access_token:
            FacebookAdsApi.init(access_token=access_token)
            self.account = AdAccount('act_24590952')
    
    def load_config(self):
        with open(self.config_path, 'r') as f:
            return json.load(f)
    
    def save_config(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
        print(f"✅ Configuration saved to {self.config_path}")
    
    def show_config(self):
        """Display current configuration"""
        print("\n" + "=" * 80)
        print("📋 Current Budget Scheduler Configuration")
        print("=" * 80)
        
        print(f"\n⏰ Schedule:")
        print(f"  Timezone: {self.config['timezone']}")
        print(f"  Nightly Time (low budget): {self.config['schedule']['nightly_time']}")
        print(f"  Daytime Time (high budget): {self.config['schedule']['daytime_time']}")
        
        print(f"\n💰 Budget Amounts:")
        nightly = self.config['budgets']['nightly_amount']
        daytime = self.config['budgets']['daytime_amount']
        print(f"  Nightly Amount: ${nightly/100:.2f} ({nightly} cents)")
        print(f"  Daytime Amount: ${daytime/100:.2f} ({daytime} cents)")
        
        print(f"\n🚫 Exclusions:")
        print(f"  Excluded Ad Sets: {len(self.config['excluded_adsets'])}")
        for adset_id in self.config['excluded_adsets']:
            print(f"    - {adset_id}")
        
        print(f"  Excluded Campaigns: {len(self.config['excluded_campaigns'])}")
        for campaign_id in self.config['excluded_campaigns']:
            print(f"    - {campaign_id}")
        
        print(f"\n⚙️  Settings:")
        print(f"  Dry Run Mode: {self.config.get('dry_run', True)}")
        
        print("=" * 80 + "\n")
    
    def set_budgets(self, nightly_dollars, daytime_dollars):
        """Set budget amounts in dollars"""
        self.config['budgets']['nightly_amount'] = int(nightly_dollars * 100)
        self.config['budgets']['daytime_amount'] = int(daytime_dollars * 100)
        self.save_config()
        print(f"✅ Budgets updated: Nightly=${nightly_dollars:.2f}, Daytime=${daytime_dollars:.2f}")
    
    def exclude_adset(self, adset_id):
        """Add an ad set to exclusion list"""
        if adset_id not in self.config['excluded_adsets']:
            self.config['excluded_adsets'].append(adset_id)
            self.save_config()
            print(f"✅ Ad Set {adset_id} added to exclusion list")
        else:
            print(f"⚠️  Ad Set {adset_id} is already excluded")
    
    def include_adset(self, adset_id):
        """Remove an ad set from exclusion list"""
        if adset_id in self.config['excluded_adsets']:
            self.config['excluded_adsets'].remove(adset_id)
            self.save_config()
            print(f"✅ Ad Set {adset_id} removed from exclusion list")
        else:
            print(f"⚠️  Ad Set {adset_id} is not in exclusion list")
    
    def exclude_campaign(self, campaign_id):
        """Add a campaign to exclusion list"""
        if campaign_id not in self.config['excluded_campaigns']:
            self.config['excluded_campaigns'].append(campaign_id)
            self.save_config()
            print(f"✅ Campaign {campaign_id} added to exclusion list")
        else:
            print(f"⚠️  Campaign {campaign_id} is already excluded")
    
    def include_campaign(self, campaign_id):
        """Remove a campaign from exclusion list"""
        if campaign_id in self.config['excluded_campaigns']:
            self.config['excluded_campaigns'].remove(campaign_id)
            self.save_config()
            print(f"✅ Campaign {campaign_id} removed from exclusion list")
        else:
            print(f"⚠️  Campaign {campaign_id} is not in exclusion list")
    
    def toggle_dry_run(self):
        """Toggle dry run mode"""
        current = self.config.get('dry_run', True)
        self.config['dry_run'] = not current
        self.save_config()
        
        if self.config['dry_run']:
            print("✅ Dry run mode ENABLED - No actual changes will be made")
        else:
            print("⚠️  Dry run mode DISABLED - Budget changes will be applied!")
    
    def list_active_items(self):
        """List all active campaigns and ad sets that would be affected"""
        print("\n" + "=" * 80)
        print("📊 Active Campaigns and Ad Sets")
        print("=" * 80)
        
        try:
            campaigns = self.account.get_campaigns(
                fields=['id', 'name', 'daily_budget'],
                params={'effective_status': ['ACTIVE']}
            )
            
            print("\n🎯 Active Campaigns:")
            for campaign in campaigns:
                campaign_id = campaign.get('id')
                is_excluded = campaign_id in self.config['excluded_campaigns']
                status = "❌ EXCLUDED" if is_excluded else "✅ INCLUDED"
                budget = campaign.get('daily_budget')
                budget_str = f"${int(budget)/100:.2f}" if budget else "No budget set"
                print(f"  {status} - {campaign.get('name')} (ID: {campaign_id}) - Budget: {budget_str}")
            
            print("\n" + "=" * 80 + "\n")
        except Exception as e:
            print(f"❌ Error fetching campaigns: {str(e)}")

def print_usage():
    """Print usage instructions"""
    print("""
📖 Budget Scheduler Management Tool

Usage:
  python manage_scheduler.py [command] [arguments]

Commands:
  show                          - Show current configuration
  set-budgets <nightly> <day>   - Set budget amounts in dollars
                                  Example: set-budgets 10 50
  exclude-adset <id>            - Exclude an ad set from scheduling
  include-adset <id>            - Include an ad set in scheduling
  exclude-campaign <id>         - Exclude a campaign from scheduling
  include-campaign <id>         - Include a campaign in scheduling
  toggle-dry-run                - Toggle dry run mode on/off
  list                          - List all active campaigns and ad sets
  
Examples:
  python manage_scheduler.py show
  python manage_scheduler.py set-budgets 10 50
  python manage_scheduler.py exclude-adset 6913347655784
  python manage_scheduler.py toggle-dry-run
    """)

def main():
    if len(sys.argv) < 2:
        print_usage()
        return
    
    manager = SchedulerManager()
    command = sys.argv[1].lower()
    
    try:
        if command == 'show':
            manager.show_config()
        
        elif command == 'set-budgets':
            if len(sys.argv) < 4:
                print("❌ Error: Please provide nightly and daytime amounts")
                print("Example: python manage_scheduler.py set-budgets 10 50")
                return
            nightly = float(sys.argv[2])
            daytime = float(sys.argv[3])
            manager.set_budgets(nightly, daytime)
        
        elif command == 'exclude-adset':
            if len(sys.argv) < 3:
                print("❌ Error: Please provide ad set ID")
                return
            manager.exclude_adset(sys.argv[2])
        
        elif command == 'include-adset':
            if len(sys.argv) < 3:
                print("❌ Error: Please provide ad set ID")
                return
            manager.include_adset(sys.argv[2])
        
        elif command == 'exclude-campaign':
            if len(sys.argv) < 3:
                print("❌ Error: Please provide campaign ID")
                return
            manager.exclude_campaign(sys.argv[2])
        
        elif command == 'include-campaign':
            if len(sys.argv) < 3:
                print("❌ Error: Please provide campaign ID")
                return
            manager.include_campaign(sys.argv[2])
        
        elif command == 'toggle-dry-run':
            manager.toggle_dry_run()
        
        elif command == 'list':
            manager.list_active_items()
        
        else:
            print(f"❌ Unknown command: {command}")
            print_usage()
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main()

