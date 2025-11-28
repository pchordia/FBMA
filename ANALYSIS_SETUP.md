
# Daily Facebook Ads Analysis System

Automated daily analysis of Facebook Ads performance using Claude AI.

## 🎯 What It Does

Every morning at **8:00 AM PT**:

1. **Downloads Facebook Ads data** from yesterday with comprehensive metrics:
   - Spend, impressions, CPM, reach, frequency
   - Clicks, CPC, CTR, link clicks, outbound clicks
   - Actions (installs, trials, conversions)
   - Cost per action (CPI, CPT)
   - Video engagement metrics
   - Quality rankings

2. **Creates detailed breakdowns**:
   - Ad-level overview
   - Demographics (age, gender)
   - Placements (platform, position)
   - Ad Set-level summary
   - Campaign-level summary

3. **Analyzes with Claude AI** focusing on:
   - Cost Per Trial (CPT) performance
   - Install-to-Trial conversion rates
   - CPI efficiency
   - Creative performance (CTR/CPC)
   - Audience health (CPM)
   - Funnel diagnostics
   - Kill/scale recommendations

4. **Saves results**:
   - CSV files with all metrics
   - Text analysis report
   - Uploaded as GitHub artifacts

## 📊 Key Metrics Tracked

### Must-Have Metrics:
- `spend` - Total spend
- `impressions` - Total impressions
- `cpm` - Cost per 1000 impressions
- `clicks`, `cpc`, `ctr` - Click metrics
- `inline_link_clicks` - More accurate link clicks
- `action_mobile_app_install` - Install count
- `action_[your_trial_event]` - Trial starts
- `cpa_mobile_app_install` - Cost Per Install (CPI)
- `cpa_[your_trial_event]` - Cost Per Trial (CPT)

### Supporting Metrics:
- `reach`, `frequency` - Unique reach and frequency
- `video_p50_watched_actions` - 50% video views
- `video_p75_watched_actions` - 75% video views
- `quality_ranking` - Facebook's quality score
- `engagement_rate_ranking` - Engagement score
- `conversion_rate_ranking` - Conversion score

## 🚀 Quick Start

### Test Locally

```bash
# Download yesterday's data
python3 download_fb_data.py

# Analyze with Claude
python3 analyze_with_claude.py

# Or run both together
python3 daily_analysis.py
```

### Configure Analysis Prompt

Edit `analysis_prompt.txt` to customize:
- Target CPT
- Kill thresholds
- Graduate thresholds
- Analysis priorities

Example:
```
Target CPT: $15
Kill threshold: CPT >$25 after $100 spend
Graduate threshold: CPT <$10 with 20+ trials
```

## 📅 Automated Schedule

The GitHub Action runs automatically at **8:00 AM PT** every day.

**Timeline:**
- 12:00 AM PT - Budget lowered to $50
- 7:00 AM PT - Budgets restored to originals
- 8:00 AM PT - **Data downloaded & analyzed**

## 📁 Output Files

### CSV Files (saved to `data/`):
- `ad_overview_YYYYMMDD.csv` - All ads, all metrics
- `ad_demographics_YYYYMMDD.csv` - Breakdown by age/gender
- `ad_placement_YYYYMMDD.csv` - Breakdown by platform/position
- `adset_overview_YYYYMMDD.csv` - Ad set level summary
- `campaign_overview_YYYYMMDD.csv` - Campaign level summary

### Analysis Reports (saved to `analyses/`):
- `analysis_YYYYMMDD.txt` - Claude's full analysis

All files are uploaded as GitHub Actions artifacts (30-90 day retention).

## 🔍 View Results

