from fastapi import HTTPException, Header
from typing import Optional
from ..utils.logger import logger

# Authentication
fake_token = "abc123"

def verify_token(authorization: Optional[str] = Header(None)):
    """Verify the authentication token"""
    if not authorization:
        logger.warning("Token verification failed: No authorization header")
        raise HTTPException(status_code=401, detail="Unauthorized")
    if authorization != f"Bearer {fake_token}":
        logger.warning("Token verification failed: Invalid token")
        raise HTTPException(status_code=401, detail="Unauthorized")
    return authorization

def validate_credentials(username: str, password: str):
    """Validate user credentials and return a token if valid"""
    if username == "test" and password == "password":
        logger.debug(f"Credentials validated for user: {username}")
        return fake_token
    logger.debug(f"Invalid credentials for user: {username}")
    return None
