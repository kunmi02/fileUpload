from fastapi import APIRouter, UploadFile, File, Depends, BackgroundTasks, HTTPException
from ..services.auth import verify_token
from ..services.file_processor import process_csv_to_parquet, save_uploaded_file
from ..db.sqlite import insert_file_record
from ..config import MAX_UPLOAD_SIZE
from ..utils.logger import logger
import time

router = APIRouter()

@router.post("/upload")
def upload(
    file: UploadFile = File(...), 
    background_tasks: BackgroundTasks = None, 
    authorization: str = Depends(verify_token)
):
    """Handle file upload, save the file, and start background processing"""
    # Validate file is CSV
    if not file.filename.endswith('.csv'):
        logger.warning(f"Rejected non-CSV file upload attempt: {file.filename}")
        raise HTTPException(status_code=400, detail="Only CSV files are accepted")
    
    # Check file size before reading content
    # FastAPI's UploadFile has a file attribute which is a SpooledTemporaryFile
    # We can use seek and tell to determine the file size
    file.file.seek(0, 2)  # Seek to the end of the file
    file_size = file.file.tell()  # Get current position (file size)
    file.file.seek(0)  # Reset file position to the beginning
    
    # Validate file size
    if file_size > MAX_UPLOAD_SIZE:
        logger.warning(f"Rejected file upload due to size: {file.filename}, size: {file_size / (1024 * 1024):.2f} MB")
        raise HTTPException(
            status_code=413,  # Request Entity Too Large
            detail=f"File too large. Maximum allowed size is {MAX_UPLOAD_SIZE / (1024 * 1024):.2f} MB"
        )
    
    # Read the file content
    content = file.file.read()
    
    # Save the file
    file_path = save_uploaded_file(content, file.filename)
    
    # Add initial entry to database with Processing status
    file_id = insert_file_record(file.filename, time.time() * 1000)
    
    # Process the file in the background
    background_tasks.add_task(process_csv_to_parquet, file_path, file.filename, file_id)
    
    logger.info(f"File uploaded successfully: {file.filename}, id: {file_id}, size: {file_size / 1024:.2f} KB")
    return {"message": f"File {file.filename} uploaded and processing started", "id": file_id}
