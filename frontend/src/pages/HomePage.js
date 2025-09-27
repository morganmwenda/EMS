import React from 'react';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
  const navigate = useNavigate();

  const initiateEmergency = () => {
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          navigate('/emergency', {
            state: {
              latitude: position.coords.latitude,
              longitude: position.coords.longitude
            }
          });
        },
        (error) => {
          alert('❌ Location access denied. Please enable location services for emergency dispatch.');
        }
      );
    } else {
      alert('❌ Geolocation is not supported by this browser.');
    }
  };

  return (
    <div className="container">
      <div className="card" style={{ textAlign: 'center', color: 'white' }}>
        <h1 style={{ fontSize: '3rem', marginBottom: '1rem', fontWeight: 700 }}>
          🚑 Emergency Management System
        </h1>
        <p style={{ fontSize: '1.2rem', marginBottom: '2rem', opacity: 0.9 }}>
          Fast, reliable emergency response when every second counts
        </p>
        
        <button className="emergency-btn" onClick={initiateEmergency}>
          🆘 EMERGENCY SOS
        </button>
        
        <div style={{ marginTop: '2rem', padding: '1rem', background: 'rgba(76, 175, 80, 0.2)', borderRadius: '10px', border: '1px solid rgba(76, 175, 80, 0.5)' }}>
          <h3>✅ System Status: Online</h3>
          <p>All emergency services are operational</p>
        </div>
        
        <div className="grid" style={{ color: 'white' }}>
          <div className="card">
            <h3>📍 GPS Tracking</h3>
            <p>Real-time location tracking of ambulances and emergency responses</p>
          </div>
          <div className="card">
            <h3>🚨 Instant Dispatch</h3>
            <p>Automated ambulance allocation based on proximity and specialization</p>
          </div>
          <div className="card">
            <h3>🏥 Hospital Integration</h3>
            <p>Seamless integration with local hospital databases</p>
          </div>
          <div className="card">
            <h3>👨‍⚕️ Medical Support</h3>
            <p>Video/voice consultation with healthcare professionals</p>
          </div>
        </div>
        
        <div style={{ marginTop: '2rem', display: 'flex', gap: '1rem', justifyContent: 'center' }}>
          <button 
            style={{ padding: '10px 20px', borderRadius: '25px', border: 'none', background: 'rgba(255,255,255,0.2)', color: 'white', cursor: 'pointer' }}
            onClick={() => navigate('/dashboard')}
          >
            📊 Dashboard
          </button>
          <button 
            style={{ padding: '10px 20px', borderRadius: '25px', border: 'none', background: 'rgba(255,255,255,0.2)', color: 'white', cursor: 'pointer' }}
            onClick={() => navigate('/tracking')}
          >
            🗺️ Live Tracking
          </button>
        </div>
      </div>
    </div>
  );
};

export default HomePage;