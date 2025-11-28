# Budget Scheduler Deployment Guide

This guide covers how to deploy the Facebook Budget Scheduler to run automatically at scheduled times.

## 📋 Overview

The scheduler automatically adjusts your Facebook ad budgets based on time of day:
- **12:00 AM PT** - Switch to nightly (low) budget
- **7:00 AM PT** - Switch to daytime (high) budget

## 🚀 Deployment Options

### Option 1: Local Cron Job (Mac/Linux)

**Best for:** If you have a computer/server that runs 24/7

**Setup:**

1. Make the script executable:
```bash
chmod +x budget_scheduler.py
```

2. Edit your crontab:
```bash
crontab -e
```

3. Add these lines (replace `/path/to/FBMA` with your actual path):
```cron
# Run scheduler every hour to check and adjust budgets
0 * * * * cd /Users/paragchordia/Documents/code/FBMA && /usr/bin/python3 budget_scheduler.py >> /tmp/fb_scheduler.log 2>&1

# OR run only at specific times (12am and 7am PT)
0 0 * * * cd /Users/paragchordia/Documents/code/FBMA && /usr/bin/python3 budget_scheduler.py >> /tmp/fb_scheduler.log 2>&1
0 7 * * * cd /Users/paragchordia/Documents/code/FBMA && /usr/bin/python3 budget_scheduler.py >> /tmp/fb_scheduler.log 2>&1
```

4. View logs:
```bash
tail -f /tmp/fb_scheduler.log
```

**Note:** Make sure your Mac doesn't sleep! Go to System Preferences → Energy Saver → Prevent computer from sleeping.

---

### Option 2: AWS Lambda + EventBridge (Cloud Scheduler)

**Best for:** Reliable, no local machine needed, free tier available

**Setup:**

1. **Install AWS CLI and configure:**
```bash
pip install awscli
aws configure
```

2. **Create deployment package:**
```bash
cd /Users/paragchordia/Documents/code/FBMA
pip install -r requirements.txt -t ./lambda_package
cp budget_scheduler.py lambda_package/
cp config.json lambda_package/
cp .env lambda_package/
cd lambda_package
zip -r ../scheduler_lambda.zip .
```

3. **Create Lambda function:**
   - Go to AWS Console → Lambda
   - Create new function
   - Runtime: Python 3.10
   - Upload `scheduler_lambda.zip`
   - Set handler to: `budget_scheduler.main`
   - Add environment variable: `FACEBOOK_ACCESS_TOKEN` = your token

4. **Set up EventBridge schedule:**
   - Go to EventBridge → Rules
   - Create two rules:
     - Rule 1: cron(0 8 * * ? *) - Triggers at 12am PT (8am UTC)
     - Rule 2: cron(0 15 * * ? *) - Triggers at 7am PT (3pm UTC)
   - Target: Your Lambda function

**Cost:** Free tier includes 1M requests/month (you'll use ~60/month)

---

### Option 3: GitHub Actions (Free Alternative)

**Best for:** Simple, free, no server needed

**Setup:**

1. Create `.github/workflows/scheduler.yml` in your repo:

```yaml
name: Budget Scheduler

on:
  schedule:
    # Runs at 12am PT (8am UTC) every day
    - cron: '0 8 * * *'
    # Runs at 7am PT (3pm UTC) every day
    - cron: '0 15 * * *'
  workflow_dispatch: # Allows manual trigger

jobs:
  adjust-budgets:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run scheduler
      env:
        FACEBOOK_ACCESS_TOKEN: ${{ secrets.FACEBOOK_ACCESS_TOKEN }}
      run: |
        python budget_scheduler.py
```

2. Add your token as a GitHub Secret:
   - Go to repo Settings → Secrets → Actions
   - Add `FACEBOOK_ACCESS_TOKEN`

3. Push to GitHub - it will run automatically!

---

### Option 4: Google Cloud Functions

**Best for:** Similar to AWS Lambda, good if you use Google Cloud

**Setup:**

1. Install gcloud CLI
2. Deploy function:
```bash
gcloud functions deploy budget_scheduler \
  --runtime python310 \
  --trigger-http \
  --entry-point main \
  --set-env-vars FACEBOOK_ACCESS_TOKEN=your_token
```

3. Set up Cloud Scheduler:
```bash
gcloud scheduler jobs create http nightly-budget \
  --schedule="0 0 * * *" \
  --time-zone="America/Los_Angeles" \
  --uri="https://YOUR_FUNCTION_URL"

gcloud scheduler jobs create http daytime-budget \
  --schedule="0 7 * * *" \
  --time-zone="America/Los_Angeles" \
  --uri="https://YOUR_FUNCTION_URL"
```

---

## 🎯 Testing Before Production

1. **Test in dry run mode:**
```bash
python manage_scheduler.py show  # Check dry_run is true
python budget_scheduler.py       # Test run
```

2. **Configure your budgets:**
```bash
python manage_scheduler.py set-budgets 10 50  # $10 nightly, $50 daytime
```

3. **Add exclusions if needed:**
```bash
python manage_scheduler.py exclude-adset 6913347655784
```

4. **Disable dry run when ready:**
```bash
python manage_scheduler.py toggle-dry-run
```

---

## 📊 Management Commands

```bash
# View configuration
python manage_scheduler.py show

# Set budget amounts
python manage_scheduler.py set-budgets 10 50

# Exclude specific ad sets
python manage_scheduler.py exclude-adset <adset_id>

# List all active campaigns
python manage_scheduler.py list

# Toggle dry run mode
python manage_scheduler.py toggle-dry-run
```

---

## 🔍 Monitoring

### Check if scheduler is working:

**Local Cron:**
```bash
tail -f /tmp/fb_scheduler.log
```

**AWS Lambda:**
- Go to CloudWatch → Log Groups → Your Lambda function

**GitHub Actions:**
- Go to your repo → Actions tab

---

## ⚠️ Important Notes

1. **Timezone:** The scheduler uses Pacific Time (America/Los_Angeles)
2. **Dry Run:** Always test with dry_run enabled first
3. **Exclusions:** Add any manual campaigns to exclusion list
4. **Token:** Keep your access token secure and refresh before expiry
5. **Frequency:** Running hourly ensures budget changes happen on time

---

## 🆘 Troubleshooting

**Cron job not running:**
- Check system logs: `grep CRON /var/log/syslog`
- Verify crontab: `crontab -l`
- Check file permissions: `ls -la budget_scheduler.py`

**Budget not changing:**
- Check if dry_run is enabled
- Verify ad sets aren't excluded
- Check Facebook API rate limits

**Token expired:**
- Generate new token in Facebook Business Manager
- Update .env file or cloud environment variables

---

## 📈 Recommended Setup

For most users, I recommend:
1. Start with **Local Cron** for testing
2. Move to **GitHub Actions** for free, reliable cloud scheduling
3. Use **AWS Lambda** if you need more control and monitoring

The scheduler will check budgets every hour and adjust them based on the configured times!

