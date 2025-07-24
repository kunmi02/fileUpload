# CSV Upload Portal

A fullstack web application for uploading, processing, and managing CSV files with authentication. This project consists of a React frontend with Redux state management and a FastAPI backend.

## Project Structure

```
├── frontend/                # React frontend application
│   ├── public/             # Public assets
│   ├── src/                # Source files
│   │   ├── App.js          # Main application component
│   │   ├── Login.js        # Authentication component
│   │   ├── UploadForm.js   # File upload component
│   │   ├── FileTable.js    # Display uploaded files
│   │   └── store.js        # Redux store configuration
│   ├── package.json        # Frontend dependencies
│   ├── Dockerfile          # Frontend Docker configuration
│   └── nginx.conf          # Nginx configuration for serving the frontend
│
└── backend/                # FastAPI backend application
    ├── app/                # Modularized application package
    │   ├── main.py         # FastAPI app setup
    │   ├── routes/         # API route handlers
    │   │   ├── auth.py     # Authentication endpoints
    │   │   ├── upload.py   # File upload endpoints
    │   │   └── files.py    # File listing endpoints
    │   ├── services/       # Business logic services
    │   │   ├── auth.py     # Authentication service
    │   │   └── file_processor.py # CSV to Parquet conversion
    │   ├── models/         # Data models
    │   │   └── schemas.py  # Pydantic models
    │   └── db/             # Database operations
    │       └── sqlite.py   # SQLite database access
    ├── main.py             # Entry point for Docker
    ├── run.py              # Development server entry point
    ├── Dockerfile          # Backend Docker configuration
    └── requirements.txt    # Python dependencies
```

## Technologies Used

### Frontend
- **React 18**: UI library for building the user interface
- **Redux 4**: State management for the application
- **React-Redux 8**: React bindings for Redux

### Backend
- **FastAPI**: Modern, high-performance web framework for building APIs
- **Uvicorn**: ASGI server for running the FastAPI application
- **Pandas & PyArrow**: Data processing libraries for CSV and Parquet files
- **SQLAlchemy**: SQL toolkit and ORM for database operations

## Setup Instructions

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```
4. The frontend will be available at `http://localhost:3000`

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
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
5. API documentation is available at `http://localhost:8000/docs`

## Features

### Authentication
- Simple token-based authentication system
- Login credentials: 
  - Username: `test`
  - Password: `password`

### File Management
- Upload CSV files through an intuitive interface
- View list of uploaded files and their processing status
- Files are stored in the `uploads` directory on the server
- Automatic conversion to Parquet format for efficient storage

### API Endpoints
- `POST /login`: Authenticate and receive a token
- `POST /upload`: Upload CSV files (requires authentication)
- `GET /files`: Retrieve list of uploaded files (requires authentication)

## Development

The application uses CORS middleware to allow cross-origin requests, making local development easier. The backend creates necessary directories (`uploads` and `parquet`) automatically if they don't exist.

## Future Enhancements

- Implement proper user management with secure password storage
- Add data visualization for uploaded CSV files
- Implement file processing status tracking
- Add pagination for file listings
- Implement data validation for uploaded files
