Facebook Ads Analysis (OpenAI GPT) - 20251127
================================================================================

Here’s what stands out looking over the last 7 days.

I’ll anchor on days where we actually have trial data (22–25, 27; 26 is missing and early days are mostly subscribe-only).

---

### 1. Overall performance & trend

**High level**

- Data is messy pre–Nov 25 (mostly “subscribe” CPAs, very few start_trial events), but from the 25th onward we can see real **Cost per Trial (CPT)**.
- Comparing **Nov 25 vs Nov 27** (last full “old setup” vs the latest day with the new StartTrial + new creatives):

  - **Nov 25 (older mix, mostly rap install/purchase):**  
    • Spend on ads with measurable trials ≈ **$780**  
    • Estimated trials ≈ **32** → **CPT ≈ $24–25**

  - **Nov 27 (StartTrial campaigns + female/baby creatives):**  
    • Spend on ads with measurable trials ≈ **$1.64k**  
    • Estimated trials ≈ **140–145** → **CPT ≈ $11–12**

  → **Roughly 4–4.5x more trials at ~50% lower CPT** in two days. That’s a big step-change, not noise.

- Early in the 7‑day window (Nov 22–23), CPT on the core “tyson_rap_2_4x5” was often **$50–$400 per trial** when trials even showed up, so what we’re seeing now is a very real improvement, not just a tiny optimization.

**Takeaway:** performance is *trending sharply better* in the last 48 hours, driven by:
- Moving from install/purchase optimization toward **StartTrial optimization**, and
- Introducing **new creative clusters**, especially “female rapper” avatars.

---

### 2. What’s working (with real spend)

I’m going to focus on ads with **$50+ spend in the last 7 days** *and* a measurable trial CPA.

#### a) Female rapper avatars – clear new winners

These are the standouts right now.

**Install campaign – FB_iOS_itoshi_rap_female (Nov 27)**  
- **“06 fbg og – Copy” (ad_id 6916177886184)**  
  - Spend: **$229.30**  
  - Start trial CPA: **$8.49**  
  - CTR: 2.50%, CPC: $0.48, CPI: ~$1.16  
  - Est. trials: ~27  
  → Great volume + great CPT. This is arguably the new benchmark.

- **“07 black_4 – Copy” (ad_id 6916177885984)**  
  - Spend: **$31.42**  
  - Start trial CPA: **$5.24**  
  - CTR: 2.21%, CPC: $0.53, CPI: ~$0.95  
  - Est. trials: ~6  
  → Extremely efficient CPT; just needs more spend to confirm.

**Purchase campaign – FB_iOS_Purchase_itoshi_rap_female_261125 (Nov 27)**  
- **“07 black_4” (ad_id 6916167363584)**  
  - Spend: **$202.73**  
  - Start trial CPA: **$10.14**  
  - CTR: 1.46%, CPC: $1.33, CPI: ~$3.69  
  - Est. trials: ~20  
  → Solid CPT at scale; strong candidate to keep scaling.

- **“06 fbg og” (ad_id 6916167127784)**  
  - Spend: **$124.83**  
  - Start trial CPA: **$12.48**  
  - Est. trials: ~10  
  → Slightly weaker than “07 black_4” but still very healthy.

- **“12 Prerna” (ad_id 6916168066184)**  
  - Spend: **$51.41**  
  - Start trial CPA: **$8.57**  
  - Est. trials: ~6  
  → Good CPT with modest spend. Worth more budget.

**Pattern:**  
Female rapper avatars (especially **Black_4, FBG OG, Prerna**) are **our best cost-per-trial assets right now**, with CPT in the **$8–12 range at meaningful volume**. Top-of-funnel is decent but not extraordinary; the real magic is **high install→trial conversion**.

#### b) StartTrial-optimized “Jesus/Tyson rap” – much better than their install versions

