"""
Test logowania do v2 backend
"""
import requests
import json

BASE_URL = "http://localhost:8001"

def test_login(username, password):
    print(f"\n{'='*60}")
    print(f"TEST LOGOWANIA: {username}")
    print(f"{'='*60}")
    
    # Endpoint /token wymaga OAuth2PasswordRequestForm (form data, nie JSON)
    data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/token", data=data)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ SUKCES!")
            print(f"Token: {result.get('access_token', 'brak')}")
            print(f"Token type: {result.get('token_type', 'brak')}")
            
            # Test /users/me
            token = result.get('access_token')
            headers = {"Authorization": f"Bearer {token}"}
            me_response = requests.get(f"{BASE_URL}/users/me", headers=headers)
            
            if me_response.status_code == 200:
                user_data = me_response.json()
                print(f"\nDane użytkownika:")
                print(f"  Username: {user_data.get('username')}")
                print(f"  XP: {user_data.get('xp')}")
                print(f"  Level: {user_data.get('level')}")
                print(f"  Company: {user_data.get('company')}")
            
            return True
        else:
            print(f"✗ BŁĄD!")
            try:
                error_detail = response.json()
                print(f"Szczegóły: {error_detail}")
            except:
                print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ BŁĄD: Nie można połączyć się z serwerem!")
        print("Upewnij się, że backend działa na http://localhost:8000")
        return False
    except Exception as e:
        print(f"✗ BŁĄD: {e}")
        return False

if __name__ == "__main__":
    # Test 1: Poprawne dane
    test_login("admin", "admin123")
    
    # Test 2: Niepoprawne hasło
    test_login("admin", "wrongpassword")
