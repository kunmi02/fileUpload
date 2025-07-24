from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any
from ..services.auth import verify_token
from ..db.sqlite import get_all_files
from ..models.schemas import FileMetadata, PaginatedResponse
from ..utils.logger import logger

router = APIRouter()

from fastapi import Request

@router.get("/files")
async def get_files(
    request: Request,
    authorization: str = Depends(verify_token),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return")
):
    """Get a paginated list of files and their metadata"""
    # Log all query parameters for debugging
    query_params = dict(request.query_params)
    logger.info(f"All query parameters: {query_params}")
    logger.info(f"DEBUG: Received query parameters - skip={type(skip)}:{skip}, limit={type(limit)}:{limit}")
    
    # Force conversion to integers
    try:
        skip_val = int(skip)
        limit_val = int(limit)
    except (ValueError, TypeError):
        skip_val = 0
        limit_val = 10
    
    logger.info(f"Using pagination parameters: skip={skip_val}, limit={limit_val}")
    
    files, total_count = get_all_files(skip=skip_val, limit=limit_val)
    
    # Calculate pagination metadata
    next_page = skip_val + limit_val if skip_val + limit_val < total_count else None
    prev_page = skip_val - limit_val if skip_val - limit_val >= 0 else None
    
    logger.info(f"Retrieved {len(files)} file metadata records (total: {total_count})")
    
    return {
        "items": files,
        "total": total_count,
        "page": skip_val // limit_val + 1 if limit_val > 0 else 1,
        "size": limit_val,
        "pages": (total_count + limit_val - 1) // limit_val if limit_val > 0 else 1,
        "next": next_page,
        "previous": prev_page
    }
