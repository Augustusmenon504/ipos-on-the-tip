# IPOs on the Tip

A web app for analysing Indian mainboard IPOs and estimating their listing-day move.

**Live site:** https://YOUR-USERNAME.github.io/ipos-on-the-tip/

## What it does
- **Listed IPOs:** 267 mainboard IPOs listed between June 2024 and November 2026, searchable and sortable, each with issue price, issue size, QIB / HNI / retail subscription and listing-day open and close.
- **Growth Predictor:** estimates the listing-open gain from QIB (institutional) subscription, with a typical error range and the implied opening price.
- **Forum:** one discussion thread per IPO. On this GitHub version, posts are saved in the visitor's own browser.

## The model
`listing-open gain % = -18.08 + 9.98 × ln(1 + QIB subscription)`

| Check | Error (mean absolute) | Guessing the average |
|---|---|---|
| Leave-one-out, all 267 IPOs | 13.7 pts | 18.4 pts |
| Trained on 2024–25, tested on 2026 (102 IPOs) | 11.8 pts | 18.1 pts |

R² = 0.41. Adding HNI and retail subscription improved the error by only ~0.3 points, so the model keeps QIB alone. Reproduce it with `python model/fit_model.py`.

## Data
`data/ipos.csv`, from the Trendlyne IPO screener (2024 closing prices cross-checked against Navia). InvITs and REITs are excluded. A few early-September 2026 listings are missing.

## Team and credits
College project at Kishinchand Chellaram College, Mumbai (2024–25), led by Augustus Menon with Amaan Shaikh and Sumith Nankani. The team designed the platform and built the original front-end prototype. The 2026 version adds the dataset, the working predictor and the forum, built with help from Claude (AI).

*For learning only, not investment advice.*
