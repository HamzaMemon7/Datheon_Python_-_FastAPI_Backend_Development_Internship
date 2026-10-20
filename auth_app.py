import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt

SECRET_KEY = "my_super_secret_jwt_key_change_me_later"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(title="User Auth & RBAC API")

# Memory database
users_db = {}

# Schemas
class UserRegister(BaseModel):
    username: str
    password: str
    role: str = "user"  # "admin" ya "user"

class Token(BaseModel):
    access_token: str
    token_type: str

# Stable Password Hashing
def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_password_hash(plain_password) == hashed_password

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid hai ya expire ho chuka hai",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None:
            raise credentials_exception
        return {"username": username, "role": role}
    except JWTError:
        raise credentials_exception

# 1. Register Endpoint
@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserRegister):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Yeh username pehle se mojood hai")
    hashed_pwd = get_password_hash(user.password)
    users_db[user.username] = {"username": user.username, "password": hashed_pwd, "role": user.role}
    return {"message": "User kamyabi se register ho gaya!"}

# 2. Login Endpoint
@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ghalat username ya password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 3. Protected Route
@app.get("/users/me")
def read_current_user(current_user: dict = Depends(get_current_user)):
    return {"status": "Success", "user": current_user}

# 4. Admin Route
@app.get("/admin/dashboard")
def admin_only_data(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Aapke paas admin rights nahi hain!"
        )
    return {"message": "Welcome Admin! Yeh secret portal hai."}