
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def get_hashed_password(plain_password: str):
    return password_hash.hash(plain_password)

def verify_hashed_password(plain_password: str, hashed_password) -> bool:
    return password_hash.verify(plain_password, hashed_password)