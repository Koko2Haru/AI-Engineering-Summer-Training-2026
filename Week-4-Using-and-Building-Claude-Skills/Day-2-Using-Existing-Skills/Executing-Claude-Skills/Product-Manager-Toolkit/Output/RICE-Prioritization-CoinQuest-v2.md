# RICE Prioritization — CoinQuest v2.0

Ran with the [product-manager-toolkit](../../../../.claude/skills/product-manager-toolkit) RICE prioritizer (`rice_prioritizer.py`) against the v2.0 backlog listed in [COINQUEST-V10.md](../../../../Week-2-AI-Assisted-Development/Day-5-Polishing-and-Shipping/COINQUEST-V10.md#-future-upgrades-v20-and-beyond).

## Methodology note — adapting Reach for a single user

RICE's `Reach` is defined as "users affected per quarter." CoinQuest currently has **one user (you), ~1 session/day**, so a literal user-count would flatten every feature to `Reach = 1` and the framework would collapse. Instead, `Reach` here means **sessions per quarter (~90) in which the feature is actually exercised or experienced** — a proxy for how often it touches your actual usage, which is the thing RICE is trying to capture anyway. `Impact`, `Confidence`, and `Effort` keep their standard definitions (effort is loosely "focused solo dev sessions," not literal person-months).

- **90** = daily-touch features (seen/used essentially every session)
- **26** = Healing Potions, estimated ~2x/week (side income isn't a daily event)
- **16** = Reports/comparison tool, estimated ~weekly + occasional monthly checks

## Scored Features

| Rank | Feature | Reach | Impact | Confidence | Effort | RICE Score |
|------|---------|------:|--------|------------|--------|-----------:|
| 1 | **Healing Passive** (daily/monthly income) | 90 | massive | high | m | **54.0** |
| 2 | **Healing Potions** (side income) | 26 | medium | high | xs | **26.0** |
| 3 | **Sound Design + BGM** | 90 | low | high | s | **15.0** |
| 4 | **Achievements** | 90 | medium | medium | m | **14.4** |
| 5 | **Player Character with Equipment** | 90 | medium | medium | l | **9.0** |
| 6 | **Animated Boss** | 90 | low | medium | l | **4.5** |
| 7 | **Weekly/Monthly/Yearly Reports + Comparison Tool** | 16 | high | medium | l | **3.2** |

Raw input/output: [coinquest-v2-features.csv](coinquest-v2-features.csv), [rice_results.json](rice_results.json)

## Portfolio Analysis

- **Quick wins (high/massive impact, xs/s effort):** none outright, but **Healing Passive** is close (massive impact at only medium effort) — it's the standout.
- **Big bets (high/massive impact, l/xl effort):** Reports + Comparison Tool.
- **Effort distribution:** 1× xs, 1× s, 2× m, 3× l — the backlog leans effort-heavy (3 of 7 features are `l`), so expect the roadmap to stretch across several sessions/months rather than a fast sprint.
- **Average RICE:** 18.0 — Healing Passive is a clear outlier at 3x the average.

## ⚠️ Where RICE undersells the backlog

RICE's `Reach × Impact` math structurally rewards **daily-touch, low-effort** features and penalizes **infrequent-but-deep** ones. Two results are worth overriding on judgment rather than taking the score at face value:

- **Reports + Comparison Tool ranks last (3.2)** purely because it's checked weekly, not daily — but it's arguably the *point* of a finance tracker (turning logged damage into insight). Low reach, not low value.
- **Sound Design + BGM ranks 3rd (15.0)** mostly because it's touched every session — but it's cosmetic polish with no effect on financial behavior. High reach, not high value.

If you want the RICE order to double as your build order, swap these two mentally: treat **Reports** as a second-tier priority (right after Healing Potions) and let **Sound Design** slide toward the end, since it changes nothing about how the app works.

## Suggested Build Order

1. **Healing Passive** — completes the core healing/damage loop (the game literally has no "healing" yet); highest score by a wide margin.
2. **Healing Potions** — cheap follow-on to #1, reuses the same income-entry pattern, very low effort.
3. **Weekly/Monthly/Yearly Reports + Comparison Tool** — judgment override (see above); this is the actual utility payoff of a finance tracker and unblocks reflecting on the healing/income data you'll now have.
4. **Achievements** — motivational layer, moderate effort, benefits from #1–#3 already existing (streaks/thresholds to hook into).
5. **Player Character with Equipment** — visual reinforcement of the core loop; do before the Boss since it's tied to the same HP mechanic you already have.
6. **Animated Boss** — cosmetic, higher effort for similar payoff to #5; nice-to-have once the core loop feels complete.
7. **Sound Design + BGM** — lowest-impact polish; save for a final "shipping" pass, same role it played in v1.0.

## Assumptions to revisit

- Effort sizes assume solo AI-paired dev sessions (Claude Code), not literal person-months — treat them as *relative* sizing (xs < s < m < l), not calendar estimates.
- Reach estimates for Healing Potions (26/quarter) and Reports (16/quarter) are guesses about your own usage cadence — adjust and re-run if your actual habits differ:
  ```
  python rice_prioritizer.py coinquest-v2-features.csv --capacity 4
  ```
