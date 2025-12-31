from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
import bcrypt

# 1. Config
SECRET_KEY = "my_super_secret_key" # Change this in real production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# 2. Setup Password Hashing
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    # Check if passwords match (bcrypt.checkpw expects bytes)
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        print(f"Auth Error: {e}")
        return False

def get_password_hash(password):
    # Hash a password (bcrypt.hashpw expects bytes)
    # Generate a salt and hash
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8') # Return as string for DB storage

# 3. Function to Create Token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
