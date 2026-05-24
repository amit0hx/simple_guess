<div align="center">

# Secure Guessing Shell

**A defensive authentication shell demonstrating common credential vulnerabilities and their mitigations — built in Python.**

[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

</div>

---

## Overview

Secure Guessing Shell is a terminal-based authentication simulator that demonstrates how traditional login scripts fail under attack — and how to fix them. It walks through four real-world vulnerabilities and implements industry-standard countermeasures in a single, readable Python script.

Built as a learning tool for security students, CTF players, and anyone studying defensive programming and incident response.

---

## Vulnerability → Defense Matrix

| # | Vulnerability | Risk | Defense Implemented |
|---|---------------|------|---------------------|
| 1 | **Hardcoded plaintext credentials** | Source code leak → full compromise | SHA-256 password hashing (only hash stored) |
| 2 | **Visible password input** | Shoulder surfing / screen recording | `getpass` module — masks terminal input |
| 3 | **No brute-force protection** | Automated password spray at high speed | Exponential backoff rate limiting (1s, 2s, 4s, 8s…) |
| 4 | **No audit trail** | Zero forensic evidence after an attack | Structured logging to `auth_security.log` (SIEM-ready) |

---

## How It Works

```
User launches script
        │
        ▼
┌─────────────────────┐
│  Masked input via   │
│  getpass module      │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  SHA-256 hash of    │──── Match? ──→ ACCESS GRANTED + log SUCCESS
│  input vs stored    │
└────────┬────────────┘
         │ No match
         ▼
┌─────────────────────┐
│  Log FAILED attempt │
│  Apply exponential  │
│  backoff delay      │
└────────┬────────────┘
         │
         ▼
   Attempts ≥ 5?
    Yes → LOCKOUT + log alert
    No  → Retry
```

---

## Getting Started

### Prerequisites

- Python 3.6 or later (no external dependencies)

### Installation

```bash
git clone https://github.com/amit0hx/simple_guess.git
cd simple_guess
```

### Run

```bash
python guess.py
```

---

## Log Output

All authentication events are appended to `auth_security.log` in SIEM-ingestible format:

```
[2026-05-24 15:10:02] [AUTH_SERVICE] [STATUS:FAILED]  - Attempt: 1/5 - Incorrect password attempt.
[2026-05-24 15:10:15] [AUTH_SERVICE] [STATUS:SUCCESS] - Attempt: 2/5 - User authenticated successfully.
[2026-05-24 15:12:40] [AUTH_SERVICE] [STATUS:LOCKOUT] - Attempt: 5/5 - Maximum attempt limit breached.
```

| Event | Trigger |
|-------|---------|
| `SUCCESS` | Correct credential entered |
| `FAILED` | Wrong password attempt |
| `ABORTED` | User pressed `Ctrl+C` |
| `LOCKOUT` | 5 consecutive failures — session locked |

---

## Configuration

Defaults are set in `guess.py` and can be modified:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `STORED_HASH` | SHA-256 of `pass123` | Target credential hash |
| `MAX_ATTEMPTS` | `5` | Lockout threshold |
| `LOG_FILE` | `auth_security.log` | Audit log file path |

---

## Project Structure

```
simple_guess/
├── guess.py      # Authentication shell with all defensive controls
├── made.txt      # Project credits and notes
└── README.md
```

---

## Disclaimer

This project is for **educational and demonstration purposes only**. It illustrates common authentication weaknesses and their defenses. Do not use hardcoded hashes in production systems — use proper key derivation functions (bcrypt, Argon2) and secure credential storage.

---

## License

Distributed under the [MIT License](LICENSE).

---

<div align="center">
  <sub>Built by <a href="https://github.com/amit0hx">@amit0hx</a></sub>
</div>
