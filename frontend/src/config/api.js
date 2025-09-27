// API configuration for connecting React frontend to Django backend
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// API endpoints configuration
export const API_ENDPOINTS = {
  // Authentication endpoints
  auth: {
    register: `${API_BASE_URL}/api/auth/register/`,
    login: `${API_BASE_URL}/api/auth/login/`,
    logout: `${API_BASE_URL}/api/auth/logout/`,
    profile: `${API_BASE_URL}/api/auth/profile/`,
    emergencySOS: `${API_BASE_URL}/api/auth/emergency-sos/`,
  },
  
  // Ambulance endpoints
  ambulances: {
    list: `${API_BASE_URL}/api/ambulances/`,
    nearest: `${API_BASE_URL}/api/ambulances/nearest/`,
    detail: (id) => `${API_BASE_URL}/api/ambulances/${id}/`,
    updateLocation: (id) => `${API_BASE_URL}/api/ambulances/${id}/location/`,
  },
  
  // Emergency endpoints
  emergencies: {
    list: `${API_BASE_URL}/api/emergencies/`,
    create: `${API_BASE_URL}/api/emergencies/create/`,
    detail: (id) => `${API_BASE_URL}/api/emergencies/${id}/`,
    update: (id) => `${API_BASE_URL}/api/emergencies/${id}/update/`,
    dispatch: (id) => `${API_BASE_URL}/api/emergencies/${id}/dispatch/`,
    types: `${API_BASE_URL}/api/emergencies/types/`,
  },
  
  // Tracking endpoints
  tracking: {
    list: `${API_BASE_URL}/api/tracking/`,
  },
  
  // Notification endpoints
  notifications: {
    list: `${API_BASE_URL}/api/notifications/`,
  },
  
  // Hospital endpoints
  hospitals: {
    list: `${API_BASE_URL}/api/hospitals/`,
  },
};

// Default headers for API requests
export const DEFAULT_HEADERS = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
};

// Helper function to get auth headers
export const getAuthHeaders = () => {
  const token = localStorage.getItem('authToken');
  return token ? { ...DEFAULT_HEADERS, 'Authorization': `Bearer ${token}` } : DEFAULT_HEADERS;
};

export default API_BASE_URL;