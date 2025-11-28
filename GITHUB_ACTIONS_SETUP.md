# GitHub Actions Deployment Guide

## 📋 Prerequisites

- GitHub account
- This repository pushed to GitHub
- Facebook access token
- (Optional) Claude API token

## 🚀 Step-by-Step Setup

### Step 1: Push Code to GitHub

If you haven't already created a GitHub repository:

```bash
# Initialize git (already done)
cd /Users/paragchordia/Documents/code/FBMA

# Create a new repository on GitHub.com
# Name it: FBMA (or whatever you prefer)
# Keep it PRIVATE (contains sensitive configs)

# Add remote and push
git remote add origin https://github.com/YOUR_USERNAME/FBMA.git
git branch -M main
git push -u origin main
```

### Step 2: Add GitHub Secrets

1. Go to your repository on GitHub.com
2. Click **Settings** (top menu)
3. Click **Secrets and variables** → **Actions** (left sidebar)
4. Click **New repository secret**

Add these secrets:

**Secret 1: FACEBOOK_ACCESS_TOKEN**
- Name: `FACEBOOK_ACCESS_TOKEN`
- Value: Your Facebook system user token
- Click **Add secret**

**Secret 2: ANTHROPIC_API_KEY** (optional)
- Name: `ANTHROPIC_API_KEY`  
- Value: Your Claude API token
- Click **Add secret**

### Step 3: Disable Dry Run Mode

**Important:** The scheduler needs dry_run disabled to make actual changes.

```bash
python3 manage_scheduler.py toggle-dry-run
```

Verify it's off:
```bash
python3 manage_scheduler.py show
# Should show: Dry Run Mode: False
```

Commit this change:
```bash
git add config.json
git commit -m "Disable dry run for production"
git push
```

### Step 4: Test the Workflow

Before waiting for the scheduled time, test manually:

1. Go to your repository on GitHub
2. Click **Actions** tab (top menu)
3. Click **Facebook Budget Scheduler** (left sidebar)
4. Click **Run workflow** button (right side)
5. Click the green **Run workflow** button in dropdown
6. Wait 30-60 seconds and refresh

You should see a running/completed workflow. Click it to view logs.

### Step 5: Monitor First Runs

The workflow will automatically run at:
- **12:00 AM PT** (midnight) - Lowers budgets to $50
- **7:00 AM PT** - Restores original budgets

**Check logs after first run:**
1. Go to **Actions** tab
2. Click the latest workflow run
3. Click **adjust-budgets** job
4. Expand **Run Budget Scheduler** to see output

### Step 6: Verify in Facebook Ads Manager

After the first automated run:
1. Log into Facebook Ads Manager
2. Check your ad set budgets
3. Confirm they were adjusted correctly

## 📊 Monitoring

### View Workflow Status

- Go to **Actions** tab in your repository
- See history of all runs
- Green checkmark = success
- Red X = failure (click to see error)

### Check Stored Budgets

The workflow saves `budget_state.json` as an artifact:
1. Click on a workflow run
2. Scroll down to **Artifacts**
3. Download `budget-state` to view stored budgets

### Manual Trigger

You can manually run the workflow anytime:
1. Go to **Actions** tab
2. Select **Facebook Budget Scheduler**
3. Click **Run workflow**

## 🔧 Configuration Changes

To modify settings:

```bash
# Change nightly budget
python3 manage_scheduler.py set-nightly-budget 75

# Add/remove exclusions
python3 manage_scheduler.py exclude-adset 123456789
python3 manage_scheduler.py include-adset 123456789

# Commit and push changes
git add config.json
git commit -m "Update scheduler config"
git push
```

Changes take effect on next scheduled run.

## ⏰ Schedule Times

The workflow uses UTC time (GitHub Actions requirement):

| Pacific Time | UTC Time | Purpose |
|--------------|----------|---------|
| 12:00 AM PT  | 8:00 AM UTC | Lower budgets to $50 |
| 7:00 AM PT   | 3:00 PM UTC | Restore original budgets |

**Note:** These times are for PST (standard time). During PDT (daylight saving), times shift by 1 hour. The workflow uses fixed UTC times, so adjust if needed.

## 🐛 Troubleshooting

### Workflow doesn't run
- Check that secrets are added correctly
- Verify repository isn't private with free GitHub account (need Pro for private repo scheduled workflows)
- Check Actions tab for any errors

### Budgets not changing
- Verify dry_run is False in config.json
- Check workflow logs for errors
- Verify Facebook token hasn't expired

### "Resource not accessible by integration" error
- The workflow needs write permissions to commit state changes
- Go to Settings → Actions → General
- Under "Workflow permissions", select "Read and write permissions"

### Token expired
- Generate new Facebook token
- Update GitHub secret: Settings → Secrets → FACEBOOK_ACCESS_TOKEN → Update

## 🎯 Best Practices

1. **Monitor first week** - Check logs daily to ensure proper operation
2. **Token refresh** - Set calendar reminder to refresh Facebook token before expiry
3. **Backup state** - Download budget_state.json artifact weekly
4. **Test changes** - Use manual trigger to test config changes before scheduled run

## 💰 Cost

- ✅ **Free!** - GitHub Actions free tier includes 2,000 minutes/month
- ✅ This workflow uses ~2 minutes per day = 60 minutes/month
- ✅ Well within free tier limits

## 📈 Next Steps

Once running successfully:
- Add email notifications on failure (see GitHub Actions docs)
- Set up Slack webhooks for alerts
- Create dashboard for budget monitoring
- Add performance-based budget adjustments

## 🔒 Security Notes

- Keep repository PRIVATE
- Never commit .env file
- Rotate tokens regularly
- Use GitHub secrets for all sensitive data
- Enable two-factor authentication on GitHub account

