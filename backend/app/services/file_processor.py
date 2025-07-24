import os
import pandas as pd
from ..db.sqlite import update_file_record

# Directory setup
UPLOAD_DIR = './uploads'
PARQUET_DIR = './parquet'
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PARQUET_DIR, exist_ok=True)

def process_csv_to_parquet(file_path: str, filename: str, file_id: int):
    """Process a CSV file and convert it to Parquet format"""
    try:
        # Read CSV - add error handling for empty files
        try:
            # First check if file has any content at all
            with open(file_path, 'r') as f:
                first_line = f.readline().strip()
                has_content = bool(first_line)
            
            # Read with pandas
            df = pd.read_csv(file_path)
            
            # If file has headers but no data rows
            if df.shape[0] == 0 and has_content:
                print(f"CSV file has headers only: {filename}")
                # Count headers as 1 row if you want to treat header-only files as valid
                row_count = 1  # Set to 1 to count header as a row
            else:
                # Count actual data rows
                row_count = df.shape[0]
                
        except pd.errors.EmptyDataError:
            print(f"Empty CSV file: {filename}")
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
        
        # Update database with metadata
        update_file_record(file_id, row_count, parquet_path, status)
        
    except Exception as e:
        # Update database with error status
        update_file_record(file_id, 0, "", "Error")
        print(f"Error processing file {filename}: {str(e)}")

def save_uploaded_file(file_content, filename):
    """Save an uploaded file to the uploads directory"""
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(file_content)
    return file_path
