from v2.backend.database import SessionLocal, engine
from v2.backend import models
import bcrypt
import uuid

# Upewnij się, że tabele istnieją
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

username = "admin"
password = "admin"

# Sprawdź czy istnieje
existing = db.query(models.User).filter(models.User.username == username).first()

if existing:
    print(f"Użytkownik {username} już istnieje.")
    # Zaktualizuj hasło (dla pewności)
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    existing.password_hash = password_hash
    db.commit()
    print(f"Zaktualizowano hasło dla {username}.")
else:
    # Stwórz nowego
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    new_user = models.User(
        user_id=str(uuid.uuid4()),
        username=username,
        password_hash=password_hash,
        xp=1000,
        level=5,
        degencoins=500,
        degen_type="Admin",
        company="BrainVentureAcademy"
    )
    db.add(new_user)
    db.commit()
    print(f"Utworzono użytkownika {username}.")

db.close()
