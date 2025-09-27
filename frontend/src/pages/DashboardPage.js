import React, { useState, useEffect } from 'react';
import { emergencyAPI, ambulanceAPI, hospitalAPI } from '../services/api';

const DashboardPage = () => {
  const [dashboardData, setDashboardData] = useState({
    emergencies: { count: 0, data: [] },
    ambulances: { count: 0, data: [] },
    hospitals: { count: 0, data: [] },
    loading: true,
    error: null
  });

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setDashboardData(prev => ({ ...prev, loading: true, error: null }));
      
      const [emergenciesRes, ambulancesRes, hospitalsRes] = await Promise.all([
        emergencyAPI.getAll(),
        ambulanceAPI.getAll(),
        hospitalAPI.getAll()
      ]);

      setDashboardData({
        emergencies: { count: emergenciesRes.count || 0, data: emergenciesRes.results || [] },
        ambulances: { count: ambulancesRes.count || 0, data: ambulancesRes.results || [] },
        hospitals: { count: hospitalsRes.count || 0, data: hospitalsRes.results || [] },
        loading: false,
        error: null
      });
    } catch (error) {
      setDashboardData(prev => ({ ...prev, loading: false, error: error.message }));
    }
  };

  const availableAmbulances = dashboardData.ambulances.data.filter(amb => amb.is_available).length;
  const activeEmergencies = dashboardData.emergencies.data.filter(em => ['dispatched', 'en_route', 'on_scene'].includes(em.status)).length;

  if (dashboardData.loading) {
    return (
      <div className="dashboard-page">
        <h1>📊 Dashboard</h1>
        <p>Loading dashboard data...</p>
      </div>
    );
  }

  return (
    <div className="dashboard-page">
      <h1>📊 Emergency Management Dashboard</h1>
      {dashboardData.error && (
        <div style={{ color: 'red', padding: '10px', background: '#ffe6e6', borderRadius: '5px', marginBottom: '20px' }}>
          Error loading data: {dashboardData.error}
        </div>
      )}
      
      <div className="dashboard-grid" style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '20px',
        marginTop: '20px'
      }}>
        <div className="dashboard-card" style={{
          padding: '20px',
          border: '1px solid #ddd',
          borderRadius: '8px',
          backgroundColor: '#f8f9fa'
        }}>
          <h3>🚑 Ambulances</h3>
          <p><strong>{availableAmbulances}</strong> available out of <strong>{dashboardData.ambulances.count}</strong> total</p>
          <div style={{ fontSize: '14px', marginTop: '10px' }}>
            {dashboardData.ambulances.data.map(amb => (
              <div key={amb.id} style={{ display: 'flex', justifyContent: 'space-between', margin: '5px 0' }}>
                <span>{amb.license_plate}</span>
                <span style={{ color: amb.is_available ? 'green' : 'orange' }}>
                  {amb.status}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="dashboard-card" style={{
          padding: '20px',
          border: '1px solid #ddd',
          borderRadius: '8px',
          backgroundColor: '#f8f9fa'
        }}>
          <h3>🚨 Emergencies</h3>
          <p><strong>{activeEmergencies}</strong> active out of <strong>{dashboardData.emergencies.count}</strong> total</p>
          <div style={{ fontSize: '14px', marginTop: '10px' }}>
            {dashboardData.emergencies.data.map(emergency => (
              <div key={emergency.id} style={{ display: 'flex', justifyContent: 'space-between', margin: '5px 0' }}>
                <span>{emergency.emergency_id}</span>
                <span style={{ 
                  color: emergency.severity === 'critical' ? 'red' : 
                        emergency.severity === 'serious' ? 'orange' : 'blue' 
                }}>
                  {emergency.severity}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="dashboard-card" style={{
          padding: '20px',
          border: '1px solid #ddd',
          borderRadius: '8px',
          backgroundColor: '#f8f9fa'
        }}>
          <h3>🏥 Hospitals</h3>
          <p><strong>{dashboardData.hospitals.count}</strong> hospitals in network</p>
          <div style={{ fontSize: '14px', marginTop: '10px' }}>
            {dashboardData.hospitals.data.map(hospital => (
              <div key={hospital.id} style={{ margin: '5px 0' }}>
                <div style={{ fontWeight: 'bold' }}>{hospital.name}</div>
                <div style={{ color: '#666' }}>
                  {hospital.available_beds} beds available
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <button 
        onClick={loadDashboardData}
        style={{
          marginTop: '20px',
          padding: '10px 20px',
          background: '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer'
        }}
      >
        🔄 Refresh Data
      </button>
    </div>
  );
};

export default DashboardPage;