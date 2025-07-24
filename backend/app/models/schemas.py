from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class FileMetadata(BaseModel):
    id: int
    filename: str
    upload_timestamp: float  # Unix timestamp in milliseconds
    row_count: int
    parquet_path: str
    status: str

class PaginatedResponse(BaseModel):
    """Schema for paginated response"""
    items: List[FileMetadata]
    total: int
    page: int
    size: int
    pages: int
    next: Optional[int] = None
    previous: Optional[int] = None
