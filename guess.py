import hashlib
import time
import os
import getpass
from datetime import datetime

# ANSI Terminal Colors for Cyberpunk UI
GREEN = "\033[1;32m"
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
RESET = "\033[0m"

# Configuration
# SHA-256 hash of "pass123"
STORED_HASH = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
MAX_ATTEMPTS = 5
LOG_FILE = "auth_security.log"

def log_event(status, attempt_num, details=""):
    """Simulates a syslog/SIEM event logger for Incident Response (IR) monitoring."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [AUTH_SERVICE] [STATUS:{status}] - Attempt: {attempt_num}/{MAX_ATTEMPTS} - {details}\n"
    try:
        with open(LOG_FILE, "a") as f:
            f.write(log_message)
    except Exception as e:
        print(RED + f"  [!] Log write failure: {e}" + RESET)

def show_banner():
    # Clear screen for terminal experience
    os.system('cls' if os.name == 'nt' else 'clear')
    print(CYAN + """
  ======================================================
   ________  ___  ___  ________  ________  _________    
  |\   ____\|\  \|\  \|\   __  \|\   ____\|\___   ___\  
  \ \  \___| \ \  \\\  \ \  \|\  \ \  \___|\|___ \  \_|  
   \ \  \  ___\ \  \\\  \ \   __  \ \  \        \ \  \   
    \ \  \|\  \ \  \\\  \ \  \ \  \ \  \____    \ \  \  
     \ \_______\ \_______\ \__\ \__\ \_______\   \ \__\ 
      \|_______|\|_______|\|__|\|__|\|_______|    \|__| 
                                                        
                    [ SECURE ACCESS SHELL ]
  ======================================================
  """ + RESET)
    print(YELLOW + "  [!] Notice: All authentication attempts are logged for SIEM analysis." + RESET)
    print()

def main():
    show_banner()
    attempts = 0
    
    while attempts < MAX_ATTEMPTS:
        try:
            print(f"  [Attempt {attempts + 1}/{MAX_ATTEMPTS}]")
            # getpass masks user input so typing is not exposed on the screen
            raw_input = getpass.getpass("  Enter Authentication Key: ")
        except KeyboardInterrupt:
            print(RED + "\n\n  [!] Authentication aborted by user." + RESET)
            log_event("ABORTED", attempts, "SIGINT received.")
            return
        
        # Calculate SHA-256 hash of the entered password
        input_hash = hashlib.sha256(raw_input.encode()).hexdigest()
        attempts += 1
        
        if input_hash == STORED_HASH:
            print(GREEN + "\n  [+] ACCESS GRANTED. Initializing secure session..." + RESET)
            log_event("SUCCESS", attempts, "User authenticated successfully.")
            return
        else:
            print(RED + "  [-] Access Denied: Incorrect Credential Key." + RESET)
            
            # Anti-Brute-Force Rate Limiting (Exponential Backoff: 1s, 2s, 4s, 8s...)
            delay = 2 ** (attempts - 1)
            print(YELLOW + f"  [i] Rate limiting active. Cooldown: {delay}s..." + RESET)
            time.sleep(delay)
            
            log_event("FAILED", attempts, "Incorrect password attempt.")
            print()
            
    # Lockout logic
    print(RED + "\n  [!!!] SECURITY LOCKOUT: MAXIMUM ATTEMPTS REACHED." + RESET)
    print(RED + "  Your terminal session has been locked. Administrator alerted." + RESET)
    log_event("LOCKOUT", attempts, "Maximum attempt limit breached. Target account locked out.")

if __name__ == "__main__":
    main()
