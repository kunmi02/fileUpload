import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import './FileTable.css';

function FileTable() {
  const dispatch = useDispatch();
  const { files, pagination, loading, error } = useSelector(state => state.files);
  const token = useSelector(state => state.auth.token);
  
  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);

  useEffect(() => {
    if (token) {
      fetchFiles(0, pageSize);
    }
  }, [token, pageSize]);

  const fetchFiles = async (skip, limit) => {
    dispatch({ type: 'FETCH_FILES_REQUEST' });
    
    try {
      const response = await fetch(`/api/files?skip=${skip}&limit=${limit}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      const data = await response.json();
      
      // Debug the API response
      console.log('API Response:', data);

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to fetch files');
      }

      dispatch({ type: 'FETCH_FILES_SUCCESS', payload: data });
      // Update current page based on the response
      if (data.page) {
        setCurrentPage(data.page);
      }
    } catch (error) {
      console.error('Error fetching files:', error);
      dispatch({ type: 'FETCH_FILES_FAILURE', payload: error.message });
    }
  };
  
  const handlePageChange = (newPage) => {
    const skip = (newPage - 1) * pageSize;
    setCurrentPage(newPage);
    fetchFiles(skip, pageSize);
  };
  
  const handlePageSizeChange = (event) => {
    const newSize = parseInt(event.target.value);
    setPageSize(newSize);
    // Reset to first page when changing page size
    fetchFiles(0, newSize);
  };

  if (loading) {
    return <div className="loading">Loading files...</div>;
  }

  if (error) {
    return <div className="error-message">Error: {error}</div>;
  }

  // Determine if we have files to display
  const hasFiles = Array.isArray(files) && files.length > 0;
  // Get pagination data from the store
  const totalItems = pagination?.total || 0;
  const totalPages = pagination?.pages || 1;
  
  return (
    <div className="file-table-container">
      <h2>Uploaded Files</h2>
      
      {/* Page size selector */}
      <div className="pagination-controls">
        <div className="page-size-control">
          <label htmlFor="page-size">Items per page: </label>
          <select 
            id="page-size" 
            value={pageSize} 
            onChange={handlePageSizeChange}
            disabled={loading}
          >
            <option value="5">5</option>
            <option value="10">10</option>
            <option value="25">25</option>
            <option value="50">50</option>
          </select>
        </div>
      </div>
      
      {!hasFiles ? (
        <p>No files uploaded yet.</p>
      ) : (
        <>
          <table className="file-table">
            <thead>
              <tr>
                <th>Filename</th>
                <th>Upload Date</th>
                <th>Rows</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {files.map((file) => (
                <tr key={file.id}>
                  <td>{file.filename}</td>
                  <td>{new Date(file.upload_timestamp).toLocaleString()}</td>
                  <td>{file.row_count}</td>
                  <td>
                    <span className={`status-badge status-${file.status.toLowerCase()}`}>
                      {file.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          
          {/* Pagination controls */}
          <div className="pagination-controls">
            <div className="pagination-info">
              Showing {files.length} of {totalItems} files
            </div>
            <div className="pagination-buttons">
              <button 
                onClick={() => handlePageChange(1)} 
                disabled={currentPage === 1 || loading}
              >
                &laquo; First
              </button>
              <button 
                onClick={() => handlePageChange(currentPage - 1)} 
                disabled={currentPage === 1 || loading}
              >
                &lsaquo; Previous
              </button>
              <span className="page-indicator">
                Page {currentPage} of {totalPages}
              </span>
              <button 
                onClick={() => handlePageChange(currentPage + 1)} 
                disabled={currentPage === totalPages || loading}
              >
                Next &rsaquo;
              </button>
              <button 
                onClick={() => handlePageChange(totalPages)} 
                disabled={currentPage === totalPages || loading}
              >
                Last &raquo;
              </button>
            </div>
          </div>
        </>
      )}
      
      <button 
        onClick={() => fetchFiles((currentPage - 1) * pageSize, pageSize)} 
        disabled={loading}
        className="refresh-button"
      >
        Refresh List
      </button>
    </div>
  );
}

export default FileTable;
