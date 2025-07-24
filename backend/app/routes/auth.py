from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from ..services.auth import validate_credentials
from ..utils.logger import logger

router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return token"""
    logger.info(f"Login attempt for user: {form_data.username}")
    token = validate_credentials(form_data.username, form_data.password)
    if token:
        logger.info(f"Successful login for user: {form_data.username}")
        return {"token": token}
    logger.warning(f"Failed login attempt for user: {form_data.username}")
    raise HTTPException(status_code=401, detail="Invalid credentials")
