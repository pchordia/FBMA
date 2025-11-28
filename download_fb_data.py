#!/usr/bin/env python3
"""
Download Facebook Ads data with comprehensive metrics and breakdowns
Saves as CSV for analysis
"""

import os
import json
from datetime import datetime, timedelta
import csv
import pytz
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights

load_dotenv()

class FacebookDataDownloader:
    def __init__(self):
        self.access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        if not self.access_token:
            raise Exception("FACEBOOK_ACCESS_TOKEN not found in .env file")
        
        FacebookAdsApi.init(access_token=self.access_token)
        self.ad_account_id = 'act_24590952'
        self.account = AdAccount(self.ad_account_id)
        self.timezone = pytz.timezone('America/Los_Angeles')
    
    def get_date_range(self, days_ago=1):
        """Get date range for yesterday (or specified days ago)"""
        today = datetime.now(self.timezone).date()
        target_date = today - timedelta(days=days_ago)
        
        return {
            'since': target_date.strftime('%Y-%m-%d'),
            'until': target_date.strftime('%Y-%m-%d')
        }
    
    def download_ad_insights(self, date_range, level='ad', breakdowns=None):
        """
        Download Facebook Ads insights with comprehensive metrics
        
        Args:
            date_range: dict with 'since' and 'until' keys
            level: 'campaign', 'adset', or 'ad'
            breakdowns: list of breakdowns (e.g., ['age', 'gender'])
        """
        
        # Comprehensive field list
        fields = [
            # Identifiers
            'campaign_id',
            'campaign_name',
            'adset_id',
            'adset_name',
            'ad_id',
            'ad_name',
            
            # Core metrics
            'spend',
            'impressions',
            'reach',
            'frequency',
            
            # Click metrics
            'clicks',
            'cpc',
            'ctr',
            'cpm',
            'cpp',  # Cost per 1000 people reached
            
            # Link clicks (more accurate for conversion tracking)
            'inline_link_clicks',
            'inline_link_click_ctr',
            'cost_per_inline_link_click',
            
            # Outbound clicks (leaving Facebook)
            'outbound_clicks',
            'outbound_clicks_ctr',
            'cost_per_outbound_click',
            
            # Actions (conversions)
            'actions',
            'action_values',
            'cost_per_action_type',
            'conversions',
            'conversion_values',
            'cost_per_conversion',
            
            # Video metrics
            'video_30_sec_watched_actions',
            'video_p25_watched_actions',
            'video_p50_watched_actions',
            'video_p75_watched_actions',
            'video_p100_watched_actions',
            'video_avg_time_watched_actions',
            
            # Quality metrics
            'quality_ranking',
            'engagement_rate_ranking',
            'conversion_rate_ranking',
        ]
        
        params = {
            'time_range': date_range,
            'level': level,
            'time_increment': 1,  # Daily data
        }
        
        if breakdowns:
            params['breakdowns'] = breakdowns
        
        print(f"Fetching {level}-level insights for {date_range['since']}...")
        if breakdowns:
            print(f"  Breakdowns: {', '.join(breakdowns)}")
        
        try:
            insights = self.account.get_insights(
                fields=fields,
                params=params
            )
            
            data = []
            for insight in insights:
                row = insight.export_all_data()
                data.append(row)
            
            print(f"  ✅ Downloaded {len(data)} rows")
            return data
            
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            return []
    
    def flatten_actions(self, data):
        """
        Flatten the 'actions' and 'cost_per_action_type' fields
        Creates separate columns for each action type
        """
        flattened_data = []
        
        for row in data:
            flat_row = {}
            
            # Copy all non-action fields
            for key, value in row.items():
                if key not in ['actions', 'action_values', 'cost_per_action_type', 
                              'conversions', 'conversion_values', 'video_30_sec_watched_actions',
                              'video_p25_watched_actions', 'video_p50_watched_actions',
                              'video_p75_watched_actions', 'video_p100_watched_actions',
                              'video_avg_time_watched_actions']:
                    flat_row[key] = value
            
            # Flatten actions
            if 'actions' in row and row['actions']:
                for action in row['actions']:
                    action_type = action.get('action_type', 'unknown')
                    action_value = action.get('value', 0)
                    flat_row[f'action_{action_type}'] = action_value
            
            # Flatten cost per action
            if 'cost_per_action_type' in row and row['cost_per_action_type']:
                for action in row['cost_per_action_type']:
                    action_type = action.get('action_type', 'unknown')
                    action_value = action.get('value', 0)
                    flat_row[f'cpa_{action_type}'] = action_value
            
            # Flatten video metrics
            video_metrics = [
                'video_30_sec_watched_actions',
                'video_p25_watched_actions',
                'video_p50_watched_actions',
                'video_p75_watched_actions',
                'video_p100_watched_actions',
                'video_avg_time_watched_actions'
            ]
            
            for metric in video_metrics:
                if metric in row and row[metric]:
                    for item in row[metric]:
                        action_type = item.get('action_type', 'unknown')
                        action_value = item.get('value', 0)
                        flat_row[f'{metric}_{action_type}'] = action_value
            
            flattened_data.append(flat_row)
        
        return flattened_data
    
    def save_to_csv(self, data, filename):
        """Save data to CSV file"""
        if not data:
            print(f"⚠️  No data to save for {filename}")
            return None
        
        # Get all unique keys from all rows
        all_keys = set()
        for row in data:
            all_keys.update(row.keys())
        
        fieldnames = sorted(list(all_keys))
        
        filepath = f"data/{filename}"
        os.makedirs('data', exist_ok=True)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"✅ Saved to {filepath} ({len(data)} rows)")
        return filepath
    
    def download_daily_report(self, days_ago=1):
        """Download daily report with essential breakdowns only"""
        date_range = self.get_date_range(days_ago)
        date_str = date_range['since'].replace('-', '')
        
        print("=" * 80)
        print(f"📊 Downloading Facebook Ads Data for {date_range['since']}")
        print("=" * 80)
        
        reports = {}
        
        # 1. Ad-level overview (no breakdowns) - MAIN FILE
        print("\n1. Ad-level overview (main file)...")
        ad_data = self.download_ad_insights(date_range, level='ad')
        if ad_data:
            flat_data = self.flatten_actions(ad_data)
            reports['ad_overview'] = self.save_to_csv(
                flat_data, 
                f'ad_overview_{date_str}.csv'
            )
        
        # 2. Age breakdown
        print("\n2. Age breakdown...")
        age_data = self.download_ad_insights(
            date_range, 
            level='ad',
            breakdowns=['age']
        )
        if age_data:
            flat_data = self.flatten_actions(age_data)
            reports['age'] = self.save_to_csv(
                flat_data,
                f'ad_by_age_{date_str}.csv'
            )
        
        # 3. Gender breakdown
        print("\n3. Gender breakdown...")
        gender_data = self.download_ad_insights(
            date_range,
            level='ad',
            breakdowns=['gender']
        )
        if gender_data:
            flat_data = self.flatten_actions(gender_data)
            reports['gender'] = self.save_to_csv(
                flat_data,
                f'ad_by_gender_{date_str}.csv'
            )
        
        # 4. Placement breakdown
        print("\n4. Placement breakdown...")
        placement_data = self.download_ad_insights(
            date_range,
            level='ad',
            breakdowns=['publisher_platform']
        )
        if placement_data:
            flat_data = self.flatten_actions(placement_data)
            reports['placement'] = self.save_to_csv(
                flat_data,
                f'ad_by_placement_{date_str}.csv'
            )
        
        print("\n" + "=" * 80)
        print(f"✅ Download complete! {len(reports)} reports saved")
        print("=" * 80)
        
        return reports

def main():
    try:
        downloader = FacebookDataDownloader()
        
        # Download yesterday's data
        reports = downloader.download_daily_report(days_ago=1)
        
        # Print summary
        print("\n📁 Files created:")
        for report_type, filepath in reports.items():
            if filepath:
                print(f"  - {report_type}: {filepath}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main()

