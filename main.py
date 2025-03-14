from fastapi import FastAPI, Depends
from pydantic import BaseModel
from utils.jwt_utils import create_jwt , verify_jwt


# Initialize FastAPI
app = FastAPI()



# Request model for login
class LoginRequest(BaseModel):
    username: str


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
