import requests
import json
import os
import time

# Cloudflare API details
API_TOKEN = os.getenv("API_TOKEN")
ZONE_ID = os.getenv("ZONE_ID")
RECORD_NAME = os.getenv("RECORD_NAME")

# Configurable interval (default 5 minutes)
UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", 300))  # Seconds

CLOUDFLARE_API_URL = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"

# Get the current public IP
def get_public_ip():
    response = requests.get("https://api.ipify.org?format=json")
    return response.json()["ip"]

# Get DNS record details
def get_dns_record():
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    params = {"type": "A", "name": RECORD_NAME}
    response = requests.get(CLOUDFLARE_API_URL, headers=headers, params=params)
    data = response.json()
    print(data)
    
    if data["success"] and data["result"]:
        return data["result"][0]  # Return the first matching record
    return None

# Update DNS record
def update_dns():
    public_ip = get_public_ip()
    record = get_dns_record()

    if not record:
        print("DNS record not found!")
        return

    if record["content"] == public_ip:
        print("IP address is unchanged. No update needed.")
        return

    record_id = record["id"]
    update_url = f"{CLOUDFLARE_API_URL}/{record_id}"
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    data = {"type": "A", "name": RECORD_NAME, "content": public_ip, "ttl": 300}

    response = requests.put(update_url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Updated {RECORD_NAME} to {public_ip}")
    else:
        print("Failed to update DNS record:", response.json())

if __name__ == "__main__":
    while True:
        update_dns()
        print(f"Sleeping for {UPDATE_INTERVAL} seconds...\n")
        time.sleep(UPDATE_INTERVAL)