### On GitHub:
1. Go to: https://github.com/pchordia/FBMA/actions
2. Click **"Daily Facebook Ads Analysis"**
3. Click on the latest run
4. Scroll to **Artifacts** section
5. Download:
   - `facebook-ads-data` (CSV files)
   - `analysis-report` (Claude's analysis)

### Logs:
Click on the workflow run to see:
- Data download logs
- Claude's analysis preview
- File summaries

## ⚙️ Configuration

### Customize Analysis Prompt

Edit `analysis_prompt.txt`:

```
Target CPT: $15          # Your target cost per trial
Kill threshold: CPT >$25 after $100 spend
Graduate threshold: CPT <$10 with 20+ trials
```

Commit and push changes:
```bash
git add analysis_prompt.txt
git commit -m "Update analysis targets"
git push
```

### Change Schedule

Edit `.github/workflows/daily-analysis.yml`:

```yaml
schedule:
  - cron: '0 16 * * *'  # 8am PT = 4pm UTC (PST)
```

## 📊 Analysis Output Format

Claude provides:

### 1. CPT Summary
- Top 5 and bottom 5 performers
- CPT by campaign, ad set, and ad
- Comparison to target

### 2. Kill List
- Ads/ad sets exceeding kill threshold
- Reasoning for each recommendation
- Alternative strategies

### 3. Scale Candidates
- Best performers under graduate threshold
- Budget increase recommendations
- Expected impact

### 4. Funnel Diagnostics
- Install-to-Trial conversion analysis
- Creative performance breakdown
- Audience health assessment

### 5. Creative Patterns
- What's working (common patterns)
- What's not working
- Testing recommendations

## 🧪 Testing

### Test with Manual Trigger:

1. Go to: https://github.com/pchordia/FBMA/actions/workflows/daily-analysis.yml
2. Click **Run workflow**
3. Select **main** branch
4. Click **Run workflow**

The workflow will run immediately and analyze yesterday's data.

### Test Locally:

```bash
# Set up environment
export FACEBOOK_ACCESS_TOKEN="your_token"
export ANTHROPIC_API_KEY="your_claude_key"

# Run full pipeline
python3 daily_analysis.py

# Check outputs
ls -lh data/
ls -lh analyses/
cat analyses/analysis_*.txt
```

## 📈 What to Do with Analysis

### Daily Routine:

1. **Review Claude's analysis** (8:30 AM)
   - Check CPT summary
   - Review kill list
   - Identify scale candidates

2. **Take action** (by 9:00 AM)
   - Pause underperformers
   - Increase budgets on winners
   - Launch new creative tests

3. **Monitor throughout day**
   - Check Facebook Ads Manager
   - Verify changes applied correctly

### Weekly Review:

- Download all CSV files from artifacts
- Analyze trends over time
- Adjust targets in prompt
- Review creative patterns

## 🔧 Troubleshooting

### No data downloaded:
- Check Facebook token is valid
- Verify ad account has active campaigns
- Check date range (yesterday must have data)

### Claude analysis fails:
- Verify ANTHROPIC_API_KEY is set in GitHub secrets
- Check API quota/limits
- Review error logs in Actions

### Wrong metrics:
- Edit `download_fb_data.py` to add/remove fields
- Check Facebook Ads API documentation
- Test locally before pushing

## 💡 Advanced Customization

### Add More Breakdowns:

Edit `download_fb_data.py`, add to `download_daily_report()`:

```python
# Device breakdown
device_data = self.download_ad_insights(
    date_range,
    level='ad',
    breakdowns=['device_platform']
)
```

Available breakdowns:
- `age`, `gender`
- `country`, `region`
- `device_platform`, `impression_device`
- `publisher_platform`, `platform_position`
- `product_id` (for DPA/catalog ads)

### Customize Analysis Focus:

Edit `analysis_prompt.txt` to focus on:
- Different KPIs (ROAS, LTV, etc.)
- Creative testing insights
- Audience saturation detection
- Competitive intelligence

### Add Slack Notifications:

Add to workflow:
```yaml
- name: Send to Slack
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {"text": "Daily analysis complete!"}
```

## 📚 Resources

- [Facebook Marketing API Docs](https://developers.facebook.com/docs/marketing-apis/)
- [Anthropic Claude API Docs](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)
- [GitHub Actions Docs](https://docs.github.com/en/actions)

## 🎯 Best Practices

1. **Review daily** - Don't let analyses pile up
2. **Act quickly** - Kill losers fast, scale winners faster
3. **Test continuously** - Use insights to inform new creative
4. **Track changes** - Note what actions you took based on analysis
5. **Refine prompt** - Update targets as you learn

---

**Next Steps:**
1. Run manual test to verify setup
2. Review tomorrow's first automated analysis
3. Adjust thresholds based on your goals
4. Set up daily routine for reviewing reports

