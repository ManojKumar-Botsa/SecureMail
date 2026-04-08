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

### Observation Example

```python
Observation(email_text="URGENT: verify your password immediately or your account will be suspended")
```

### Action Example

```python
Action(label="phishing")
```

## Reward Rules

The grader uses an ordered severity scale:

`safe (0) -> suspicious (1) -> phishing (2)`

| Prediction vs Actual | Reward |
|---|---|
| Exact match | `1.0` |
| One step away | `0.5` |
| Opposite ends | `0.0` |

This setup penalizes risky misses more than cautious uncertainty.

## Difficulty Tiers

| Tier | Typical pattern |
|---|---|
| Easy | Clear scams, fake domains, obvious pressure language |
| Medium | Ambiguous alerts that need context checks |
| Hard | Professional-looking fraud and subtle social engineering |

## Categories

`credential_theft`, `brand_impersonation`, `bec_fraud`, `invoice_fraud`, `social_engineering`, `account_alert`, `it_impersonation`, `ecommerce_notification`, `internal_communication`, `newsletter`, `prize_scam`, `file_sharing`, `domain_scam`, `identity_theft`

## Run Locally

```bash
pip install -r requirements.txt

# Run keyword baseline across all tasks
python baseline.py

# Launch Streamlit demo
python -m streamlit run app.py
```

## Project Layout

```text
securemail-openenv/
|- env.py          # Environment implementation
|- tasks.py        # Labeled task data
|- grader.py       # Reward function
|- baseline.py     # Keyword baseline script
|- app.py          # Streamlit UI
|- server.py       # FastAPI server
|- openenv.yaml    # Environment spec
|- Dockerfile
`- requirements.txt
```

## Adding Tasks

Append a new item to `TASKS` in `tasks.py`:

```python
{
    "email": "Your email text",
    "label": "safe" | "suspicious" | "phishing",
    "difficulty": "easy" | "medium" | "hard",
    "category": "your_category",
    "explanation": "Why this label is reasonable."
}
```

## License

MIT