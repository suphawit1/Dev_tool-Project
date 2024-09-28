import React, { useState } from 'react';

function App() {
  const [fallReported, setFallReported] = useState(false);

  const reportFall = async () => {
    const response = await fetch('http://35.187.245.152:8000/report-fall/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: 'user123',
        timestamp: new Date().toISOString(),
      }),
      redirect: 'manual' // This prevents automatic redirection
    });
    
    if (response.ok) {
      setFallReported(true);
      alert('Fall reported!');
    }
  };

  return (
    <div>
      <h1>SafeStep</h1>
      <button onClick={reportFall}>Rawdaweport Fall</button>
      {fallReported && <p>Fall reported successfully!</p>}
    </div>
  );
}

export default App;