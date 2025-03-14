# FastAPI JWT Authentication Example

This project is a simple FastAPI app that uses JWT (JSON Web Token) authentication. It allows users to log in with a username and get a secure token. This token is then used to access protected routes.

---

## How This Works

### 1. **First, We Import Some Tools** 🛠️

```python
import jwt
import secrets
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
```

- `jwt`: Helps us create and verify secure tokens.
- `secrets`: Used to generate a secret key (like a super strong password).
- `datetime` & `timedelta`: Helps us set an expiration time for tokens.
- `FastAPI`: The tool we use to build our web app.
- `HTTPException`: Used to handle errors (like when a token is wrong).
- `Depends`: Helps us protect routes that need a valid token.
- `BaseModel`: Helps us define how user data should look.

---

### 2. **We Create Our App** 🚀
```python
app = FastAPI()
```
- This starts our FastAPI web application.

---

### 3. **We Make a Secret Key & Set Some Rules** 🔑
```python
SECRET_KEY = secrets.token_hex(32)  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour
```
- `SECRET_KEY`: A secret key that makes our tokens secure.
- `ALGORITHM`: The method we use to lock our tokens.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: How long the token stays valid (1 hour).

---

### 4. **We Define What Login Data Looks Like** 👤
```python
class LoginRequest(BaseModel):
    username: str
```
- This makes sure that when someone logs in, they send a `username`.

---

### 5. **We Create a Function to Make a Token** 🔐
```python
def create_jwt(username: str):
    expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "exp": expiration}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token
```
- `expiration`: Sets the time when the token will expire.
- `payload`: Stores the username and expiration time inside the token.
- `jwt.encode(...)`: Creates a secure token.

---

### 6. **We Make a Function to Check Tokens** 🔍
```python
def verify_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]  # Return username if valid
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```
- `jwt.decode(...)`: Tries to unlock the token and read the username.
- If the token is **expired**, it gives an error.
- If the token is **wrong**, it gives an error.

---

### 7. **We Make a Route to Check if the Server is Running** ✅
```python
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
```
- If you open the app in a browser, you will see a message that the server is running.

---

### 8. **We Create a Login Route** 🔓
```python
@app.post("/login")
def login(user: LoginRequest):
    token = create_jwt(user.username)
    return {"access_token": token, "token_type": "bearer"}
```
- When a user logs in, we create a token and send it back.
- The token is like a **magic key** to open locked doors (protected routes).

---

### 9. **We Make a Protected Route** 🔒
```python
@app.get("/protected")
def protected_route(username: str = Depends(verify_jwt)):
    return {"message": f"Hello {username}, here is your secure data!"}
```
- This route **only** works if the user has a valid token.
- If the token is wrong or expired, the user is **blocked**!

---

## How to Run This Project 🏃

1. **Install FastAPI and Uvicorn** (only needed once):
   ```sh
   pip install fastapi uvicorn pyjwt
   ```
2. **Run the app**:
   ```sh
   uvicorn main:app --reload
   ```
3. **Test the API**:
   - Open a browser and go to: `http://127.0.0.1:8000/`
   - Use **Postman** or **cURL** to test login and protected routes.

---

## Example Requests 📡

### 1. **Login to Get a Token** 🪪
```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/login' \
  -H 'Content-Type: application/json' \
  -d '{"username": "Ali"}'
```
- Response:
```json
{
  "access_token": "your_generated_token_here",
  "token_type": "bearer"
}
```

### 2. **Access Protected Route with Token** 🔑
```sh
curl -X 'GET' \
  'http://127.0.0.1:8000/protected' \
  -H 'Authorization: Bearer your_generated_token_here'
```
- If token is **valid**, response:
```json
{
  "message": "Hello Ali, here is your secure data!"
}
```
- If token is **wrong or expired**, response:
```json
{
  "detail": "Invalid token"
}
```

---

## Conclusion 🎉

- This project **generates JWT tokens** for users who log in.
- Users must **send their token** to access protected data.
- If the token is **wrong or expired**, they are **blocked**.

Now you know how to use JWT in FastAPI! 🚀

