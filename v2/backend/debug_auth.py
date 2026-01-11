from database import SessionLocal
import models
import bcrypt

# Skopiowane z main.py aby mieć pewność 1:1 (chyba że zrobię import main, ale to uruchomi app)
def verify_password(plain_password, hashed_password):
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        print(f"Błąd verify_password: {e}")
        return False

def debug_login():
    db = SessionLocal()
    username = "admin"
    password = "admin"
    
    print(f"Szukam użytkownika: {username}")
    user = db.query(models.User).filter(models.User.username == username).first()
    
    if not user:
        print("Użytkownik NIE ZNALEZIONY w bazie!")
    else:
        print(f"Użytkownik znaleziony. ID: {user.id}")
        print(f"Hash z bazy: {user.password_hash}")
        
        # Test 1: Verify Password
        is_valid = verify_password(password, user.password_hash)
        print(f"Weryfikacja bcrypt (verify_password): {is_valid}")
        
        # Test 2: Plain text match
        is_plain_match = (user.password_hash == password)
        print(f"Weryfikacja plain text: {is_plain_match}")

    db.close()

if __name__ == "__main__":
    debug_login()
