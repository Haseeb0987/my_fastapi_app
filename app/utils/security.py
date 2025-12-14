import bcrypt

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    # Bcrypt has a 72-byte limit for passwords
    password = password[:72]
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    # Bcrypt has a 72-byte limit for passwords
    plain_password = plain_password[:72]
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


