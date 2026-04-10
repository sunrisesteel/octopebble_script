import requests

# --- Configuration ---
API_KEY = "ENTER YOUR API KEY HERE"
ACCOUNT_NUMBER = "ENTER YOUR ACCOUNT NUMBER HERE"
API_URL = "https://api.octopus.energy/v1/graphql/"

def get_details():
    print(f"--- Local Config ---\nAPI Key: {API_KEY}\nAccount: {ACCOUNT_NUMBER}\n\n--- Fetching live details...")
    try:
        # Obtain Token
        q1 = "mutation krakenTokenAuthentication($apiKey: String!) { obtainKrakenToken(input: {APIKey: $apiKey}) { token } }"
        res = requests.post(API_URL, json={'query': q1, 'variables': {'apiKey': API_KEY}})
        res.raise_for_status()
        token = res.json()['data']['obtainKrakenToken']['token']

        # Fetch Devices
        q2 = "query Devices($accountNumber: String!) { devices(accountNumber: $accountNumber) { id name deviceType provider } }"
        res = requests.post(API_URL, headers={"Authorization": token}, json={'query': q2, 'variables': {'accountNumber': ACCOUNT_NUMBER}})
        res.raise_for_status()

        devices = res.json().get('data', {}).get('devices', [])
        print(f"\n--- Live Devices Found ({len(devices)}) ---")
        for i, d in enumerate(devices, 1):
            print(f"  {i}. {d.get('name')} ({d.get('deviceType')}) - ID: {d.get('id')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_details()
