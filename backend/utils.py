import uuid
from werkzeug.security import generate_password_hash, check_password_hash

def create_token():
    return uuid.uuid4().hex

def hash_password(password: str) -> str:
    return generate_password_hash(password)

def verify_password(hashpw: str, password: str) -> bool:
    return check_password_hash(hashpw, password)
