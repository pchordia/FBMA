#!/usr/bin/env python3
"""
Download Facebook Ads data for the past 7 days
"""

from download_fb_data import FacebookDataDownloader
from datetime import datetime, timedelta

def main():
    print("=" * 80)
    print("📊 DOWNLOADING LAST 7 DAYS OF FACEBOOK ADS DATA")
    print("=" * 80)
    
    try:
        downloader = FacebookDataDownloader()
        
        all_reports = {}
        
        # Download data for each of the past 7 days
        for days_ago in range(1, 8):  # 1 to 7 days ago
            date = (datetime.now().date() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
            
            print(f"\n{'='*80}")
            print(f"Downloading data for {date} ({days_ago} days ago)")
            print(f"{'='*80}")
            
            reports = downloader.download_daily_report(days_ago=days_ago)
            all_reports[date] = reports
        
        print("\n\n" + "=" * 80)
        print("✅ 7-DAY DOWNLOAD COMPLETE")
        print("=" * 80)
        
        for date, reports in all_reports.items():
            print(f"\n{date}: {len(reports)} files")
            for report_type, filepath in reports.items():
                if filepath:
                    print(f"  - {report_type}")
        
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main()

