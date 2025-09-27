import React, { useState, useEffect } from 'react';
import { emergencyAPI, ambulanceAPI, hospitalAPI } from '../services/api';

const ApiTestComponent = () => {
  const [apiStatus, setApiStatus] = useState({
    emergencies: 'testing...',
    ambulances: 'testing...',
    hospitals: 'testing...',
  });

  useEffect(() => {
    testApiConnections();
  }, []);

  const testApiConnections = async () => {
    // Test Emergency API
    try {
      await emergencyAPI.getAll();
      setApiStatus(prev => ({ ...prev, emergencies: '✅ Connected' }));
    } catch (error) {
      setApiStatus(prev => ({ ...prev, emergencies: `❌ Error: ${error.message}` }));
    }

    // Test Ambulance API
    try {
      await ambulanceAPI.getAll();
      setApiStatus(prev => ({ ...prev, ambulances: '✅ Connected' }));
    } catch (error) {
      setApiStatus(prev => ({ ...prev, ambulances: `❌ Error: ${error.message}` }));
    }

    // Test Hospital API
    try {
      await hospitalAPI.getAll();
      setApiStatus(prev => ({ ...prev, hospitals: '✅ Connected' }));
    } catch (error) {
      setApiStatus(prev => ({ ...prev, hospitals: `❌ Error: ${error.message}` }));
    }
  };

  return (
    <div style={{
      position: 'fixed',
      top: '10px',
      right: '10px',
      background: 'white',
      padding: '15px',
      border: '1px solid #ddd',
      borderRadius: '8px',
      boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
      fontSize: '14px',
      zIndex: 1000,
      minWidth: '250px'
    }}>
      <h4 style={{ margin: '0 0 10px 0', color: '#333' }}>🔌 API Connection Status</h4>
      <div><strong>Emergencies:</strong> {apiStatus.emergencies}</div>
      <div><strong>Ambulances:</strong> {apiStatus.ambulances}</div>
      <div><strong>Hospitals:</strong> {apiStatus.hospitals}</div>
      <button 
        onClick={testApiConnections}
        style={{
          marginTop: '10px',
          padding: '5px 10px',
          background: '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
          fontSize: '12px'
        }}
      >
        🔄 Retest
      </button>
    </div>
  );
};

export default ApiTestComponent;