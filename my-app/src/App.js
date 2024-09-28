import React, { useState } from 'react';

function App() {
  const [fallReported, setFallReported] = useState(false);

  const reportFall = async () => {
    const ip = "35.187.245.152"
    const response = await fetch('http://35.187.245.152:3000/report-fall', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: 'user123',
        timestamp: new Date().toISOString(),
      }),
    });
    
    if (response.ok) {
      setFallReported(true);
      alert('Fall reported!');
    }
  };

  return (
    <div>
      <h1>SafeStep</h1>
      <button onClick={reportFall}>Report Fall</button>
      {fallReported && <p>Fall reported successfully!</p>}
    </div>
  );
}

export default App;