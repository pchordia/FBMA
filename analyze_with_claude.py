#!/usr/bin/env python3
"""
Analyze Facebook Ads data using Claude AI
"""

import os
import csv
from datetime import datetime, timedelta
import anthropic
from dotenv import load_dotenv

load_dotenv()

class ClaudeAnalyzer:
    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise Exception("ANTHROPIC_API_KEY not found in .env file")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        
        # Load analysis prompt
        with open('analysis_prompt.txt', 'r') as f:
            self.analysis_prompt = f.read()
    
    def read_csv_to_text(self, filepath, max_rows=None):
        """Convert CSV to formatted text for Claude"""
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        if not rows:
            return None
        
        # Format as a readable table
        text = f"\n{'='*80}\n{os.path.basename(filepath)}\n{'='*80}\n"
        text += f"Total rows: {len(rows)}\n\n"
        
        # Limit rows if specified
        rows_to_show = rows[:max_rows] if max_rows else rows
        
        # Include rows for detailed analysis
        for i, row in enumerate(rows_to_show, 1):
            text += f"\n--- Row {i} ---\n"
            for key, value in row.items():
                if value:  # Only include non-empty values
                    text += f"{key}: {value}\n"
        
        if max_rows and len(rows) > max_rows:
            text += f"\n... and {len(rows) - max_rows} more rows\n"
        
        return text
    
    def prepare_data_summary(self, date_str):
        """Prepare CSV data for analysis - main overview only, breakdowns as summaries"""
        data_dir = 'data'
        
        data_summary = ""
        
        # 1. Ad-level overview - FULL FILE (this is the main data)
        ad_file = os.path.join(data_dir, f'ad_overview_{date_str}.csv')
        if os.path.exists(ad_file):
            data_summary += self.read_csv_to_text(ad_file) + "\n"
        
        # For breakdowns, note that they exist but don't include full data
        # (Claude can infer patterns from the main ad overview)
        data_summary += "\n" + "="*80 + "\n"
        data_summary += "BREAKDOWN DATA AVAILABLE (not shown to save space):\n"
        data_summary += "="*80 + "\n"
        
        age_file = os.path.join(data_dir, f'ad_by_age_{date_str}.csv')
        if os.path.exists(age_file):
            data_summary += f"✓ Age breakdown: {self.count_rows(age_file)} rows\n"
        
        gender_file = os.path.join(data_dir, f'ad_by_gender_{date_str}.csv')
        if os.path.exists(gender_file):
            data_summary += f"✓ Gender breakdown: {self.count_rows(gender_file)} rows\n"
        
        placement_file = os.path.join(data_dir, f'ad_by_placement_{date_str}.csv')
        if os.path.exists(placement_file):
            data_summary += f"✓ Placement breakdown: {self.count_rows(placement_file)} rows\n"
        
        data_summary += "\nNote: Focus analysis on the ad_overview data above.\n"
        
        return data_summary
    
    def count_rows(self, filepath):
        """Count rows in a CSV file"""
        with open(filepath, 'r') as f:
            return sum(1 for _ in f) - 1  # Subtract header row
    
    def analyze(self, date_str):
        """Send data to Claude for analysis"""
        print("=" * 80)
        print("🤖 Starting Claude AI Analysis")
        print("=" * 80)
        
        # Prepare data
        print("\n📊 Loading CSV data...")
        data_summary = self.prepare_data_summary(date_str)
        
        if not data_summary:
            print("❌ No data found for analysis")
            return None
        
        print(f"✅ Data loaded ({len(data_summary)} characters)")
        
        # Construct message for Claude
        message_content = f"""{self.analysis_prompt}

DATA FOR ANALYSIS:
{data_summary}

Please provide a comprehensive analysis following the structure outlined above.
Focus on actionable insights and specific recommendations."""
        
        print("\n🔄 Sending to Claude...")
        
        try:
            # Call Claude API
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                messages=[
                    {
                        "role": "user",
                        "content": message_content
                    }
                ]
            )
            
            analysis = message.content[0].text
            
            print("✅ Analysis received!")
            print("\n" + "=" * 80)
            print("📊 CLAUDE'S ANALYSIS")
            print("=" * 80)
            print(analysis)
            print("=" * 80)
            
            # Save analysis to file
            output_dir = 'analyses'
            os.makedirs(output_dir, exist_ok=True)
            
            output_file = os.path.join(output_dir, f'analysis_{date_str}.txt')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"Facebook Ads Analysis - {date_str}\n")
                f.write("=" * 80 + "\n\n")
                f.write(analysis)
            
            print(f"\n💾 Analysis saved to: {output_file}")
            
            return analysis
            
        except Exception as e:
            print(f"❌ Error calling Claude API: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def analyze_yesterday(self):
        """Analyze yesterday's data"""
        yesterday = datetime.now().date() - timedelta(days=1)
        date_str = yesterday.strftime('%Y%m%d')
        
        return self.analyze(date_str)

def main():
    try:
        analyzer = ClaudeAnalyzer()
        analyzer.analyze_yesterday()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main()

