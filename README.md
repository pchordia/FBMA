# Facebook Marketing Automation (FBMA)

Automated budget scheduling for Facebook ad campaigns with smart budget restoration.

## 🌟 Features

- **Smart Budget Scheduling**: Automatically adjusts budgets based on time of day
- **Budget Memory**: Remembers original budgets and restores them (not forced to same amount)
- **Pacific Time Aware**: Runs on PST/PDT timezone
- **Exclusion System**: Opt out specific campaigns or ad sets
- **Dry Run Mode**: Test changes before applying them
- **Easy Management**: Simple CLI tools for configuration

## 🕐 How It Works

### Nightly Mode (12:00 AM PT)
- Reduces all active ad set budgets to $50
- Stores each ad set's original budget before changing

### Daytime Mode (7:00 AM PT)
- Restores each ad set to its original budget
- If an ad set was $500, it goes back to $500
- If it was $100, it goes back to $100

### Example:
```
Before midnight:
  Ad Set A: $500
  Ad Set B: $200
  Ad Set C: $100

At 12:00 AM:
  All reduced to $50 (originals stored)

At 7:00 AM:
  Ad Set A: Back to $500
  Ad Set B: Back to $200
  Ad Set C: Back to $100
```

## 🚀 Quick Start

### 1. Setup
```bash
# Install dependencies
pip3 install -r requirements.txt

# Configure your token in .env
# FACEBOOK_ACCESS_TOKEN=your_token_here
```

### 2. Test the System
```bash
# View current configuration
python3 manage_scheduler.py show

# Test the full day/night cycle
python3 test_scheduler.py

# Run the scheduler manually
python3 budget_scheduler_v2.py
```

### 3. Configure

```bash
# Set nightly budget amount
python3 manage_scheduler.py set-nightly-budget 50

# Exclude an ad set from automation
python3 manage_scheduler.py exclude-adset 6913347655784

# List all active campaigns
python3 manage_scheduler.py list

# Disable dry run when ready
python3 manage_scheduler.py toggle-dry-run
```

### 4. Deploy

See [SCHEDULER_DEPLOYMENT.md](SCHEDULER_DEPLOYMENT.md) for deployment options:
- Local cron job (Mac/Linux)
- AWS Lambda (Recommended)
- GitHub Actions (Free!)
- Google Cloud Functions

## 📋 Management Commands

```bash
# View configuration and stored budgets
python3 manage_scheduler.py show

# Set nightly budget to $50
python3 manage_scheduler.py set-nightly-budget 50

# Exclude/include ad sets
python3 manage_scheduler.py exclude-adset <adset_id>
python3 manage_scheduler.py include-adset <adset_id>

# Exclude/include campaigns
python3 manage_scheduler.py exclude-campaign <campaign_id>
python3 manage_scheduler.py include-campaign <campaign_id>

# Toggle dry run on/off
python3 manage_scheduler.py toggle-dry-run

# List all active campaigns and ad sets
python3 manage_scheduler.py list
```

## 📁 Files

- `budget_scheduler_v2.py` - Main scheduler (use this!)
- `manage_scheduler.py` - Configuration management CLI
- `test_scheduler.py` - Test script for simulations
- `config.json` - Configuration (budgets, exclusions, schedule)
- `budget_state.json` - Stores original budgets (auto-generated)
- `.env` - Your Facebook access token (keep secure!)

## 🔒 Security

- `.env` file is gitignored - never commit your token!
- Use system user tokens for long-term automation
- Refresh tokens before expiry

## ⚙️ Configuration

Edit `config.json`:

```json
{
  "timezone": "America/Los_Angeles",
  "budgets": {
    "nightly_amount": 5000,  // $50 in cents
    "restore_original": true
  },
  "schedule": {
    "nightly_time": "00:00",  // 12:00 AM
    "daytime_time": "07:00"   // 7:00 AM
  },
  "excluded_adsets": [],
  "excluded_campaigns": [],
  "dry_run": true  // Set to false when ready for production
}
```

## 🧪 Testing

Always test before going live:

1. Keep `dry_run: true` in config
2. Run `python3 test_scheduler.py` to simulate full cycle
3. Review the output carefully
4. When satisfied, toggle dry run: `python3 manage_scheduler.py toggle-dry-run`
5. Monitor logs for first few days

## 📊 Monitoring

Check if scheduler is running correctly:

```bash
# View stored budgets and last run
python3 manage_scheduler.py show

# Check state file
cat budget_state.json

# For cron jobs, check logs
tail -f /tmp/fb_scheduler.log
```

## ⚠️ Important Notes

1. **Exclusions**: Any ad sets you manage manually should be added to exclusions
2. **Budget Changes**: If you manually change a budget during the day, it will be stored as the "original" at next midnight
3. **New Ad Sets**: Automatically included unless you exclude them
4. **Timezone**: System uses Pacific Time - adjust in config if needed

## 🆘 Troubleshooting

**Budgets not changing:**
- Check if dry_run is enabled
- Verify ad sets aren't in exclusion list
- Check Facebook API rate limits

**State file issues:**
- Delete `budget_state.json` to reset
- System will recreate it on next run

**Token expired:**
- Generate new token in Facebook Business Manager
- Update `.env` file

## 📈 Future Enhancements

- Performance-based budget adjustments
- Multi-account support
- Web dashboard
- Slack/email notifications
- Budget rules based on ROAS

## 📄 License

Private use only - Telepathic, Inc.

