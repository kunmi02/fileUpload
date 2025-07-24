# CSV Upload Portal - Frontend

This is the frontend component of the CSV Upload Portal, built with React and Redux.

## Overview

The frontend provides a user interface for:
- User authentication (login)
- File upload functionality
- Viewing uploaded files

## Tech Stack

- **React 18**: UI library for building the user interface
- **Redux 4**: State management for the application
- **React-Redux 8**: React bindings for Redux

## Project Structure

```
frontend/
├── public/              # Public assets
├── src/                 # Source files
│   ├── App.js           # Main application component
│   ├── Login.js         # Authentication component
│   ├── UploadForm.js    # File upload component
│   ├── FileTable.js     # Display uploaded files
│   └── store.js         # Redux store configuration
└── package.json         # Frontend dependencies
```

## Component Overview

- **App.js**: Main application component that handles routing and layout
- **Login.js**: Handles user authentication and token storage
- **UploadForm.js**: Provides interface for uploading CSV files
- **FileTable.js**: Displays list of uploaded files and their status
- **store.js**: Redux store configuration for state management

## State Management

The application uses Redux for state management with the following key states:
- Authentication state (token, login status)
- File upload state (upload progress, errors)
- File list state (list of uploaded files)

## API Integration

The frontend communicates with the backend API at `http://localhost:8000` with the following endpoints:
- `POST /login`: For user authentication
- `POST /upload`: For file uploads
- `GET /files`: For retrieving the list of files

## Setup and Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

3. The application will be available at `http://localhost:3000`

## Development Notes

- The application uses token-based authentication stored in Redux state
- File uploads are handled via multipart/form-data
- The UI is designed to be responsive and user-friendly
- Authentication token is included in the Authorization header for protected API calls

## Testing

To run the test suite:
```bash
npm test
```

## Building for Production

To create a production build:
```bash
npm run build
```

This will create an optimized build in the `build` folder that can be deployed to any static hosting service.
