import jwt
import secrets
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

# Initialize FastAPI
app = FastAPI()

# Securely generate a secret key (avoid hardcoding keys)
SECRET_KEY = secrets.token_hex(32)  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour

# Request model for login
class LoginRequest(BaseModel):
    username: str

# Function to generate JWT token
def create_jwt(username: str):
    expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "exp": expiration}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

# Function to verify JWT token
def verify_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]  # Return username if valid
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Root route - Server status
@app.get("/")
def server_status():
    return {
        "message": "Server is running",
        "status": "success",
        "data": {
            "app_name": "FastAPI JWT Auth",
            "version": "1.0.0",
            "description": "A simple FastAPI app with JWT authentication"
        }
    }

# Login route - Generate JWT token
@app.post("/login")
def login(user: LoginRequest):
    token = create_jwt(user.username)
    return {"access_token": token, "token_type": "bearer"}

# Secure route - Requires authentication
@app.get("/protected")
def protected_route(username: str = Depends(verify_jwt)):
    return {"message": f"Hello {username}, here is your secure data!"}
