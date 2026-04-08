TASKS = [
    # ------------------------------------------------------------
    # EASY: obvious phishing signals
    # ------------------------------------------------------------
    {
        "email": "URGENT: verify your password immediately or your account will be suspended",
        "label": "phishing",
        "difficulty": "easy",
        "category": "credential_theft",
        "explanation": "High-pressure language and a password request in one message.",
    },
    {
        "email": "Congratulations! You have won $1,000,000. Click here to claim your prize now!",
        "label": "phishing",
        "difficulty": "easy",
        "category": "prize_scam",
        "explanation": "Unsolicited prize messages with urgent links are a common scam pattern.",
    },
    {
        "email": "Your PayPal account has been limited. Login immediately at paypa1-secure.com to restore access.",
        "label": "phishing",
        "difficulty": "easy",
        "category": "brand_impersonation",
        "explanation": "The domain is spoofed (paypa1 vs paypal) and asks for immediate login.",
    },
    {
        "email": "Dear Customer, your Netflix subscription has expired. Update your billing details to avoid losing access: netflix-billing-update.com",
        "label": "phishing",
        "difficulty": "easy",
        "category": "brand_impersonation",
        "explanation": "It imitates a known brand and sends users to an untrusted domain.",
    },
    {
        "email": "ACTION REQUIRED: Your bank account has been locked. Call 1-800-555-FAKE or click here to unlock now.",
        "label": "phishing",
        "difficulty": "easy",
        "category": "credential_theft",
        "explanation": "The message uses fear and urgency to push immediate action.",
    },

    # ------------------------------------------------------------
    # EASY: clearly safe
    # ------------------------------------------------------------
    {
        "email": "Hi team, the all-hands meeting is rescheduled to Friday at 3 PM. Please update your calendars.",
        "label": "safe",
        "difficulty": "easy",
        "category": "internal_communication",
        "explanation": "Routine scheduling update with no risky request.",
    },
    {
        "email": "Your Amazon order #112-3456789 has shipped and will arrive by Thursday. Track your package here.",
        "label": "safe",
        "difficulty": "easy",
        "category": "ecommerce_notification",
        "explanation": "Typical order status email; no credential or payment-change request.",
    },
    {
        "email": "Thanks for subscribing to our newsletter! Here's your weekly digest of top tech articles.",
        "label": "safe",
        "difficulty": "easy",
        "category": "newsletter",
        "explanation": "Standard newsletter content with no pressure or sensitive data request.",
    },

    # ------------------------------------------------------------
    # MEDIUM: needs context and judgment
    # ------------------------------------------------------------
    {
        "email": "We noticed a login to your Google account from a new device in Chennai, India. If this was you, no action needed. If not, secure your account here.",
        "label": "suspicious",
        "difficulty": "medium",
        "category": "account_alert",
        "explanation": "Could be real, but this format is often copied by phishing campaigns.",
    },
    {
        "email": "Your password will expire in 3 days. Please reset it using your company portal to maintain access.",
        "label": "suspicious",
        "difficulty": "medium",
        "category": "it_impersonation",
        "explanation": "Password expiry notices are normal, but sender and link context are missing.",
    },
    {
        "email": "Hi, I am reaching out on behalf of your CEO regarding an urgent and confidential wire transfer. Please reply only to this email.",
        "label": "phishing",
        "difficulty": "medium",
        "category": "bec_fraud",
        "explanation": "Classic business email compromise: fake authority plus secrecy around money.",
    },
    {
        "email": "We are upgrading our email servers this weekend. Please confirm your login credentials to ensure uninterrupted service.",
        "label": "phishing",
        "difficulty": "medium",
        "category": "it_impersonation",
        "explanation": "Legitimate IT teams do not request credentials by email.",
    },
    {
        "email": "Your Dropbox file 'Q3_Report.pdf' has been shared with you by john.doe@company.com. Click to view.",
        "label": "suspicious",
        "difficulty": "medium",
        "category": "file_sharing",
        "explanation": "Looks normal, but similar notifications are frequently used for malware delivery.",
    },
    {
        "email": "Dear valued customer, we are conducting a routine security audit. Please verify your identity by confirming your date of birth and last 4 digits of your SSN.",
        "label": "phishing",
        "difficulty": "medium",
        "category": "identity_theft",
        "explanation": "Sensitive identity data should not be collected through unsolicited email.",
    },

    # ------------------------------------------------------------
    # HARD: subtle and professional-looking
    # ------------------------------------------------------------
    {
        "email": "Following up on our conversation last week - I've attached the revised invoice as discussed. Please process it at your earliest convenience. Let me know if you need anything else.",
        "label": "phishing",
        "difficulty": "hard",
        "category": "invoice_fraud",
        "explanation": "This is a common invoice-fraud style message that relies on fake prior context.",
    },
    {
        "email": "Hi Sarah, just checking in - did you get a chance to review the proposal I sent Monday? Happy to jump on a call to walk you through it.",
        "label": "safe",
        "difficulty": "hard",
        "category": "business_followup",
        "explanation": "Normal professional follow-up with no red-flag request.",
    },
    {
        "email": "As part of our annual compliance review, all employees are required to complete the attached security awareness training by end of month. IT Security Team.",
        "label": "suspicious",
        "difficulty": "hard",
        "category": "it_impersonation",
        "explanation": "Could be legitimate, but attachments and generic sender style warrant caution.",
    },
    {
        "email": "Your recent login from an unrecognized device was successful. If you did not initiate this, please contact support within 24 hours.",
        "label": "suspicious",
        "difficulty": "hard",
        "category": "account_alert",
        "explanation": "Plausible security alert, but could be social engineering without trusted contact details.",
    },
    {
        "email": "We noticed you haven't logged in for 90 days. Your account will be deactivated unless you log in within the next 7 days.",
        "label": "suspicious",
        "difficulty": "hard",
        "category": "account_alert",
        "explanation": "Inactivity notices are common, but this pressure pattern is also used in phishing.",
    },
    {
        "email": "Please find attached the updated vendor payment details for next month's invoice cycle. Kindly update your records accordingly. Regards, Accounts Team.",
        "label": "phishing",
        "difficulty": "hard",
        "category": "bec_fraud",
        "explanation": "Changing payment routing by email is a high-risk fraud indicator.",
    },
    {
        "email": "Hi, I'm from the IT helpdesk. We've detected a conflict on your workstation that may affect performance. Could you share your current username so we can look into it?",
        "label": "phishing",
        "difficulty": "hard",
        "category": "social_engineering",
        "explanation": "Low-friction info requests can be the first step in credential escalation.",
    },
    {
        "email": "Good morning, this is a reminder that your domain registration for securemail.io expires in 14 days. Renew now to avoid disruption.",
        "label": "suspicious",
        "difficulty": "hard",
        "category": "domain_scam",
        "explanation": "Domain renewal reminders can be real or spoofed; sender validation is required.",
    },

    # ------------------------------------------------------------
    # ADDITIONAL: balance label distribution
    # ------------------------------------------------------------
    {
        "email": "Hi, just a reminder that the office will be closed on Monday for the public holiday. See you Tuesday!",
        "label": "safe",
        "difficulty": "easy",
        "category": "internal_communication",
        "explanation": "Simple internal notice with no risky action requested.",
    },
    {
        "email": "Your monthly bank statement for March 2026 is now available. Log in to your account to view it.",
        "label": "suspicious",
        "difficulty": "medium",
        "category": "account_alert",
        "explanation": "Could be legitimate, but this template is heavily imitated by phishing emails.",
    },
    {
        "email": "Hey, wanted to follow up - did you get a chance to look at the slides I shared for Thursday's presentation? No rush, just checking!",
        "label": "safe",
        "difficulty": "hard",
        "category": "business_followup",
        "explanation": "Friendly follow-up with no request for credentials, money, or urgent action.",
    },
]
