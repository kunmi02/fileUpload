import sqlite3
import os
from ..config import DB_PATH

# Database setup is now handled by config.py

def init_db():
    """Initialize the SQLite database with necessary tables"""
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

def get_connection():
    """Get a connection to the SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

def insert_file_record(filename, upload_timestamp, row_count=0, parquet_path="", status="Processing"):
    """Insert a new file record into the database"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO files (filename, upload_timestamp, row_count, parquet_path, status) VALUES (?, ?, ?, ?, ?)",
        (filename, upload_timestamp, row_count, parquet_path, status)
    )
    file_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return file_id

def update_file_record(file_id, row_count, parquet_path, status):
    """Update an existing file record in the database"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE files SET row_count = ?, parquet_path = ?, status = ? WHERE id = ?",
        (row_count, parquet_path, status, file_id)
    )
    conn.commit()
    conn.close()

def get_all_files(skip: int = 0, limit: int = 100):
    """Get files from the database with pagination, ordered by upload timestamp
    
    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        
    Returns:
        tuple: (files, total_count) where files is a list of file records and
               total_count is the total number of records in the database
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get total count for pagination metadata
    cursor.execute("SELECT COUNT(*) as count FROM files")
    total_count = cursor.fetchone()["count"]
    
    # Get paginated results
    cursor.execute(
        "SELECT * FROM files ORDER BY upload_timestamp DESC LIMIT ? OFFSET ?",
        (limit, skip)
    )
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
    
    return files, total_count
