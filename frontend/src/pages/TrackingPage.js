import React from 'react';

const TrackingPage = () => {
  return (
    <div className="tracking-page">
      <h1>🗺️ Real-time Tracking</h1>
      <p>Live ambulance tracking - to be implemented</p>
      <div className="tracking-container" style={{
        width: '100%',
        height: '400px',
        backgroundColor: '#e9ecef',
        border: '1px solid #ddd',
        borderRadius: '8px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        marginTop: '20px'
      }}>
        <div style={{ textAlign: 'center' }}>
          <h3>🗺️ Map View</h3>
          <p>Interactive map with ambulance locations will be displayed here</p>
          <small>Integration with Leaflet maps coming soon</small>
        </div>
      </div>
    </div>
  );
};

export default TrackingPage;