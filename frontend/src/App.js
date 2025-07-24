import React from 'react';
import UploadForm from './UploadForm';
import FileTable from './FileTable';
import Login from './Login';
import { useSelector } from 'react-redux';

function App() {
  const isAuthenticated = useSelector(state => state.auth.token);
  return (
    <div>
      <h1>CSV Upload Portal</h1>
      {!isAuthenticated ? <Login /> : (
        <>
          <UploadForm />
          <FileTable />
        </>
      )}
    </div>
  );
}
export default App;
