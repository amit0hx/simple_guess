# Secure Guessing Shell - Defensive Python Implementation

A Python terminal-based authentication shell designed to demonstrate core security vulnerabilities in traditional login scripts and implement robust defense countermeasures (rate limiting, credential masking, hashing, and audit logs).

---

## 🛡️ Security Vulnerabilities & Defensive Mitigations

This project demonstrates the transition from insecure coding practices to a secure authentication flow:

### 1. Weak Credential Storage (Hardcoded Secrets)
- **Vulnerability:** Storing credentials in plain text (`our_password = "pass123"`) inside source code allows anyone with source access or memory-dumping capabilities to retrieve the password.
- **Defensive Fix:** Implemented **SHA-256 password hashing**. The source code only stores the hash (`5e884898da2...`). During login, the user's input is hashed and compared to this stored hash.

### 2. Shoulder Surfing (Plaintext Input)
- **Vulnerability:** Standard `input()` displays the password characters on the screen as the user types, making them vulnerable to shoulder-surfing attacks.
- **Defensive Fix:** Swapped `input()` with the python standard **`getpass`** module, which masks input character typing, preventing visual credential leakage.

### 3. Automated Brute-Force Attacks
- **Vulnerability:** A simple loop with a flat try counter can easily be bypassed or automated with password spray tools running at high speed.
- **Defensive Fix:** Implemented **Exponential Backoff Rate Limiting**. The cooldown duration doubles after each wrong attempt ($2^{attempts - 1}$ seconds: e.g., 1s, 2s, 4s, 8s...), stopping automated brute-force scripts while keeping the experience normal for genuine users.

### 4. Lack of Audit Trail (Incident Response)
- **Vulnerability:** If an attacker attempts to guess a password, there are no logs to alert administrators or provide forensic evidence.
- **Defensive Fix:** Implemented a **Structured Logging Engine** that writes all authentication events (Success, Failure, Interruption, and Lockouts) with precise timestamps, attempt indices, and alert triggers to `auth_security.log`. These logs are formatted to be ingested by SIEM (Security Information and Event Management) tools for anomaly detection.

---

## 💻 Running the Script

Ensure you have Python 3 installed. Run the script directly from your terminal:

```bash
python guess.py
```

### Log Inspection (For Incident Response Analysis)
All authentication attempts are appended to `auth_security.log` in the local directory:
```text
[2026-05-24 15:10:02] [AUTH_SERVICE] [STATUS:FAILED] - Attempt: 1/5 - Incorrect password attempt.
[2026-05-24 15:10:15] [AUTH_SERVICE] [STATUS:SUCCESS] - Attempt: 2/5 - User authenticated successfully.
```

---

## 📄 License
This project is licensed under the MIT License.
