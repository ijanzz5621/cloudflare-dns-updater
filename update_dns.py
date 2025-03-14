import requests
import json
import os
import time

# for local test only
from dotenv import load_dotenv
load_dotenv()

# Cloudflare API details
API_TOKEN = os.getenv("API_TOKEN")
ZONE_ID = os.getenv("ZONE_ID")
RECORD_NAME = os.getenv("RECORD_NAME")
RECORD_NAMES = str(RECORD_NAME).split(",")

# Configurable interval (default 5 minutes)
UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", 300))  # Seconds

CLOUDFLARE_API_URL = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"

# Get the current public IP
def get_public_ip():
    response = requests.get("https://api.ipify.org?format=json")
    return response.json()["ip"]

# Get DNS record details
def get_dns_record(record_name):
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    params = {"type": "A", "name": record_name}
    response = requests.get(CLOUDFLARE_API_URL, headers=headers, params=params)
    data = response.json()
    print(data)
    
    if data["success"] and data["result"]:
        return data["result"][0]  # Return the first matching record
    return None

# Update DNS record
def update_dns(record_name):
    public_ip = get_public_ip()
    record = get_dns_record(record_name)

    if not record:
        print("DNS record not found!")
        return

    if record["content"] == public_ip:
        print("IP address is unchanged. No update needed.")
        return

    record_id = record["id"]
    update_url = f"{CLOUDFLARE_API_URL}/{record_id}"
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    data = {"type": "A", "name": record_name, "content": public_ip, "ttl": 300}

    response = requests.put(update_url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Updated {record_name} to {public_ip}")
    else:
        print("Failed to update DNS record:", response.json())

if __name__ == "__main__":
    while True:
        for record_name in RECORD_NAMES:
            update_dns(record_name)
        print(f"Sleeping for {UPDATE_INTERVAL} seconds...\n")
        time.sleep(UPDATE_INTERVAL)
