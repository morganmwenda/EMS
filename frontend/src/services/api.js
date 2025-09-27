import { API_ENDPOINTS, getAuthHeaders } from '../config/api';

// Generic API request function
const apiRequest = async (url, options = {}) => {
  const config = {
    headers: getAuthHeaders(),
    ...options,
  };

  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      return await response.json();
    }
    
    return await response.text();
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
};

// Authentication API functions
export const authAPI = {
  register: (userData) => apiRequest(API_ENDPOINTS.auth.register, {
    method: 'POST',
    body: JSON.stringify(userData),
  }),
  
  login: (credentials) => apiRequest(API_ENDPOINTS.auth.login, {
    method: 'POST',
    body: JSON.stringify(credentials),
  }),
  
  logout: () => apiRequest(API_ENDPOINTS.auth.logout, {
    method: 'POST',
  }),
  
  getProfile: () => apiRequest(API_ENDPOINTS.auth.profile),
  
  emergencySOS: (locationData) => apiRequest(API_ENDPOINTS.auth.emergencySOS, {
    method: 'POST',
    body: JSON.stringify(locationData),
  }),
};

// Ambulance API functions
export const ambulanceAPI = {
  getAll: () => apiRequest(API_ENDPOINTS.ambulances.list),
  
  getNearest: (location) => apiRequest(
    `${API_ENDPOINTS.ambulances.nearest}?lat=${location.lat}&lng=${location.lng}`
  ),
  
  getById: (id) => apiRequest(API_ENDPOINTS.ambulances.detail(id)),
  
  updateLocation: (id, locationData) => apiRequest(API_ENDPOINTS.ambulances.updateLocation(id), {
    method: 'POST',
    body: JSON.stringify(locationData),
  }),
};

// Emergency API functions
export const emergencyAPI = {
  getAll: () => apiRequest(API_ENDPOINTS.emergencies.list),
  
  create: (emergencyData) => apiRequest(API_ENDPOINTS.emergencies.create, {
    method: 'POST',
    body: JSON.stringify(emergencyData),
  }),
  
  getById: (id) => apiRequest(API_ENDPOINTS.emergencies.detail(id)),
  
  update: (id, updateData) => apiRequest(API_ENDPOINTS.emergencies.update(id), {
    method: 'PUT',
    body: JSON.stringify(updateData),
  }),
  
  dispatch: (id, dispatchData) => apiRequest(API_ENDPOINTS.emergencies.dispatch(id), {
    method: 'POST',
    body: JSON.stringify(dispatchData),
  }),
  
  getTypes: () => apiRequest(API_ENDPOINTS.emergencies.types),
};

// Tracking API functions
export const trackingAPI = {
  getAll: () => apiRequest(API_ENDPOINTS.tracking.list),
};

// Hospital API functions
export const hospitalAPI = {
  getAll: () => apiRequest(API_ENDPOINTS.hospitals.list),
};

// Notification API functions
export const notificationAPI = {
  getAll: () => apiRequest(API_ENDPOINTS.notifications.list),
};

// Helper function to handle location-based requests
export const getCurrentLocation = () => {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('Geolocation is not supported by this browser'));
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        resolve({
          lat: position.coords.latitude,
          lng: position.coords.longitude,
          accuracy: position.coords.accuracy,
        });
      },
      (error) => {
        reject(error);
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 300000, // 5 minutes
      }
    );
  });
};

export default apiRequest;