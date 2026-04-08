---
title: SecureMail OpenEnv
sdk: docker
app_port: 7860
---

# SecureMail OpenEnv

A small OpenEnv-style environment for phishing email classification.

This project was built for the Meta x Hugging Face x PyTorch OpenEnv Hackathon.

## What This Environment Tests

The agent reads one email body and chooses one label:

- `safe`
- `suspicious`
- `phishing`

The task set mixes obvious phishing with realistic business email patterns, so simple keyword rules are not enough on harder samples.

## Environment Summary

| Property | Value |
|---|---|
| Observation space | Raw email body text (`str`) |
| Action space | `safe` / `suspicious` / `phishing` |
| Total tasks | 25 |
| Difficulty tiers | easy / medium / hard |
| Max reward | 1.0 |

## Reward Rules

The grader uses an ordered severity scale:

`safe (0) -> suspicious (1) -> phishing (2)`

| Prediction vs Actual | Reward |
|---|---|
| Exact match | `1.0` |
| One step away | `0.5` |
| Opposite ends | `0.0` |

This setup penalizes risky misses more than cautious uncertainty.

## Difficulty Breakdown

- `easy`: 9 tasks
- `medium`: 7 tasks
- `hard`: 9 tasks

## Categories

`credential_theft`, `brand_impersonation`, `bec_fraud`, `invoice_fraud`, `social_engineering`, `account_alert`, `it_impersonation`, `ecommerce_notification`, `internal_communication`, `newsletter`, `prize_scam`, `file_sharing`, `domain_scam`, `identity_theft`, `business_followup`

## Run Locally

```bash
pip install -r requirements.txt
python baseline.py
python -m streamlit run app.py
```

## Project Layout

```text
securemail-openenv/
|- env.py
|- tasks.py
|- grader.py
|- baseline.py
|- app.py
|- server.py
|- inference.py
|- openenv.yaml
|- Dockerfile
`- requirements.txt
```

## License

MIT
