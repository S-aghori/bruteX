# wordlist_gen.py — Smart wordlist generator for BruteX

def generate_wordlist(username, extra_words=None):
    """
    Generate a smart password list based on username.
    Returns a list of passwords to try.
    """
    base = [
        # Most common passwords
        "password", "123456", "password123", "admin",
        "root", "toor", "12345", "qwerty", "abc123",
        "letmein", "monkey", "1234567890", "iloveyou",
        "sunshine", "princess", "welcome", "shadow",
        "superman", "dragon", "master", "666666",
        "123123", "000000", "pass", "test", "guest",

        # Username based
        username,
        username + "123",
        username + "1234",
        username + "@123",
        username + "2024",
        username + "2025",
        username + "2026",
        username + "!",
        username + "#",
        "123" + username,

        # Service specific
        "admin123", "root123", "administrator",
        "ftp", "ftpuser", "ftpadmin",
        "ssh", "sshuser", "login",
        "service", "backup", "temp",
    ]

    if extra_words:
        base.extend(extra_words)

    # Remove duplicates while keeping order
    seen = set()
    unique = []
    for p in base:
        if p not in seen:
            seen.add(p)
            unique.append(p)

    return unique


def load_wordlist(filepath):
    """
    Load passwords from a wordlist file.
    Returns list of passwords.
    """
    try:
        with open(filepath, "r", encoding="utf-8",
                  errors="ignore") as f:
            passwords = [line.strip() for line in f
                        if line.strip()]
        print(f"[*] Loaded {len(passwords)} passwords from {filepath}")
        return passwords
    except FileNotFoundError:
        print(f"[!] Wordlist file not found: {filepath}")
        print(f"[*] Using built-in wordlist instead")
        return generate_wordlist("admin")


def get_wordlist(filepath=None, username="admin"):
    """
    Main function — returns wordlist from file or generates one.
    """
    if filepath:
        return load_wordlist(filepath)
    else:
        words = generate_wordlist(username)
        print(f"[*] Generated {len(words)} passwords for user: {username}")
        return words