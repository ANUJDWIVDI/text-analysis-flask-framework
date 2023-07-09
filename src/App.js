import React from 'react';

function App() {
  const handleStartClick = () => {
    const ipAddress = `${window.location.protocol}//${window.location.hostname}:5000`;
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
