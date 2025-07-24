from fastapi import APIRouter, UploadFile, File, Depends, BackgroundTasks, HTTPException
from ..services.auth import verify_token
from ..services.file_processor import process_csv_to_parquet, save_uploaded_file
from ..db.sqlite import insert_file_record
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
        raise HTTPException(status_code=400, detail="Only CSV files are accepted")
    
    # Read the file content
    content = file.file.read()
    
    # Save the file
    file_path = save_uploaded_file(content, file.filename)
    
    # Add initial entry to database with Processing status
    file_id = insert_file_record(file.filename, time.time() * 1000)
    
    # Process the file in the background
    background_tasks.add_task(process_csv_to_parquet, file_path, file.filename, file_id)
    
    return {"message": f"File {file.filename} uploaded and processing started", "id": file_id}
