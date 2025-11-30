# AppsFlyer Manual Data Workflow

Until API access is fully working, use this manual workflow to get AppsFlyer data for FB vs AF comparison.

## 📥 Step 1: Export from AppsFlyer Dashboard

### Daily Export (Recommended):

1. Log into **AppsFlyer Dashboard**
2. Go to **Reports** → **Overview** → **Partners** (or **Analytics** → **Partners**)
3. Set filters:
   - **Date Range:** Single day (e.g., Nov 27, 2025)
   - **Media Source:** Facebook
   - **Group By:** Add Campaign, Ad Set, Ad (if available)
4. Click **Export** → **CSV**
5. Save the file (e.g., `appsflyer_2025-11-27.csv`)

### What to Export:

Make sure your export includes these columns:
- Media Source
- Campaign / Campaign ID
- Ad Set / Ad Set ID  
- Ad / Ad ID
- **Installs**
- **Events** (start_trial, purchase, etc.)
- **Revenue**
- **Cost** (if available)

## 📂 Step 2: Import into System

```bash
# Import the CSV
python import_appsflyer_csv.py ~/Downloads/appsflyer_export.csv 20251127

# Or let it prompt you for the date
python import_appsflyer_csv.py ~/Downloads/appsflyer_export.csv
```

This will copy the file to: `data/appsflyer_fb_YYYYMMDD.csv`

## 🔍 Step 3: Compare FB vs AF

```bash
# Compare yesterday's data
python compare_fb_af.py
```

This will show:
- Install discrepancies (FB reported vs AF attributed)
- Trial discrepancies
- Attribution differences
- Saves report to: `comparisons/fb_af_comparison_YYYYMMDD.txt`

## 📅 Daily Routine:

**Morning (8:30 AM):**
1. Review automated GPT-5.1 analysis (GitHub Actions)
2. Export yesterday's AppsFlyer data (2 mins)
3. Import: `python import_appsflyer_csv.py ~/Downloads/export.csv`
4. Compare: `python compare_fb_af.py`
5. Review discrepancies
6. Make kill/scale decisions with validated data

## ⚡ Quick Export Tips:

### Pre-configured Report:
- Create a **saved report** in AppsFlyer with your filters
- Click it daily → Export → Done in 30 seconds

### Batch Export:
- Can export multiple days at once
- Import each day separately with the date parameter

## 🔄 When API Access Works:

Once AppsFlyer API is confirmed working:
1. The `download_appsflyer_data.py` script will work automatically
2. GitHub Actions can include AppsFlyer download
3. Manual exports no longer needed

Until then, this manual workflow ensures **data accuracy and MMP validation** for your decisions.

## ⚠️ Why This Matters:

**Facebook self-reported installs ≠ AppsFlyer attributed installs**

Common discrepancies:
- **View-through attribution** - FB counts, AF might not
- **Attribution windows** - Different settings
- **Install validation** - AF has fraud detection
- **Delayed postbacks** - Timing differences

Typical variance: **5-15%**

If discrepancy >20% → investigation needed.

## 📊 Expected Workflow Time:

- **Daily:** 2-3 minutes to export & import AF data
- **Analysis:** Automated by GPT-5.1
- **Decisions:** Based on validated FB+AF data

This ensures you're making decisions on **verified attribution data**, not just Facebook's view of performance.

