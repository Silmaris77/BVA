import sys
import os
# Add root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from v2.backend.database import SessionLocal
from v2.backend import models, auth

def create_admin():
    print("Connecting to database...")
    db = SessionLocal()
    try:
        # Check if admin exists
        user = db.query(models.User).filter(models.User.username == "admin").first()
        if user:
            print("Admin user already exists. Updating password to 'admin123'...")
            user.hashed_password = auth.get_password_hash("admin123")
            db.commit()
            print("Password updated successfully.")
        else:
            print("Creating new admin user...")
            hashed_password = auth.get_password_hash("admin123")
            admin_user = models.User(
                username="admin",
                email="admin@bva.pl",
                full_name="Administrator",
                hashed_password=hashed_password,
                is_active=True,
                role="admin",
                xp=0,
                level=1,
                streak_days=0
            )
            db.add(admin_user)
            db.commit()
            print("Admin user created successfully!")
            
        # Verify
        check = db.query(models.User).filter(models.User.username == "admin").first()
        if check:
            print(f"VERIFICATION: User '{check.username}' exists in DB with ID {check.id}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
