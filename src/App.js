import React from 'react';
import { useHistory } from 'react-router-dom';

function App() {
  const history = useHistory();

  const handleStartClick = () => {
    window.location.href = 'http://localhost:5000/';
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
