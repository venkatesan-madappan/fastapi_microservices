from fastapi.security import HTTPBasicCredentials, HTTPBasic
from signup_repository import Login
from secrets import compare_digest
from passlib.context import CryptContext

http_basic = HTTPBasic()

crypt_context = CryptContext(schemes=["sha256_crypt", "md5_crypt"])

def get_password_hash(password):
    return crypt_context.hash(password)

def verify_password(plain_password, hashed_password):
    return crypt_context.verify(plain_password, hashed_password)

def authenticate(credentials: HTTPBasicCredentials, account:Login):
    try:
        is_username = compare_digest(credentials.username, account.username)
        is_password = compare_digest(credentials.password, account.password)
        # verfied_password = verify_password(credentials.password, account.passphrase)
        return True
    except Exception as e:
        print(e)
        return False