**StartTrial campaign – FB_iOS_Rap_StartTrial_Set1_251125 (Nov 27)**  
- **“jesus_rap_1_4x5” (ad_id 6915585772784)**  
  - Spend: **$123.27**  
  - Start trial CPA: **$7.70**  
  - CTR: 0.99%, CPC: $2.33 (expensive), CPI: ~$5.60  
  - Est. trials: ~16  
  → High CPC/CPI, but **excellent trial rate** – the funnel after install is doing the work.

- **“tyson_rap_2_4x5” (ad_id 6915585773184)**  
  - Spend: **$194.50**  
  - Start trial CPA: **$12.97**  
  - CTR: 1.70%, CPC: $1.53, CPI: ~$6.08  
  - Est. trials: ~15  
  → Solid mid-pack CPT; a good scale lever but not as efficient as Jesus/female variants.

**Purchase campaign – “jesus_rap_1_4x5 – Copy” (ad_id 6913866606784)**  
- Spend: **$133.06**  
- Start trial CPA: **$7.39**  
- Est. trials: ~18  
→ Mirrors the StartTrial performance – Jesus creative tends to **convert better to trial** than Tyson given similar or worse top-of-funnel.

**Install campaign versions are weak by comparison:**

- **“jesus_rap_1_4x5” in FB_iOS_itoshi_rap_set1 (ad_id 6913358815984, Nov 27)**  
  - Spend: **$158.96**  
  - Start trial CPA: **$39.74**  
  → Same creative, same audience style, but **5x worse CPT** when optimized to installs instead of trials.

- **“tyson_rap_2_4x5” in install campaign (ad_id 6913358397984, Nov 27)**  
  - Spend: **$30.73**  
  - Start trial CPA: **$30.73** (likely just 1 trial)  
  → Also much worse than its StartTrial version.

**Pattern:**  
The **StartTrial optimization itself is a huge lever.** Same creative + similar CPC/CPI, but **CPT drops from $30–40+ down to single digits/low teens** when we let the algo optimize directly to trials.

#### c) Baby avatars – promising but still small

- **“10 Asian baby – Copy” (ad_id 6916177448584, rap_baby install, Nov 27)**  
  - Spend: **$12.62**, CPT: **$3.16**, est. trials ≈ 4  
  → Crazy-good early CPT, but spend is tiny. Needs to be scaled before we treat this as a true winner.

- **“11 black baby” (ad_id 6916172721984, purchase baby, Nov 27)**  
  - Spend: **$131.81**, CPT: **$16.48**, est. ~8 trials  
  → Above our current portfolio average ($11–12) but better than legacy rap male. Keep, but lower priority than female/fbg.

**Pattern:**  
Baby avatars look **directionally strong**, especially the **Asian baby video**, but we need more volume to trust it. Black baby is “OK, not amazing” on CPT.

---

### 3. What’s not working (with real spend)

These are the places where money is going out without commensurate trials.

#### a) Legacy rap install campaigns at scale

Across the week, we over-spent on **tyson_rap_2_4x5** and to a lesser extent **jesus_rap_1_4x5** in **install-optimized** campaigns:

- **Nov 23 – tyson_rap_2_4x5 (install, ad_id 6913358397984)**  
  - Spend: **$822.86**, start_trial CPA: **$411.43**  
  → ~2 trials for $800+ of spend.

- **Nov 22 – tyson_rap_2_4x5 – Copy (purchase, ad_id 6913866606584)**  
  - Spend: **$437.06**, subscribe CPA: **$145.69** (no clear trial data)  
  → Very expensive for our primary KPI, even if it does drive some revenue.

- **Nov 23–24 – tyson_rap_2_4x5 – Copy (purchase, ad_id 6913866606584)**  
  - Spend: **$713.14** (23rd), **$393.34** (24th)  
  - Start trial CPA on 24th: **$393+** (1 trial)  
  → (Almost certainly) **thousands in spend for almost no trials.**

Even if purchase ROAS looks okay, from a **trial acquisition** standpoint, this is where a lot of waste lived earlier in the week.

