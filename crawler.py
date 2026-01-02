import requests
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime
import os
import re

# ---------------- TOR PROXY ----------------
proxies = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Educational Project)"
}

# ---------------- KEYWORDS ----------------
KEYWORDS = [
    "bitcoin", "market", "shop", "buy", "sell",
    "forum", "login", "account", "search"
]

# ---------------- UTILITIES ----------------
def clean_text(text):
    if not text:
        return ""
    return " ".join(text.split())

def detect_keywords(text):
    found = []
    text = text.lower()
    for k in KEYWORDS:
        if k in text:
            found.append(k)
    return ", ".join(found) if found else "None"

def detect_site_type(text):
    text = text.lower()
    if any(k in text for k in ["search", "engine"]):
        return "Search Engine"
    elif any(k in text for k in ["forum", "discussion", "thread"]):
        return "Forum"
    elif any(k in text for k in ["market", "shop", "buy", "sell"]):
        return "Marketplace"
    else:
        return "Unknown"

def detect_risk(site_type):
    if site_type == "Marketplace":
        return "High"
    elif site_type == "Forum":
        return "Medium"
    else:
        return "Low"

# ---------------- CRAWLER ----------------
def crawl_onion(url, retries=3, timeout=60):
    for attempt in range(retries):
        try:
            response = requests.get(
                url,
                proxies=proxies,
                headers=headers,
                timeout=timeout
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.title.text.strip() if soup.title else "No Title"
            full_text = soup.get_text(separator=" ", strip=True)
            preview = full_text[:200]

            return title, preview, full_text

        except Exception as e:
            print(f"[-] Retry {attempt+1} failed: {e}")
            time.sleep(5)

    return None, None, None

# ---------------- SAVE RESULT ----------------
def save_result(site, title, preview, full_content, writer):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    site_type = detect_site_type(title + " " + preview)
    keywords = detect_keywords(full_content)
    risk = detect_risk(site_type)
    status = "Success" if title else "Failed"

    # Save full page
    if full_content:
        os.makedirs("full_pages", exist_ok=True)
        safe_name = re.sub(r"[^a-zA-Z0-9_.-]", "_", site)
        filepath = os.path.join("full_pages", safe_name + ".txt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"URL: {site}\nTitle: {title}\n\n{full_content}")

    # Terminal output
    print("\n==============================")
    print(f"URL      : {site}")
    print(f"Title    : {title}")
    print(f"Type     : {site_type}")
    print(f"Keywords : {keywords}")
    print(f"Risk     : {risk}")
    print(f"Status   : {status}")
    print("==============================\n")

    # Write TSV
    writer.writerow([
        timestamp,
        site,
        clean_text(title),
        clean_text(preview),
        site_type,
        keywords,
        risk,
        status
    ])

# ---------------- MAIN ----------------
def main():
    print("\nONION WEB CRAWLER")
    print("1. Crawl URLs from file")
    print("2. Crawl a single URL\n")

    choice = input("Select option (1 or 2): ").strip()

    with open("output.tsv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter="\t")
        writer.writerow([
            "Crawl Timestamp",
            "URL",
            "Title",
            "Content Preview",
            "Site Type",
            "Detected Keywords",
            "Risk Level",
            "Status"
        ])

        if choice == "1":
            with open("onionsites.txt", "r") as f:
                sites = [line.strip() for line in f if line.strip()]

            for site in sites:
                title, preview, full = crawl_onion(site)
                save_result(site, title, preview, full, writer)
                time.sleep(5)

        elif choice == "2":
            site = input("Paste Onion URL: ").strip()
            title, preview, full = crawl_onion(site)
            save_result(site, title, preview, full, writer)

        else:
            print("Invalid option.")

    print("\n✔ Crawling completed. Results saved to output.tsv")

if __name__ == "__main__":
    main()
