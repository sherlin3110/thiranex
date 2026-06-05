import re
import random
import string

# Common weak passwords
COMMON_PASSWORDS = [
    "password", "123456", "qwerty", "admin", "welcome",
    "password123", "abc123", "letmein"
]

# Password history (optional)
old_passwords = ["MyOldPass@123", "Welcome@2025"]


def analyze_password(password):
    score = 0
    feedback = []

    # Length Check
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters.")

    # Uppercase Check
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")

    # Lowercase Check
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")

    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add numbers.")

    # Special Character Check
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Add special characters.")

    # Common Password Check
    if password.lower() in COMMON_PASSWORDS:
        feedback.append("This is a commonly used password.")
        return "Very Weak", feedback

    # Password Reuse Check
    if password in old_passwords:
        feedback.append("Password has been used before.")
        return "Weak", feedback

    # Strength Rating
    if score <= 2:
        strength = "Weak"
    elif score <= 5:
        strength = "Medium"
    else:
        strength = "Strong"

    return strength, feedback


def suggest_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))


password = input("Enter a password: ")

strength, feedback = analyze_password(password)

print("\nPassword Strength:", strength)

if feedback:
    print("\nSuggestions:")
    for item in feedback:
        print("-", item)

if strength != "Strong":
    print("\nSuggested Strong Password:")
    print(suggest_password())
