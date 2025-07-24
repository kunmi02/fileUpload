from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Header, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import time
import pandas as pd
import sqlite3
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory setup
UPLOAD_DIR = './uploads'
PARQUET_DIR = './parquet'
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PARQUET_DIR, exist_ok=True)

# Database setup
DB_PATH = './metadata.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        upload_timestamp TIMESTAMP NOT NULL,
        row_count INTEGER NOT NULL,
        parquet_path TEXT NOT NULL,
        status TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Authentication
fake_token = "abc123"

def verify_token(authorization: Optional[str] = Header(None)):
    if not authorization or authorization != f"Bearer {fake_token}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return authorization

# Models
class FileMetadata(BaseModel):
    id: int
    filename: str
    upload_timestamp: float  # Unix timestamp in milliseconds
    row_count: int
    parquet_path: str
    status: str

# Background task for processing CSV to Parquet
def process_csv_to_parquet(file_path: str, filename: str, file_id: int):
    try:
        # Read CSV - add error handling for empty files
        try:
            # First check if file has any content at all
            with open(file_path, 'r') as f:
                first_line = f.readline().strip()
                has_content = bool(first_line)
            
            # Read with pandas
            df = pd.read_csv(file_path)
            # print(f"CSV file loaded: {filename}, shape: {df.shape}")
            
            # If file has headers but no data rows
            if df.shape[0] == 0 and has_content:
                print(f"CSV file has headers only: {filename}")
                # Count headers as 1 row if you want to treat header-only files as valid
                row_count = 1  # Set to 1 to count header as a row
                # print(f"Counting header as a row, so row_count = {row_count}")
            else:
                # Count actual data rows
                row_count = df.shape[0]
                # print(f"CSV has {row_count} data rows")
                
            # print("DataFrame content:", df)
        except pd.errors.EmptyDataError:
            # print(f"Empty CSV file: {filename}")
            df = pd.DataFrame()
            row_count = 0
        
        # Create parquet filename
        base_filename = os.path.splitext(filename)[0]
        parquet_filename = f"{base_filename}.parquet"
        parquet_path = os.path.join(PARQUET_DIR, parquet_filename)
        
        # Convert to parquet
        if row_count > 0:
            df.to_parquet(parquet_path, index=False)
        else:
            # Create an empty file to mark it was processed
            with open(parquet_path, 'wb') as f:
                pass
        
        # Determine status based on row count
        status = "Done" if row_count > 0 else "Error"
        
        # Update database with metadata - update existing record instead of inserting new one
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE files SET row_count = ?, parquet_path = ?, status = ? WHERE id = ?",
            (row_count, parquet_path, status, file_id)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        # Update database with error status - update existing record
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE files SET row_count = ?, parquet_path = ?, status = ? WHERE id = ?",
            (0, "", "Error", file_id)
        )
        conn.commit()
        conn.close()
        print(f"Error processing file {filename}: {str(e)}")


# Endpoints
@app.post("/login")
def login(data: dict):
    if data.get("username") == "test" and data.get("password") == "password":
        return {"token": fake_token}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/upload")
def upload(file: UploadFile = File(...), background_tasks: BackgroundTasks = None, authorization: str = Depends(verify_token)):
    # Validate file is CSV
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted")
    
    # Save the file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # Read the file content
    content = file.file.read()
    
    # Save the file
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Add initial entry to database with Processing status
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO files (filename, upload_timestamp, row_count, parquet_path, status) VALUES (?, ?, ?, ?, ?)",
        (file.filename, time.time() * 1000, 0, "", "Processing")
    )
    file_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    # Process the file in the background
    background_tasks.add_task(process_csv_to_parquet, file_path, file.filename, file_id)
    
    return {"message": f"File {file.filename} uploaded and processing started", "id": file_id}

@app.get("/files", response_model=List[FileMetadata])
def get_files(authorization: str = Depends(verify_token)):
    # Get metadata from database
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM files ORDER BY upload_timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    
    # Convert to list of dictionaries
    files = []
    for row in rows:
        files.append({
            "id": row["id"],
            "filename": row["filename"],
            "upload_timestamp": row["upload_timestamp"],
            "row_count": row["row_count"],
            "parquet_path": row["parquet_path"],
            "status": row["status"]
        })
    
    return files
