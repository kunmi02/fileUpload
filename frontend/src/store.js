import { createStore, combineReducers, applyMiddleware } from 'redux';

// Authentication reducer
const initialAuthState = {
  token: null,
  error: null,
  loading: false
};

const authReducer = (state = initialAuthState, action) => {
  switch (action.type) {
    case 'LOGIN_REQUEST':
      return { ...state, loading: true, error: null };
    case 'LOGIN_SUCCESS':
      return { ...state, token: action.payload, loading: false, error: null };
    case 'LOGIN_FAILURE':
      return { ...state, loading: false, error: action.payload };
    case 'LOGOUT':
      return { ...state, token: null };
    default:
      return state;
  }
};

// Files reducer
const initialFilesState = {
  files: [],
  loading: false,
  error: null
};

const filesReducer = (state = initialFilesState, action) => {
  switch (action.type) {
    case 'FETCH_FILES_REQUEST':
      return { ...state, loading: true, error: null };
      
    case 'FETCH_FILES_SUCCESS':
      // Merge any temporary processing files with the server response
      const tempFiles = state.files.filter(file => 
        file.id.toString().startsWith('temp-') && 
        !action.payload.find(serverFile => serverFile.filename === file.filename)
      );
      
      return { 
        ...state, 
        files: [...action.payload, ...tempFiles], 
        loading: false, 
        error: null 
      };
      
    case 'FETCH_FILES_FAILURE':
      return { ...state, loading: false, error: action.payload };
      
    case 'UPLOAD_FILE_PROCESSING':
      // Add a temporary file with Processing status
      return { 
        ...state, 
        files: [...state.files.filter(f => f.id !== action.payload.id), action.payload] 
      };
      
    case 'UPLOAD_FILE_SUCCESS':
      return { 
        ...state, 
        files: [...state.files.filter(f => f.id !== action.payload.id), action.payload] 
      };
      
    case 'UPLOAD_FILE_ERROR':
      return { 
        ...state, 
        files: state.files.map(file => 
          file.id === action.payload.id ? { ...file, status: 'Error' } : file
        )
      };
      
    default:
      return state;
  }
};

// Middleware for handling file status updates
const fileStatusMiddleware = store => next => action => {
  const result = next(action);
  
  // If we received new files from the server, check for status changes
  if (action.type === 'FETCH_FILES_SUCCESS') {
    // We'll rely on the backend to set the correct status
    // The backend will set:
    // - "Done" for files with rows > 0
    // - "Error" for files with 0 rows
    // - "Processing" for files still being processed
  }
  
  return result;
};

// Combine reducers
const rootReducer = combineReducers({
  auth: authReducer,
  files: filesReducer
});

// Create store with middleware
const store = createStore(
  rootReducer,
  applyMiddleware(fileStatusMiddleware)
);

export default store;
