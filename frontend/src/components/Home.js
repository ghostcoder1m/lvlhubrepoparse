import React, { useEffect } from 'react';

const Home = () => {
  useEffect(() => {
    console.log("Home component rendered"); // Debugging line
  }, []);

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1 style={{ color: '#333', marginBottom: '20px' }}>Welcome to the STEPS Marketing System</h1>
      <p style={{ fontSize: '18px', lineHeight: '1.6' }}>
        Your one-stop solution for hyper-personalized marketing automation.
      </p>
    </div>
  );
};

export default Home;
