#!/usr/bin/env python3
"""
Daily Analysis Pipeline:
1. Download Facebook Ads data
2. Analyze with Claude AI
3. Save results
"""

from download_fb_data import FacebookDataDownloader
from analyze_with_claude import ClaudeAnalyzer
from datetime import datetime, timedelta

def main():
    print("=" * 80)
    print("📊 DAILY FACEBOOK ADS ANALYSIS PIPELINE")
    print("=" * 80)
    
    yesterday = datetime.now().date() - timedelta(days=1)
    date_str = yesterday.strftime('%Y%m%d')
    
    try:
        # Step 1: Download data
        print("\n📥 STEP 1: Downloading Facebook Ads data...")
        print("-" * 80)
        downloader = FacebookDataDownloader()
        reports = downloader.download_daily_report(days_ago=1)
        
        if not reports:
            print("❌ No data downloaded, aborting analysis")
            exit(1)
        
        # Step 2: Analyze with Claude
        print("\n\n🤖 STEP 2: Analyzing with Claude AI...")
        print("-" * 80)
        analyzer = ClaudeAnalyzer()
        analysis = analyzer.analyze(date_str)
        
        if not analysis:
            print("❌ Analysis failed")
            exit(1)
        
        # Summary
        print("\n\n" + "=" * 80)
        print("✅ DAILY ANALYSIS COMPLETE")
        print("=" * 80)
        print(f"Date analyzed: {yesterday.strftime('%Y-%m-%d')}")
        print(f"Reports generated: {len(reports)}")
        print(f"Analysis saved: analyses/analysis_{date_str}.txt")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Pipeline failed: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main()

