from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any
from ..services.auth import verify_token
from ..db.sqlite import get_all_files
from ..models.schemas import FileMetadata, PaginatedResponse
from ..utils.logger import logger

router = APIRouter()

@router.get("/files")
@router.get("/")
def get_files(
    authorization: str = Depends(verify_token),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return")
):
    """Get a paginated list of files and their metadata"""
    logger.info(f"DEBUG: Received query parameters - skip={skip}, limit={limit}")
    
    files, total_count = get_all_files(skip=skip, limit=limit)
    
    # Calculate pagination metadata
    next_page = skip + limit if skip + limit < total_count else None
    prev_page = skip - limit if skip - limit >= 0 else None
    
    logger.info(f"Retrieved {len(files)} file metadata records (total: {total_count})")
    
    return {
        "items": files,
        "total": total_count,
        "page": skip // limit + 1 if limit > 0 else 1,
        "size": limit,
        "pages": (total_count + limit - 1) // limit if limit > 0 else 1,
        "next": next_page,
        "previous": prev_page
    }
