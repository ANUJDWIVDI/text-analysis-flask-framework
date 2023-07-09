import React from 'react';
import { useHistory } from 'react-router-dom';

function App() {
  const history = useHistory();

  const handleStartClick = async () => {
    try {
      const response = await fetch('/'); // Send a GET request to the root path of the Flask server
      if (response.ok) {
        // If the request is successful, redirect to the Flask server
        window.location.href = response.url;
      } else {
        // Handle the case when the request fails
        console.error('Error:', response.status);
      }
    } catch (error) {
      console.error('Error:', error.message);
    }
  };

  return (
    <div>
      <h1>Welcome to Textopia!</h1>
      <p>
        Textopia is a powerful tool for text analysis. Click the button below to get started.
      </p>
      <button onClick={handleStartClick}>Start</button>
    </div>
  );
}

export default App;
