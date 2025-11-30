#!/usr/bin/env python3
"""
Compare Facebook Ads data vs AppsFlyer attribution data
Identifies discrepancies in installs, events, and performance
"""

import os
import csv
from datetime import datetime, timedelta
import pandas as pd

class FBAppsFlyerComparison:
    def __init__(self):
        pass
    
    def load_fb_data(self, date_str):
        """Load Facebook ad data for a specific date"""
        filepath = f"data/ad_overview_{date_str}.csv"
        
        if not os.path.exists(filepath):
            print(f"⚠️  Facebook data not found: {filepath}")
            return None
        
        df = pd.read_csv(filepath)
        print(f"✅ Loaded Facebook data: {len(df)} ads")
        return df
    
    def load_appsflyer_data(self, date_str):
        """Load AppsFlyer data for a specific date"""
        filepath = f"data/appsflyer_fb_{date_str}.csv"
        
        if not os.path.exists(filepath):
            print(f"⚠️  AppsFlyer data not found: {filepath}")
            return None
        
        df = pd.read_csv(filepath)
        print(f"✅ Loaded AppsFlyer data: {len(df)} rows")
        return df
    
    def compare_installs(self, fb_df, af_df, date_str):
        """Compare install counts between Facebook and AppsFlyer"""
        print("\n" + "=" * 80)
        print(f"📊 INSTALL COMPARISON - {date_str}")
        print("=" * 80)
        
        # Get total installs from FB
        fb_installs_col = [col for col in fb_df.columns if 'mobile_app_install' in col.lower()]
        if fb_installs_col:
            fb_total_installs = fb_df[fb_installs_col[0]].astype(float).sum()
        else:
            fb_total_installs = 0
        
        # Get total installs from AF
        af_installs_col = [col for col in af_df.columns if 'install' in col.lower()]
        if af_installs_col:
            af_total_installs = af_df[af_installs_col[0]].astype(float).sum()
        else:
            af_total_installs = 0
        
        print(f"\n📱 Total Installs:")
        print(f"  Facebook reports: {int(fb_total_installs)}")
        print(f"  AppsFlyer tracks: {int(af_total_installs)}")
        
        if fb_total_installs > 0:
            discrepancy = ((af_total_installs - fb_total_installs) / fb_total_installs) * 100
            print(f"  Discrepancy: {discrepancy:+.1f}%")
            
            if abs(discrepancy) > 10:
                print(f"  ⚠️  Significant discrepancy detected!")
            else:
                print(f"  ✅ Attribution within normal range")
        
        return {
            'date': date_str,
            'fb_installs': int(fb_total_installs),
            'af_installs': int(af_total_installs),
            'discrepancy_pct': discrepancy if fb_total_installs > 0 else None
        }
    
    def compare_events(self, fb_df, af_df, date_str, event_name='start_trial'):
        """Compare event counts (e.g., trials) between Facebook and AppsFlyer"""
        print("\n" + "=" * 80)
        print(f"🎯 {event_name.upper()} COMPARISON - {date_str}")
        print("=" * 80)
        
        # Get event count from FB
        fb_event_col = [col for col in fb_df.columns if event_name.lower() in col.lower() and 'action_' in col]
        if fb_event_col:
            fb_events = fb_df[fb_event_col[0]].astype(float).sum()
        else:
            fb_events = 0
        
        # Get event count from AF
        af_event_col = [col for col in af_df.columns if event_name.lower().replace('_', '') in col.lower()]
        if af_event_col:
            af_events = af_df[af_event_col[0]].astype(float).sum()
        else:
            af_events = 0
        
        print(f"\n🎯 Total {event_name}:")
        print(f"  Facebook reports: {int(fb_events)}")
        print(f"  AppsFlyer tracks: {int(af_events)}")
        
        if fb_events > 0:
            discrepancy = ((af_events - fb_events) / fb_events) * 100
            print(f"  Discrepancy: {discrepancy:+.1f}%")
        
        return {
            'event': event_name,
            'fb_events': int(fb_events),
            'af_events': int(af_events)
        }
    
    def compare_daily(self, date_str):
        """Compare Facebook vs AppsFlyer for a specific day"""
        print("\n" + "=" * 80)
        print(f"🔍 COMPARING FACEBOOK vs APPSFLYER - {date_str}")
        print("=" * 80)
        
        # Load both datasets
        fb_df = self.load_fb_data(date_str)
        af_df = self.load_appsflyer_data(date_str)
        
        if fb_df is None or af_df is None:
            print("❌ Cannot compare - missing data")
            return None
        
        # Compare installs
        install_comparison = self.compare_installs(fb_df, af_df, date_str)
        
        # Compare trials
        trial_comparison = self.compare_events(fb_df, af_df, date_str, 'start_trial')
        
        # Save comparison report
        self.save_comparison_report(date_str, install_comparison, trial_comparison, fb_df, af_df)
        
        return {
            'installs': install_comparison,
            'trials': trial_comparison
        }
    
    def save_comparison_report(self, date_str, install_comp, trial_comp, fb_df, af_df):
        """Save comparison report as text file"""
        output_dir = 'comparisons'
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, f'fb_af_comparison_{date_str}.txt')
        
        with open(filepath, 'w') as f:
            f.write(f"Facebook vs AppsFlyer Comparison Report\n")
            f.write(f"Date: {date_str}\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("INSTALL COMPARISON\n")
            f.write("-" * 80 + "\n")
            f.write(f"Facebook Reports: {install_comp['fb_installs']} installs\n")
            f.write(f"AppsFlyer Tracks: {install_comp['af_installs']} installs\n")
            if install_comp['discrepancy_pct']:
                f.write(f"Discrepancy: {install_comp['discrepancy_pct']:+.1f}%\n")
            
            f.write("\n" + "=" * 80 + "\n\n")
            
            f.write("TRIAL COMPARISON\n")
            f.write("-" * 80 + "\n")
            f.write(f"Facebook Reports: {trial_comp['fb_events']} trials\n")
            f.write(f"AppsFlyer Tracks: {trial_comp['af_events']} trials\n")
            
            f.write("\n" + "=" * 80 + "\n")
        
        print(f"\n💾 Comparison report saved: {filepath}")

def main():
    """
    Compare yesterday's Facebook vs AppsFlyer data
    """
    try:
        comparator = FBAppsFlyerComparison()
        
        # Compare yesterday
        yesterday = datetime.now().date() - timedelta(days=1)
        date_str = yesterday.strftime('%Y%m%d')
        
        result = comparator.compare_daily(date_str)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main()

