from fastapi import HTTPException, Header
from typing import Optional

# Authentication
fake_token = "abc123"

def verify_token(authorization: Optional[str] = Header(None)):
    """Verify the authentication token"""
    if not authorization or authorization != f"Bearer {fake_token}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return authorization

def validate_credentials(username: str, password: str):
    """Validate user credentials and return a token if valid"""
    if username == "test" and password == "password":
        return fake_token
    return None
