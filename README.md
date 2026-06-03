# ⚔️ BruteX v1.0 — SSH | FTP | HTTP Brute Force Tool

> Built as part of OSCP preparation. A professional credential brute forcing toolkit for SSH, FTP, and HTTP login pages — written in Python from scratch.

![Python](https://img.shields.io/badge/Python-3.x-red?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-557C94?style=flat-square&logo=kali-linux)
![Purpose](https://img.shields.io/badge/Purpose-OSCP%20Prep-orange?style=flat-square)
![Services](https://img.shields.io/badge/Services-SSH%20%7C%20FTP%20%7C%20HTTP-red?style=flat-square)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square)

---

## ⚠️ Disclaimer
> This tool is for **authorized penetration testing and educational purposes only.**
> Only use against systems you own or have explicit written permission to test.
> All testing shown was performed in a controlled VirtualBox lab on Metasploitable2.

---

## 🎯 What This Tool Does

BruteX automates credential brute forcing across 3 services in one command:

```
SSH Brute Force → FTP Brute Force → HTTP Login Brute Force → JSON Report
```

---

## 📸 Screenshots

### 1. Full BruteX Running — All 3 Phases
<img width="665" height="333" alt="Full brutex py running" src="https://github.com/user-attachments/assets/ff0b867a-0748-4933-8473-663c2f7e2be3" />


### 2. SSH Cracked
![SSH Cracked](screenshots/SSH_cracked.png)

### 3. Final Summary — 3 Services Cracked
![Final Summary](screenshots/Final_summary.png)

### 4. Cracked Credentials File
![Credentials](screenshots/Credentials_file.png)

### 5. JSON Report Output
![Report](screenshots/Report_JSON.png)

---

## 🛠️ Project Structure

```
brutex/
  ├── brutex.py        ← Main CLI entry point
  ├── ssh_brute.py     ← SSH brute force module
  ├── ftp_brute.py     ← FTP brute force module
  ├── http_brute.py    ← HTTP login brute force
  ├── wordlist_gen.py  ← Smart wordlist generator
  └── logger.py        ← Attack logging module
```

---

## ⚙️ Requirements

```bash
pip install paramiko
```

Only one external library needed. Everything else uses Python standard library.

---

## 🚀 Usage

### Attack all services at once
```bash
python brutex.py -t 192.168.56.200 -s all -u msfadmin
```

### SSH only
```bash
python brutex.py -t 192.168.56.200 -s ssh -u msfadmin
```

### FTP only
```bash
python brutex.py -t 192.168.56.200 -s ftp -u msfadmin
```

### HTTP only
```bash
python brutex.py -t 192.168.56.200 -s http -u admin
```

### With custom wordlist (rockyou.txt)
```bash
python brutex.py -t 192.168.56.200 -s all -u msfadmin -w /usr/share/wordlists/rockyou.txt
```

### Run individual modules
```bash
python ssh_brute.py  192.168.56.200 22 msfadmin
python ftp_brute.py  192.168.56.200 21 msfadmin
python http_brute.py 192.168.56.200 80 admin
```

---

## 📊 Sample Output

```
╔══════════════════════════════════════════╗
║          BRUTEX  v1.0                    ║
║     SSH | FTP | HTTP Brute Forcer        ║
║   [!] For authorized testing only        ║
╚══════════════════════════════════════════╝

[INFO] PHASE 1 — SSH BRUTE FORCE
[FAIL] Trying msfadmin:password → FAILED
[FAIL] Trying msfadmin:123456 → FAILED
[SUCCESS] Trying msfadmin:msfadmin → SUCCESS!
[SUCCESS] CRACKED! SSH://msfadmin:msfadmin@192.168.56.200:22

[INFO] PHASE 2 — FTP BRUTE FORCE
[SUCCESS] Trying msfadmin:msfadmin → SUCCESS!
[SUCCESS] CRACKED! FTP://msfadmin:msfadmin@192.168.56.200:21

[INFO] PHASE 3 — HTTP BRUTE FORCE
[SUCCESS] Trying msfadmin:abc123 → SUCCESS!
[SUCCESS] CRACKED! HTTP://msfadmin:abc123@192.168.56.200:80

[INFO] SCAN COMPLETE
[INFO] Target:   192.168.56.200
[INFO] Cracked:  3 service(s)
[SUCCESS] ✓ SSH  → msfadmin:msfadmin
[SUCCESS] ✓ FTP  → msfadmin:msfadmin
[SUCCESS] ✓ HTTP → msfadmin:abc123
[INFO] Report saved → brutex_report.json
```

---

## ⚔️ Lab Results — Metasploitable2

Tested against Metasploitable2 in a controlled VirtualBox lab:

| Service | Port | Username | Password | Result |
|---|---|---|---|---|
| SSH | 22 | msfadmin | msfadmin | ✅ Cracked |
| FTP | 21 | msfadmin | msfadmin | ✅ Cracked |
| HTTP | 80 | msfadmin | abc123 | ✅ Cracked |

---

## 🧠 Concepts Learned

| Concept | Where Used |
|---|---|
| Paramiko SSH library | ssh_brute.py |
| ftplib FTP library | ftp_brute.py |
| urllib HTTP requests | http_brute.py |
| Threading + Queue | All modules |
| Rate limiting (delay) | ssh_brute.py |
| Credential logging | logger.py |
| Smart wordlist gen | wordlist_gen.py |
| JSON report output | brutex.py |

---

## 🛡️ Defense Awareness

Building this tool teaches you how to **defend** against brute force:

```
✓ Use fail2ban — auto-ban IPs after X failed attempts
✓ Use SSH keys instead of passwords
✓ Rate limit login endpoints
✓ Enable MFA on all services
✓ Use strong unique passwords
✓ Monitor auth logs: /var/log/auth.log
```

---

## 🗺️ OSCP Methodology Map

```
Phase 1 → NetScanner     Recon + Port Scan    (Project 2)
Phase 2 → BruteX         Credential Attack    (This project)
Phase 3 → Post Exploit   Shell + Loot
Phase 4 → Report         Professional output
```

---

## 🔮 Planned Upgrades

- [ ] SMTP brute force module
- [ ] RDP brute force module
- [ ] Auto-detect login fail string for HTTP
- [ ] CAPTCHA detection
- [ ] Proxy support for anonymity
- [ ] HTML report generator

---

## 📁 Related Projects

- 🔗 Project 2 — NetScanner: [github.com/S-aghori/netscanner](https://github.com/S-aghori/netscanner)
- 🔗 Medium write-up: Coming soon
- 🔗 LinkedIn: S-aghori

---

## 👤 Author

**S-aghori** — Cybersecurity student preparing for OSCP
Building projects in public to document the journey.

---

*Built on Kali Linux | Tested on Metasploitable2 | For educational use only*