**Funnel diagnosis:**  
- CTRs are actually healthy (1.5–2.6%).  
- CPC/CPI are decent ($0.55–$0.80 CPC; roughly $1.7–$2.8 CPI).  
- The **drop-off is install → trial**. Traffic is cheap, but that audience+creative pairing isn’t converting in-app.

#### b) “Eddie Snoop / rap_set2” isn’t justified yet

On Nov 27, in **FB_iOS_itoshi_rap_set2_271125**:

- **“02 Eddie_Snoop” (ad_id 6916858590184)**  
  - Spend: **$110.84**  
  - Start trial CPA: **$36.95** (≈3 trials)  
  - CTR 1.80%, CPC $0.57, CPI $1.44  
  → Top-of-funnel very comparable to winners, but **trial rate is terrible**.

The rest of rap_set2 units have low spend and no trial signal yet, so right now **we’re mostly paying to learn that Eddie_Snoop doesn’t convert**.

#### c) Older non-rap/non-female concepts (splitscreen, pnp, arrestprank, bday)

Across splitscreen / pnp / arrestprank / bday purchase campaigns:

- **“pose_bday” (ad_id 6914859920984)**  
  - Nov 25: Spend **$110.13**, trial CPA **$55.07**  
  - Nov 24: Spend **$67.20**, no trial CPA but high CPI, poor efficiency  
- **Splitscreen/PnP variants** (creatydesign, kimk-braids, Anime, etc.)  
  - CPIs and CPCs are **2–4x more expensive** than rap/female  
  - Where we do see trial/sample CPAs, they cluster **>$30–50 per trial**

These look **structurally weaker** than the rap/female/baby cluster on *every* part of the funnel (CTR, CPC, CPI and install→trial). 

Unless they have much better LTV (which we don’t see here), they’re not competitive for our UA dollars.

---

### 4. Notable changes, swings & anomalies

A couple of things worth calling out:

1. **CPT step-change around Nov 25–27**  
   - 22–24: Most activity optimized to purchase/installs; any start_trial signal is sparse and very expensive.  
   - 25: First meaningful trial data in rap campaigns; CPT ≈ **$24–25**.  
   - 27: With StartTrial adset + female/fbg + baby, blended CPT on key ads falls to **~$11–12**.
   - This looks like **more than just daily noise** – it’s a structural improvement driven by optimization goal and new creatives.

2. **Same creative, wildly different CPT by optimization type**
   - **“jesus_rap_1_4x5”**:  
     - Install campaign CPT: **$39.74** (Nov 27)  
     - StartTrial campaign CPT: **$7.70**  
     - Purchase campaign CPT: **$7.39**  
   → Strong evidence to **double down on StartTrial/purchase optimization** and **shut off install-optimized versions** of these.

3. **Anomalous trial CPAs (likely due to low event counts)**  
   - e.g. **$393.34** CPT for tyson_rap_2_4x5 – Copy on Nov 24 with only 1 tracked trial.  
   - These spikes are mainly a **low-volume measurement artifact**, but they underline how bad things get when spend is high and conversion tracking is sparse.

4. **No signs of frequency fatigue yet**  
   - Frequency largely **1.0–1.2** on all major spenders.  
   → We have **room to scale** the best creatives before worrying about rot.

5. **New clusters just turned on (female, baby, rap_set2)**  
   - **Female rap**: already out of “promising” and into “clear winner” territory.  
   - **Baby**: still “promising” – great early CPT, low spend.  
   - **rap_set2**: mostly still in the exploratory phase; only Eddie_Snoop has volume and it’s not good.

---

### 5. Questions, hypotheses & next tests

Here’s what I’d dig into and what I’d test next.

#### a) Scale plan & budget reallocation

**Immediate shifts I’d make:**

- **Aggressively scale**:
  - “06 fbg og – Copy” (female install)
  - “07 black_4 – Copy” (female install)
  - “07 black_4” & “06 fbg og” & “12 Prerna” (female purchase)
  - “jesus_rap_1_4x5” in StartTrial and purchase adsets

