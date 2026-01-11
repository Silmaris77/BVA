import requests

BASE_URL = "http://localhost:8001"
USERNAME = "admin"
PASSWORD = "admin123"

def test_login():
    print(f"Attempting login to {BASE_URL}/token with user={USERNAME}")
    try:
        response = requests.post(
            f"{BASE_URL}/token",
            data={"username": USERNAME, "password": PASSWORD}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    test_login()
