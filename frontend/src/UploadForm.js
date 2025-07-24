import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

function UploadForm() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const dispatch = useDispatch();
  const token = useSelector(state => state.auth.token);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage('');
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file to upload');
      return;
    }

    setUploading(true);
    setMessage('');
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      // Upload the file
      const response = await fetch('/api/upload', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Upload failed');
      }

      // The backend now returns the file ID of the created record
      const fileId = data.id;
      
      // No need to create a temporary entry - the backend already created one with Processing status
      setMessage(`File ${file.name} uploaded and processing started`);
      setFile(null);
      
      // Poll for file status updates
      startPolling();
      
      // Immediately fetch files to show the Processing status
      fetchFiles();
      
    } catch (error) {
      setError(error.message);
    } finally {
      setUploading(false);
    }
  };

  // Poll for file status updates
  const startPolling = () => {
    // Initial fetch
    fetchFiles();
    
    // Set up polling every 2 seconds
    const pollInterval = setInterval(() => {
      fetchFiles();
    }, 2000);
    
    // Clear interval after 15 seconds (should be enough time for processing)
    setTimeout(() => {
      clearInterval(pollInterval);
      // Reset uploading state to ensure button is active again
      setUploading(false);
    }, 15000);
  };

  const fetchFiles = async () => {
    try {
      const response = await fetch('/api/files', {
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

  return (
    <div className="upload-container">
      <h2>Upload CSV File</h2>
      {message && <div className="success-message">{message}</div>}
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="file">Select CSV file:</label>
          <input
            type="file"
            id="file"
            accept=".csv"
            onChange={handleFileChange}
            disabled={uploading}
          />
        </div>
        <button type="submit" disabled={uploading || !file}>
          {uploading ? 'Uploading...' : 'Upload'}
        </button>
      </form>
    </div>
  );
}

export default UploadForm;