- **Maintain / cautiously scale**:
  - “tyson_rap_2_4x5” in StartTrial set (solid CPT, not best-in-class)
  - Baby avatars, especially “10 Asian baby – Copy”, with spend caps until we get >$50–100/day and confirm the CPT holds.

- **Downweight or pause**:
  - All **install-optimized versions** of rap creatives where we have significantly worse CPT than their StartTrial counterparts (e.g. jesus_rap_1, tyson_rap_2 under FB_iOS_itoshi_rap_set1).
  - **Eddie_Snoop** and any **rap_set2** units that don’t quickly show <~$15 CPT with >$50 spend.
  - **Splitscreen / pnp / bday / arrestprank** units unless they have superior LTV (need product insight).

#### b) Funnel & creative hypotheses

1. **Female avatars = better intent fit?**  
   - Hypothesis: female rapper avatars resonate more with the **current iOS audience mix** and set more accurate expectations about what the app does (AI avatar videos), leading to higher trial completion.
   - Test:  
     - Clone best male rap hooks but swap in female/baby avatars to isolate “avatar type” effect.  
     - Use same copy & framing, only change the persona.

2. **“Jesus rap” > “Tyson rap” on install→trial**  
   - Jesus variants consistently deliver better trial CPAs than Tyson, despite similar or worse CPCs.
   - Hypothesis: tone/story of the Jesus creative attracts users more likely to complete a trial.
   - Test:
     - **Hybrid creatives**: Tyson-style energy/visuals with clearer Jesus-style “try this in the app in 3 taps” CTA or framing.
     - Landing page/store description alignment for each creative (does the store make the promise explicit?).

3. **Optimization goal matters more than CPI**  
   - Same creatives, similar CPI, very different CPT between install vs StartTrial optimization.
   - Hypothesis: Meta’s delivery is able to find “trial-likely” pockets that installs optimization misses.
   - Test:
     - For each top winner (06 fbg og, 07 black_4, jesus_rap_1), run **A/B: StartTrial vs Purchase vs Install** optimization, same audiences and budgets, track CPT and downstream revenue.

4. **Install → trial drop-off diagnosis**  
   - For underperformers like Eddie_Snoop & install-optimized rap, top-of-funnel KPIs are fine, but CPT is bad.
   - Questions:
     - Are these creatives over‑promising something the app doesn’t deliver immediately?
     - Does their traffic skew to segments (geo/age/gender) that historically under-convert in-app?
   - Use breakdowns to:
     - Identify segments where install→trial is worst and either **exclude** them or **tailor creatives**.

#### c) Measurement & structure cleanup

A few structural things that would help:

- **Standardize the KPI event** across campaigns:
  - Right now we have mixes of `subscribe_*` and `start_trial_*` in different campaigns/days.
  - Make **one canonical optimization event** for trials so that performance is apples-to-apples and the algo can learn more effectively across adsets.

- **Separate testing sandboxes from scaling campaigns**:
  - High-volume testing is great, but several weak concepts (splitscreen, pnp, etc.) have racked up $80–$120 each with poor CPT.
  - Create a **strict test budget ceiling per creative** (e.g. $30–50) and only promote to scale if CPT < target after that.

---

### TL;DR for the team

- **Performance is materially better now** than at the start of the week – last day’s blended CPT on scaled ads is roughly **$11–12 vs. ~$24–25 two days earlier**, and orders of magnitude better than early-week.
- **New hero cluster** is **female rapper avatars** (Black_4, FBG OG, Prerna), especially in **StartTrial/purchase-optimized** campaigns.
- **StartTrial optimization beats installs by a mile** on the same creatives; install-optimized versions of Jesus/Tyson rap should be **deprioritized**.
- **Key waste pockets**: legacy rap install + heavy Eddie_Snoop / splitscreen/pnp spend with high CPT and weak install→trial.
- Next steps: **aggressively shift budget to female + best StartTrial rap creatives**, cap or pause weak clusters, and run a few **structured tests** around optimization goal, persona type, and install→trial funnel.