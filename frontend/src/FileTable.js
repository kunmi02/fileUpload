import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';

function FileTable() {
  const dispatch = useDispatch();
  const { files, loading, error } = useSelector(state => state.files);
  const token = useSelector(state => state.auth.token);

  useEffect(() => {
    if (token) {
      fetchFiles();
    }
  }, [token]);

  const fetchFiles = async () => {
    dispatch({ type: 'FETCH_FILES_REQUEST' });
    
    try {
      const response = await fetch('http://localhost:8000/files', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to fetch files');
      }

      dispatch({ type: 'FETCH_FILES_SUCCESS', payload: data });
    } catch (error) {
      dispatch({ type: 'FETCH_FILES_FAILURE', payload: error.message });
    }
  };

  if (loading) {
    return <div className="loading">Loading files...</div>;
  }

  if (error) {
    return <div className="error-message">Error: {error}</div>;
  }

  return (
    <div className="file-table-container">
      <h2>Uploaded Files</h2>
      {files.length === 0 ? (
        <p>No files uploaded yet.</p>
      ) : (
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
      )}
      <button onClick={fetchFiles} disabled={loading}>
        Refresh List
      </button>
    </div>
  );
}

export default FileTable;
