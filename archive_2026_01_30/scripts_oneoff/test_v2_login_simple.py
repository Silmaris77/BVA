"""Prosty test logowania v2 - weryfikacja hasła admin/admin123"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from v2.backend.database import SessionLocal
from v2.backend import models
import bcrypt

def test_password_verification():
    db = SessionLocal()
    
    # Pobierz użytkownika admin
    user = db.query(models.User).filter(models.User.username == "admin").first()
    
    if not user:
        print("❌ Użytkownik 'admin' nie istnieje!")
        return
    
    print(f"✓ Użytkownik znaleziony: {user.username}")
    print(f"  ID: {user.id}")
    print(f"  User ID: {user.user_id}")
    print(f"  XP: {user.xp}")
    print(f"  Level: {user.level}")
    print(f"  Password hash: {user.password_hash[:50]}...")
    
    # Test weryfikacji hasła
    test_password = "admin123"
    
    try:
        is_valid = bcrypt.checkpw(test_password.encode('utf-8'), user.password_hash.encode('utf-8'))
        if is_valid:
            print(f"\n✅ HASŁO PRAWIDŁOWE: '{test_password}' pasuje do użytkownika '{user.username}'")
        else:
            print(f"\n❌ HASŁO BŁĘDNE: '{test_password}' NIE pasuje do użytkownika '{user.username}'")
    except Exception as e:
        print(f"\n⚠️ Błąd weryfikacji bcrypt: {e}")
        # Sprawdź plain text (fallback)
        if user.password_hash == test_password:
            print(f"  Ale hasło pasuje jako plain text (wymaga re-hash)")
    
    db.close()

if __name__ == "__main__":
    print("="*60)
    print("TEST WERYFIKACJI HASŁA - BVA v2")
    print("="*60)
    test_password_verification()
    print("="*60)
