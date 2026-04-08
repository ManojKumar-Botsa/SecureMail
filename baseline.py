from env import PhishingEnv
from tasks import TASKS

KEYWORDS = {
    "phishing": [
        "urgent",
        "verify",
        "password",
        "click here",
        "suspend",
        "suspended",
        "login",
        "confirm",
        "account",
        "claim",
        "winner",
        "prize",
        "act now",
        "immediately",
        "restricted",
        "update your billing",
        "confirm your",
        "validate",
    ],
    "suspicious": [
        "unusual",
        "unrecognized",
        "new device",
        "expire",
        "expiring",
        "security audit",
        "routine",
        "no action needed",
        "if this was you",
        "24 hours",
        "7 days",
        "reminder",
    ],
}


def predict(email_text: str) -> str:
    text = email_text.lower()

    phishing_score = sum(1 for kw in KEYWORDS["phishing"] if kw in text)
    suspicious_score = sum(1 for kw in KEYWORDS["suspicious"] if kw in text)

    if phishing_score >= 2:
        return "phishing"
    if phishing_score == 1 or suspicious_score >= 1:
        return "suspicious"
    return "safe"


env = PhishingEnv()

results = {"easy": [], "medium": [], "hard": []}
total_reward = 0

print("=" * 60)
print("SecureMail Baseline - Full Task Evaluation")
print("=" * 60)

for task in TASKS:
    obs = env.reset_with_task(task)
    action = predict(obs.email_text)
    obs, reward, done, info = env.step({"label": action})

    total_reward += reward
    results[info["difficulty"]].append(reward)

    status = "OK" if reward == 1.0 else ("NEAR" if reward == 0.5 else "MISS")
    print(f"[{status}] [{info['difficulty'].upper():6}] reward={reward:.1f}")
    print(f"      Email    : {obs.email_text[:72]}...")
    print(f"      Predicted: {action:10}  Actual: {task['label']}")
    print()

print("=" * 60)
print("Results by difficulty:")
for diff, rewards in results.items():
    if rewards:
        avg = sum(rewards) / len(rewards)
        perfect = sum(1 for r in rewards if r == 1.0)
        print(f"  {diff.capitalize():8}: avg={avg:.2f}  exact={perfect}/{len(rewards)}")

print()
print(f"Overall average reward : {total_reward / len(TASKS):.3f}")
print(f"Total tasks evaluated  : {len(TASKS)}")
print("=" * 60)
