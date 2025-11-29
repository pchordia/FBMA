#!/usr/bin/env python3
"""
Analyze Facebook Ads data using OpenAI GPT-4 with reasoning
"""

import os
import csv
from datetime import datetime, timedelta
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class OpenAIAnalyzer:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise Exception("OPENAI_API_KEY not found in .env file")
        
        self.client = OpenAI(api_key=self.api_key)
        
        # Load analysis prompt
        with open('analysis_prompt.txt', 'r') as f:
            self.analysis_prompt = f.read()
    
    def read_csv_to_text(self, filepath):
        """Convert CSV to formatted text for analysis"""
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
    
    def count_rows(self, filepath):
        """Count rows in a CSV file"""
        with open(filepath, 'r') as f:
            return sum(1 for _ in f) - 1  # Subtract header row
    
    def prepare_data_summary(self, date_str):
        """Prepare CSV data for analysis - main overview for last 7 days"""
        data_dir = 'data'
        
        data_summary = ""
        data_summary += "="*80 + "\n"
        data_summary += "FACEBOOK ADS DATA - LAST 7 DAYS\n"
        data_summary += "="*80 + "\n\n"
        
        # Get the date for yesterday
        yesterday = datetime.strptime(date_str, '%Y%m%d').date()
        
        # Load data for each of the past 7 days
        for days_ago in range(7):
            target_date = yesterday - timedelta(days=days_ago)
            target_date_str = target_date.strftime('%Y%m%d')
            
            ad_file = os.path.join(data_dir, f'ad_overview_{target_date_str}.csv')
            
            if os.path.exists(ad_file):
                data_summary += f"\n{'='*80}\n"
                data_summary += f"DAY {days_ago+1}: {target_date.strftime('%Y-%m-%d')} ({days_ago} days ago)\n"
                data_summary += f"{'='*80}\n"
                data_summary += self.read_csv_to_text(ad_file) + "\n"
            else:
                data_summary += f"\n⚠️ No data for {target_date.strftime('%Y-%m-%d')}\n"
        
        # Note about breakdown data (available but not sent to save tokens)
        data_summary += "\n" + "="*80 + "\n"
        data_summary += "BREAKDOWN DATA AVAILABLE (not shown):\n"
        data_summary += "="*80 + "\n"
        data_summary += "Age, gender, and placement breakdowns exist for each day above.\n"
        data_summary += "Focus analysis on the ad_overview data shown.\n"
        
        return data_summary
    
    def analyze(self, date_str):
        """Send data to OpenAI for analysis"""
        print("=" * 80)
        print("🤖 Starting OpenAI GPT Analysis")
        print("=" * 80)
        
        # Prepare data
        print("\n📊 Loading CSV data...")
        data_summary = self.prepare_data_summary(date_str)
        
        if not data_summary:
            print("❌ No data found for analysis")
            return None
        
        print(f"✅ Data loaded ({len(data_summary)} characters)")
        
        # Construct message
        message_content = f"""{self.analysis_prompt}

DATA FOR ANALYSIS:
{data_summary}

Please provide your analysis in a conversational, insights-focused format as described above."""
        
        print("\n🔄 Sending to OpenAI GPT-5.1 (with reasoning)...")
        
        try:
            # Call OpenAI API with GPT-5.1 using new responses.create format
            result = self.client.responses.create(
                model="gpt-5.1",
                input=message_content,
                reasoning={"effort": "medium"},  # Use medium reasoning effort for thorough analysis
                text={"verbosity": "medium"}
            )
            
            analysis = result.output_text
            
            print("✅ Analysis received!")
            print("\n" + "=" * 80)
            print("📊 OPENAI'S ANALYSIS")
            print("=" * 80)
            print(analysis)
            print("=" * 80)
            
            # Save analysis to file
            output_dir = 'analyses'
            os.makedirs(output_dir, exist_ok=True)
            
            output_file = os.path.join(output_dir, f'analysis_openai_{date_str}.txt')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"Facebook Ads Analysis (OpenAI GPT) - {date_str}\n")
                f.write("=" * 80 + "\n\n")
                f.write(analysis)
            
            print(f"\n💾 Analysis saved to: {output_file}")
            
            return analysis
            
        except Exception as e:
            print(f"❌ Error calling OpenAI API: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def analyze_last_7_days(self):
        """Analyze last 7 days of data"""
        yesterday = datetime.now().date() - timedelta(days=1)
        date_str = yesterday.strftime('%Y%m%d')
        
        return self.analyze(date_str)

def main():
    try:
        analyzer = OpenAIAnalyzer()
        analyzer.analyze_last_7_days()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main()

