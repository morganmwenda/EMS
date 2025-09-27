import React from 'react';

const EmergencyPage = () => {
  return (
    <div className="emergency-page">
      <h1>🚨 Emergency</h1>
      <p>Emergency dispatch interface - to be implemented</p>
      <div className="emergency-actions">
        <button className="sos-button" style={{
          backgroundColor: '#dc3545',
          color: 'white',
          border: 'none',
          padding: '20px 40px',
          fontSize: '18px',
          borderRadius: '8px',
          cursor: 'pointer'
        }}>
          🆘 EMERGENCY SOS
        </button>
      </div>
    </div>
  );
};

export default EmergencyPage;