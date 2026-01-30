import requests
import json

BASE_URL = "http://localhost:8001"
USER = "admin"
PASS = "admin123"

def test_persistence():
    # 1. Login
    print("Logging in...")
    resp = requests.post(f"{BASE_URL}/token", data={"username": USER, "password": PASS})
    if resp.status_code != 200:
        print(f"Login failed: {resp.text}")
        return
    token = resp.json()['access_token']
    print("Logged in.")

    # 2. Get recommendation (Simulate Step 4)
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "app_id": "hydraulik", # Zgaduje ID, powinno byc w bazie recommender
        "answers": {
            "q1": "option_a",
            "q2": "option_b"
        }
    }
    
    print("Requesting recommendation...")
    url = f"{BASE_URL}/tools/milwaukee/recommendation"
    resp = requests.post(url, json=payload, headers=headers)
    
    if resp.status_code == 200:
        print("Recommendation success.")
        print(f"Keys: {list(resp.json().keys())}")
    else:
        print(f"Recommendation failed: {resp.text}")
        
    # 3. Verify Activity Log
    print("Checking activity log...")
    resp = requests.get(f"{BASE_URL}/users/{USER}/activities", headers=headers)
    activities = resp.json()
    
    found = False
    for act in activities:
        if act['activity_type'] == 'tool_used' and 'milwaukee' in act['description']:
            print(f"Found activity: {act['description']} (+{act['xp_awarded']} XP)")
            found = True
            break
            
    if found:
        print("Persistence verified!")
    else:
        print("Activity not found in logs.")

if __name__ == "__main__":
    test_persistence()
