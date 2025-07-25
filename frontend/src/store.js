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
  pagination: {
    total: 0,
    page: 1,
    size: 10,
    pages: 1,
    next: null,
    previous: null
  },
  loading: false,
  error: null
};

const filesReducer = (state = initialFilesState, action) => {
  switch (action.type) {
    case 'FETCH_FILES_REQUEST':
      return { ...state, loading: true, error: null };
      
    case 'FETCH_FILES_SUCCESS':
      
      // Force handling as paginated response
      let fileItems = [];
      let paginationData = {
        total: 0,
        page: 1,
        size: 10,
        pages: 1,
        next: null,
        previous: null
      };
      
      // Check response format and extract data
      if (action.payload && typeof action.payload === 'object' && 'items' in action.payload) {
        // Properly formatted paginated response
        const { items = [], total = 0, page = 1, size = 10, pages = 1, next = null, previous = null } = action.payload;
        fileItems = items;
        paginationData = { total, page, size, pages, next, previous };
      } else if (Array.isArray(action.payload)) {
        // Direct array of files (old format or incorrect response)
        fileItems = action.payload;
        paginationData.total = action.payload.length;
        paginationData.pages = Math.ceil(action.payload.length / paginationData.size);
      } else {
        // Unexpected format
        console.error('Unexpected response format:', action.payload);
        return { ...state, loading: false, error: 'Invalid response format from server' };
      }
      
      // Merge any temporary processing files with the server response
      const tempFiles = state.files.filter(file => 
        file.id.toString().startsWith('temp-') && 
        !fileItems.find(serverFile => serverFile.filename === file.filename)
      );
      
      return { 
        ...state, 
        files: [...fileItems, ...tempFiles], 
        pagination: paginationData,
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
