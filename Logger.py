# logger.py — Attack logging module for BruteX

import os
from datetime import datetime

LOG_FILE = "brutex_log.txt"

def log(message, level="INFO"):
    """
    Write a log entry to file and print to terminal.
    Levels: INFO, SUCCESS, FAIL, ERROR
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [{level}] {message}"

    # Print to terminal with colors
    colors = {
        "INFO":    "\033[94m",   # blue
        "SUCCESS": "\033[92m",   # green
        "FAIL":    "\033[91m",   # red
        "ERROR":   "\033[93m",   # yellow
    }
    reset = "\033[0m"
    color = colors.get(level, "")
    print(f"{color}{entry}{reset}")

    # Write to log file
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")

def log_success(host, port, service, username, password):
    """Log a successful credential find."""
    msg = f"CRACKED! {service}://{username}:{password}@{host}:{port}"
    log(msg, "SUCCESS")

    # Also save to credentials file
    with open("cracked_credentials.txt", "a") as f:
        f.write(f"{service}:{host}:{port}:{username}:{password}\n")

def clear_logs():
    """Clear old log files before new scan."""
    for f in [LOG_FILE, "cracked_credentials.txt"]:
        if os.path.exists(f):
            os.remove(f)