from pydantic import BaseModel

class FileMetadata(BaseModel):
    id: int
    filename: str
    upload_timestamp: float  # Unix timestamp in milliseconds
    row_count: int
    parquet_path: str
    status: str
