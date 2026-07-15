# 🚢 Day 5 — Polishing & Shipping: CoinQuest v1.0

> **Week 2 — AI-Assisted Development · Day 5 Deliverable**
> From a plain white page to a full gamified finance RPG — in one day of AI pair-programming with Claude Code. 🎮💰

---

## 📍 Where We Started: v0.5

After applying the milestones from `SPECS.md`, the app *worked* — but it was rough:

- ❌ No background color — just plain white
- ❌ Default browser fonts and inputs
- ❌ A single budget bar, one pie chart, a basic expense list
- ❌ XP logic that rewarded *spending* (yes, really — more on that below)

![CoinQuest v0.5 — plain white, default fonts](/Week-2-AI-Assisted-Development/Day-5-Polishing-and-Shipping/CoinQuest-v1/screenshots/v05-before.png)

Functional? Yes. Shippable? Not yet. So I called it **v0.5** and started grinding, component by component. Every version bump below is one focused upgrade session with Claude Code.

---

## 🗡️ v0.6 — The Damage History (formerly "expense list")

The boring expense list became a proper **Damage History** log:

- ✅ **Delete one, many, or all** — checkboxes with a *Select all* option, for when you fat-finger an entry
- 🔃 **Sorting** — up/down on multiple columns: damage amount, date, and category
- 🎨 **Severity levels** — every damage entry gets a color-coded level, from **LOW** 🟢 all the way to **FATAL** 💀
- 💬 **WhatsApp-style notes** — long notes get truncated with a *show more* toggle, so the table stays clean without hiding your info

![Damage History — sorting, multi-select delete, severity levels](/Week-2-AI-Assisted-Development/Day-5-Polishing-and-Shipping/CoinQuest-v1/screenshots/v06-damage-history.png)

## 🪙 v0.7 — The Coin Adder (formerly "log an expense")

The entry form got a full quality-of-life pass:

- 📅 **Calendar date picker** — comfortably pick any date instead of typing it
- ✍️ **Custom categories** — choosing *Other* reveals a text field so you can type exactly what it was (e.g. "Prime Subscription")
- 🐛 **Fixed the reset annoyance** — the category no longer snaps back to *Food* after every log, so entering multiple Bills or Transport damages in a row is painless
- 💵💳 **Payment method** — every damage is now tagged as **Cash** or **Credit**

| Standard entry | Custom category on *Other* |
|---|---|
| ![Coin Adder with date picker and payment method](/Week-2-AI-Assisted-Development/Day-5-Polishing-and-Shipping/CoinQuest-v1/screenshots/v07-coin-adder.png) | ![Custom category field revealed](/Week-2-AI-Assisted-Development/Day-5-Polishing-and-Shipping/CoinQuest-v1/screenshots/v07-custom-category.png) |

## 🧙 v0.8 — The AI Coach

- Tested **multiple models** head-to-head to find the one with the best balance of response quality and **speed**
- The three personalities are live: 🛡️ **Coach**, 🔥 **Roast**, and 🏴‍☠️ **Pirate**
- Boss report shows damage dealt + your spending weakness

## 📊 v0.9 — Cash vs Credit Analytics

Since damages are now split by payment method, the charts should be too:

- 🥧 The **pie chart** stays as the overview: everything, cash + credit combined
- 📊 Below it: **two dedicated bar charts** — one for Cash, one for Credit — each showing Coins / Spent / Remaining
- 💯 **Percentages everywhere** — now you can see exactly which category hit you hardest, and *where* (physical vs electronic spending)

![Cash vs Credit — dedicated bar charts for each payment method](/Week-2-AI-Assisted-Development/Day-5-Polishing-and-Shipping/CoinQuest-v1/screenshots/v09-cash-vs-credit.png)

## ✨ v1.0 — The Final Boss of Polish

The last session tied everything together:

- 📊 **Separate budget bars** — Cash, Credit, and Total each get their own HP bar, and *Edit coins* lets you set the cash and credit budgets independently
- ⚡ **XP rework** — the old logic gave you XP for *adding an expense*… which rewards spending money. Counterintuitive! New logic:
  - XP grows based on **how long you survive without spending**
  - 1 hour clean → 100 XP, and it keeps doubling hour after hour (100 + 200 + ...)
  - Log a damage → 💥 **XP resets to 0**
  - Now the game actually rewards *not spending*. That's the whole point of a finance tracker!
- 🔤 **Poppins font** (Google Fonts) — way more eye-appealing and alive than the browser default
- 🌊 **Glossy, wavy animated background** — subtle color blobs and waves moving behind the UI, making the whole app feel lively instead of flat

![Separate Cash, Credit, and Total budget bars with Edit coins](/Week-2-AI-Assisted-Development/Day-5-Polishing-and-Shipping/CoinQuest-v1/screenshots/v10-budget-bars.png)

![CoinQuest v1.0 — Poppins, animated background, pie chart + AI Coach](/Week-2-AI-Assisted-Development/Day-5-Polishing-and-Shipping/CoinQuest-v1/screenshots/v10-overview.png)

---

## 🆚 Before & After

| | v0.5 | v1.0 |
|---|---|---|
| **Look** | White page, default fonts | Animated glossy background, Poppins |
| **Budget** | One bar | Cash + Credit + Total bars, editable |
| **Charts** | One pie | Pie + 2 bar charts, with percentages |
| **Expense list** | Plain rows | Sortable, multi-delete, severity levels, expandable notes |
| **Entry form** | Basic, resets to Food | Date picker, custom categories, payment method |
| **XP** | Rewarded spending 🤦 | Rewards *surviving* without spending |
| **AI** | Untested | Model-tested Coach / Roast / Pirate |

---

## 🔮 Future Upgrades (v2.0 and beyond)

v1.0 is just the beginning. The backlog:

- 💱 **More damage types & currencies** — cheque support, USD, AUD, etc.
- ❤️‍🩹 **Healing passive** — recurring income (daily allowance, monthly salary)
- 🧪 **Healing potions** — preset amounts (50 / 100 / 250 / 1000) or custom, for side-hustle income
- 🏆 **Achievements** — "don't spend for X time", "keep HP above X%"
- 📅 **Weekly / monthly / yearly reports** + a comparison tool
- 🐉 **A living boss** — an animated monster that gets more terrifying the more damage you take
- ⚔️ **A player character** — earn shields and weapons by healing; lose equipment as HP drops, until you hit FATAL 💀
- 🔊 **Sound design** — click and hover SFX, background music

---

## 🎓 Reflection

Five days ago this was a one-page spec. Today it's a working, polished, gamified finance tracker with an AI coach — built end to end alongside Claude Code, one version bump at a time. The biggest lesson of Day 5: **polish is iterative**. No single prompt made the app good; ten focused sessions did.

**CoinQuest v1.0 — shipped.** 🚀

![CoinQuest v1.0 — the full dashboard](/Week-2-AI-Assisted-Development/Day-5-Polishing-and-Shipping/CoinQuest-v1/screenshots/v10-full-dashboard.png)