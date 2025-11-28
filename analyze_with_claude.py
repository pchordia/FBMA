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
    
    def read_csv_to_text(self, filepath):
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
        
        # Include all rows for detailed analysis
        for i, row in enumerate(rows, 1):
            text += f"\n--- Row {i} ---\n"
            for key, value in row.items():
                if value:  # Only include non-empty values
                    text += f"{key}: {value}\n"
        
        return text
    
    def prepare_data_summary(self, date_str):
        """Prepare all CSV data for analysis"""
        data_dir = 'data'
        
        # Find all CSVs for the date
        csv_files = [
            f'ad_overview_{date_str}.csv',
            f'ad_demographics_{date_str}.csv',
            f'ad_placement_{date_str}.csv',
            f'adset_overview_{date_str}.csv',
            f'campaign_overview_{date_str}.csv',
        ]
        
        data_summary = ""
        
        for csv_file in csv_files:
            filepath = os.path.join(data_dir, csv_file)
            csv_text = self.read_csv_to_text(filepath)
            if csv_text:
                data_summary += csv_text + "\n"
        
        return data_summary
    
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

