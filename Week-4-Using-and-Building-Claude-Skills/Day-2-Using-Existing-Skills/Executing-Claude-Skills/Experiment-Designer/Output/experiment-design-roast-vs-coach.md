# Experiment Design — Roast Mode vs Coach Mode → Logging Frequency

## 1. Hypothesis (If/Then/Because)

- **If** the AI coach personality is set to **Roast mode** instead of **Coach mode**
- **Then** weekly expense-logging frequency will increase by **≥20%** (from a baseline of 3 entries/week to ≥3.6 entries/week)
- **Because** the sharper, more critical tone increases loss-aversion / social-accountability pressure, making the user more likely to log damage promptly rather than let it pile up unlogged

**Failure condition:** if the 95% CI for the Roast-vs-Coach difference in weekly logging count includes zero (or favors Coach), the hypothesis is not supported.

## 2. Metrics

| Type | Metric | Definition |
|------|--------|------------|
| **Primary** | Weekly expense-logging count | Number of expense entries logged in a given week, tagged by which coach mode was active that week |
| **Guardrail** | Session abandonment | Did the user stop opening the app / disengage more under Roast mode? (qualitative flag — N=1, so this is a self-check, not a stat test) |
| **Secondary (diagnostic only)** | Time-to-log latency | Time between an expense happening and it being logged, per mode |
| **Secondary (diagnostic only)** | Coach interaction sentiment | Subjective: does Roast mode feel motivating or just annoying after repeated exposure? |

## 3. Study Design — this is an N-of-1, not a between-subjects A/B test

CoinQuest has **one user, ~1 session/day**. A standard A/B test (random users → Group A/B) doesn't apply — there's no population to randomize across. The right design here is a **within-subject alternating/crossover design**:

- Unit of observation: **one calendar week**, tagged as either `Coach` or `Roast`.
- Randomize week-mode assignment in matched pairs (e.g., flip a coin for which mode goes first in each 2-week block) to spread out day-of-week/seasonal/life-event confounds instead of a fixed `CCCCRRRR` block, which would confound "mode" with "time passing."
- Keep everything else constant during the test (no other CoinQuest feature changes mid-run — see [Common Pitfalls](../../../../../.claude/skills/experiment-designer/SKILL.md) re: isolating changes).

## 4. Sample Size & Duration

### Why the toolkit's calculator needed adapting

`scripts/sample_size_calculator.py` computes sample size for a **two-proportion z-test** — it expects a conversion-rate metric (0–1) and *independent* trials per group. Two things don't fit this experiment out of the box:

1. **"3 entries/week" is a count/rate, not a proportion.** To use the tool at all, I reframed it as *"probability the user logs ≥1 entry on a given day"* → `3/7 ≈ 0.4286`, with each **day** as one trial. Raw output: [sample_size_raw_output.txt](sample_size_raw_output.txt) → **533 days per arm (1,066 total ≈ 3 years)**.
2. **That result isn't trustworthy as-is**, because the z-test assumes independent trials — but every "trial" here is the same single person, so days aren't independent draws from a population. It also throws away information by collapsing "how many entries" down to "did ≥1 entry happen."

So I cross-checked with the statistically correct method for this design: a **two-sample mean comparison (t-test) on weekly counts**, using the standard sample-size formula:

```
n_per_arm = 2 · σ² · (z_α/2 + z_β)² / Δ²
```

with `σ² ≈ baseline mean = 3` (Poisson-style variance assumption — no historical variance data exists yet, since this experiment hasn't been run), `z_α/2 = 1.96` (α=0.05), `z_β = 0.8416` (power=0.8), and `Δ = baseline × MDE`.

### Result for the requested 20% MDE

| Metric | Value |
|---|---|
| Baseline | 3 entries/week |
| Target (20% relative lift) | 3.6 entries/week |
| Δ (absolute) | 0.6 entries/week |
| **n per arm** | **131 weeks** |
| **Total duration** | **262 weeks (~5 years)** |

**Both methods converge on the same conclusion: a 20% lift on a baseline this small and this noisy is not detectable at conventional rigor (α=0.05, power=0.8) within a timeframe anyone would actually run a personal experiment for.** This isn't a bug in either calculation — it's what happens when the effect size (0.6 entries/week) is small relative to the natural week-to-week noise in a single person's logging habit.

### What's actually achievable — MDE vs. duration tradeoff

Same formula, solved for duration at larger MDEs:

| MDE (relative lift) | Target/week | n per arm | Total duration |
|---|---|---|---|
| 20% | 3.6 | 131 weeks | ~262 weeks (~5 yrs) |
| 35% | 4.05 | 43 weeks | ~86 weeks (~1.6 yrs) |
| 50% | 4.5 | 21 weeks | ~42 weeks (~9.7 mo) |
| 75% | 5.25 | 10 weeks | ~20 weeks (~4.6 mo) |
| 100% (doubling) | 6.0 | 6 weeks | ~12 weeks (~3 mo) |

### Recommendation

Pick one, don't split the difference:

- **Rigorous test:** only worth running if you're willing to commit ~3 months and only care about detecting a **~100% lift or larger** (3 → 6+ entries/week). Anything smaller isn't provable at N=1 on a reasonable timescale.
- **Pragmatic pilot (recommended given this is a personal app, not a company with a research budget):** run **4 weeks Coach / 4 weeks Roast, randomized week order, 8 weeks total.** Treat the result as a **directional signal, not a statistically confirmed effect** — report the point estimate and eyeball the trend, don't claim significance you didn't power for.

## 5. Stopping Rule

Fixed duration, decided in advance (per whichever option above is chosen) — **no early stopping on a good week**. Randomly alternating single-user data is noisy; peeking and stopping on a lucky Roast week is the single easiest way to fool yourself here.

## 6. Known Threats to Validity (N=1 specific)

- **Novelty effect:** Roast mode may boost logging simply for being *new*, independent of tone — a longer run or a second crossover cycle would help separate novelty from a real effect.
- **Order/carryover effects:** logging habits from a Coach week may bleed into the following Roast week. Randomized week-order (not a fixed block) mitigates this but doesn't eliminate it.
- **Autocorrelation:** this person's own weeks aren't independent of each other, which is exactly why the "533 days" proportion-test number and the "131 weeks" t-test number should both be read as *lower bounds under an idealized-independence assumption*, not guarantees.
