from fastapi import APIRouter, Depends
from typing import List
from ..services.auth import verify_token
from ..db.sqlite import get_all_files
from ..models.schemas import FileMetadata

router = APIRouter()

@router.get("/files", response_model=List[FileMetadata])
def get_files(authorization: str = Depends(verify_token)):
    """Get a list of all files and their metadata"""
    return get_all_files()
