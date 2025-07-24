# CSV Upload Portal - Backend

This is the backend component of the CSV Upload Portal, built with FastAPI.

## Overview

The backend provides a RESTful API for user authentication and file management, allowing users to:
- Authenticate using username and password
- Upload CSV files
- Retrieve a list of uploaded files

## Tech Stack

- **FastAPI**: Modern, high-performance web framework for building APIs
- **Uvicorn**: ASGI server for running the FastAPI application
- **Pandas & PyArrow**: Data processing libraries for CSV and Parquet files
- **SQLAlchemy**: SQL toolkit and ORM for database operations
- **Python-Multipart**: Library for handling file uploads

## Project Structure

```
backend/
├── main.py             # API endpoints and business logic
├── requirements.txt    # Python dependencies
├── uploads/            # Directory for storing uploaded CSV files (auto-created)
└── parquet/            # Directory for storing converted Parquet files (auto-created)
```

## API Endpoints

- `POST /login`: Authenticate and receive a token
  - Request body: `{"username": "test", "password": "password"}`
  - Response: `{"token": "abc123"}`

- `POST /upload`: Upload CSV files (requires authentication)
  - Request: Multipart form with file
  - Headers: `Authorization: Bearer abc123`
  - Response: `{"message": "Received filename.csv"}`

- `GET /files`: Retrieve list of uploaded files (requires authentication)
  - Headers: `Authorization: Bearer abc123`
  - Response: Array of file information

## Authentication

The backend uses a simple token-based authentication system. For development purposes, a hardcoded token (`abc123`) is used. In a production environment, this should be replaced with a more secure authentication system.

## Setup and Installation

1. Create and activate a virtual environment:
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate on macOS/Linux
   source venv/bin/activate
   
   # Activate on Windows
   .\venv\Scripts\activate
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

4. The API will be available at `http://localhost:8000`

5. API documentation is automatically available at:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## Development Notes

- The application automatically creates the necessary directories (`uploads` and `parquet`) if they don't exist
- CORS middleware is configured to allow requests from any origin, which is suitable for development but should be restricted in production
- The current implementation uses a simple in-memory authentication system; for production, implement a proper user management system
