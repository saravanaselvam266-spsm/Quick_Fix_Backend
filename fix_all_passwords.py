from db.database import SessionLocal
from models.user_model import User
from core.security import get_password_hash

# 1. Connect to Database
db = SessionLocal()

print("Checking all users for invalid passwords...")

# 2. Get All Users
users = db.query(User).all()
print(f"Found {len(users)} users in the database.")

fixed_count = 0

for user in users:
    current_pwd = user.password_hash
    
    # Check if existing password is NOT a valid hash (Bcrypt hashes start with $2)
    # If it is plain text (like "password"), it won't start with $2
    if not current_pwd.startswith("$2"):
        print(f"--> Fixing password for user: {user.email} (ID: {user.user_id})")
        
        # We assume the current value IS the plain text password.
        # So we hash it and save it back.
        new_hashed_password = get_password_hash(current_pwd)
        user.password_hash = new_hashed_password
        
        fixed_count += 1
    else:
        print(f"User {user.email} is already secure.")

# 3. Save Changes
if fixed_count > 0:
    db.commit()
    print("------------------------------------------------")
    print(f"SUCCESS: Fixed {fixed_count} users! Your login should work now.")
else:
    print("------------------------------------------------")
    print("All users already have secure passwords. No changes needed.")

db.close()
