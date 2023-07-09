import React from 'react';
import { useHistory } from 'react-router-dom';

function App() {
  const history = useHistory();

  const handleStartClick = () => {
    const { protocol, hostname } = window.location;
    const ipAddress = `${protocol}//${hostname}:5000`;
    window.location.href = ipAddress;
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
