# CSV Upload Portal - Docker Setup

This document explains how to run the CSV Upload Portal using Docker.

## Prerequisites

- Docker and Docker Compose installed on your system
- Git (to clone the repository)

## Quick Start

1. Clone the repository (if you haven't already):
   ```
   git clone <repository-url>
   cd fullstack-assignment
   ```

2. Build and start the containers:
   ```
   docker-compose up -d
   ```

3. Access the application:
   - Frontend: http://localhost
   - Backend API: http://localhost/api

## Architecture

The Docker setup consists of two services:

1. **Backend (FastAPI)**
   - Python-based API service with modular architecture
   - Organized into routes, services, models, and database layers
   - Handles CSV file uploads and processing
   - Converts CSV to Parquet format
   - Stores metadata in SQLite database

2. **Frontend (React)**
   - React-based web interface
   - Communicates with the backend via API
   - Displays file upload status and metadata

## Persistent Data

The following data is persisted using Docker volumes:
- Uploaded CSV files
- Generated Parquet files
- SQLite database with file metadata

## Development

To make changes to the code and see them reflected:

1. For backend changes:
   - Edit files in the `backend/app` directory structure
   - Changes to routes, services, models, or database operations should be made in their respective modules
   - The changes will be automatically detected and the server will reload

2. For frontend changes:
   - Edit files in the `frontend` directory
   - Rebuild the frontend container:
     ```
     docker-compose build frontend
     docker-compose up -d
     ```

## Troubleshooting

- **Backend not starting**: Check logs with `docker-compose logs backend`
- **Frontend not connecting to backend**: Ensure the backend is running and the API proxy is configured correctly
- **File uploads failing**: Check backend logs and ensure the upload directory is writable

## Stopping the Application

To stop the application:
```
docker-compose down
```

To stop and remove all data (including volumes):
```
docker-compose down -v
```
