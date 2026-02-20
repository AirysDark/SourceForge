from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

SECRET_KEY = "dev-secret-change"
ALGO = "HS256"
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pw(p): return pwd.hash(p)
def verify_pw(p,h): return pwd.verify(p,h)

def create_access(username):
    return jwt.encode({"sub": username, "exp": datetime.utcnow()+timedelta(minutes=30)}, SECRET_KEY, algorithm=ALGO)

def decode_access(t):
    try: return jwt.decode(t, SECRET_KEY, algorithms=[ALGO])
    except JWTError: return None
