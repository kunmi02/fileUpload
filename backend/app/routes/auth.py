from fastapi import APIRouter, HTTPException
from ..services.auth import validate_credentials

router = APIRouter()

@router.post("/login")
def login(data: dict):
    """Handle user login and return authentication token"""
    token = validate_credentials(data.get("username"), data.get("password"))
    if token:
        return {"token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")
