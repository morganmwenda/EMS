#!/usr/bin/env python3
"""
Simple HTTP server to demonstrate EMS backend functionality
This serves as a fallback when Django dependencies are not available
"""

import http.server
import socketserver
import json
import urllib.parse
from datetime import datetime
import uuid
import math


class EMSHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="templates", **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.serve_index()
        elif self.path.startswith('/api/'):
            self.handle_api_get()
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path.startswith('/api/'):
            self.handle_api_post()
        else:
            self.send_error(404)
    
    def serve_index(self):
        try:
            with open('templates/index.html', 'r') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content.encode())
        except FileNotFoundError:
            self.send_error(404, "Index file not found")
    
    def handle_api_get(self):
        if self.path == '/api/ambulances/':
            self.send_json_response(self.get_ambulances())
        elif self.path == '/api/emergencies/':
            self.send_json_response(self.get_emergencies())
        elif self.path == '/api/hospitals/':
            self.send_json_response(self.get_hospitals())
        else:
            self.send_error(404, "API endpoint not found")
    
    def handle_api_post(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return
        
        if self.path == '/api/auth/emergency-sos/':
            response = self.handle_emergency_sos(data)
            self.send_json_response(response)
        elif self.path == '/api/ambulances/nearest/':
            response = self.find_nearest_ambulance(data)
            self.send_json_response(response)
        elif self.path == '/api/auth/register/':
            response = self.handle_registration(data)
            self.send_json_response(response)
        else:
            self.send_error(404, "API endpoint not found")
    
    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def handle_emergency_sos(self, data):
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if not latitude or not longitude:
            return {'success': False, 'error': 'Location is required for emergency dispatch'}
        
        # Generate emergency ID
        emergency_id = f"EMG-{str(uuid.uuid4())[:8].upper()}"
        
        # Simulate finding nearest ambulance
        ambulances = self.get_sample_ambulances()
        nearest = self.calculate_nearest(latitude, longitude, ambulances)
        
        eta_minutes = nearest['distance_km'] / 60 * 60  # Rough calculation
        eta_minutes = max(5, min(30, int(eta_minutes)))
        
        return {
            'success': True,
            'emergency_id': emergency_id,
            'message': 'Emergency dispatch initiated. Help is on the way!',
            'estimated_arrival': f'{eta_minutes}-{eta_minutes + 4} minutes',
            'ambulance': nearest,
            'timestamp': datetime.now().isoformat()
        }
    
    def find_nearest_ambulance(self, data):
        latitude = float(data.get('latitude'))
        longitude = float(data.get('longitude'))
        
        ambulances = self.get_sample_ambulances()
        nearest = self.calculate_nearest(latitude, longitude, ambulances)
        
        return {
            'success': True,
            'ambulance': nearest
        }
    
    def calculate_nearest(self, lat, lon, ambulances):
        min_distance = float('inf')
        nearest = None
        
        for ambulance in ambulances:
            if ambulance['status'] == 'available':
                # Simple distance calculation (not accurate for real use)
                amb_lat = ambulance['location']['latitude']
                amb_lon = ambulance['location']['longitude']
                distance = math.sqrt((lat - amb_lat)**2 + (lon - amb_lon)**2) * 111  # Rough km conversion
                
                if distance < min_distance:
                    min_distance = distance
                    nearest = ambulance.copy()
                    nearest['distance_km'] = round(distance, 2)
                    nearest['eta_minutes'] = max(5, int(distance / 60 * 60))
        
        return nearest or ambulances[0]  # Fallback to first ambulance
    
    def handle_registration(self, data):
        username = data.get('username')
        email = data.get('email')
        
        if not username or not email:
            return {'success': False, 'error': 'Username and email are required'}
        
        return {
            'success': True,
            'message': 'User registered successfully',
            'user_id': str(uuid.uuid4())
        }
    
    def get_ambulances(self):
        return {'ambulances': self.get_sample_ambulances()}
    
    def get_emergencies(self):
        return {
            'emergencies': [
                {
                    'id': 'EMG-12345678',
                    'type': 'Medical Emergency',
                    'status': 'dispatched',
                    'location': {'latitude': 40.7128, 'longitude': -74.0060},
                    'reported_at': '2024-01-15T10:30:00Z',
                    'severity': 'high'
                },
                {
                    'id': 'EMG-87654321',
                    'type': 'Traffic Accident',
                    'status': 'en_route',
                    'location': {'latitude': 40.7589, 'longitude': -73.9851},
                    'reported_at': '2024-01-15T09:45:00Z',
                    'severity': 'critical'
                }
            ]
        }
    
    def get_hospitals(self):
        return {
            'hospitals': [
                {
                    'id': 1,
                    'name': 'General Hospital',
                    'type': 'general',
                    'location': {'latitude': 40.7505, 'longitude': -73.9934},
                    'emergency_services': True,
                    'available_beds': 25
                },
                {
                    'id': 2,
                    'name': 'Trauma Center',
                    'type': 'trauma',
                    'location': {'latitude': 40.7282, 'longitude': -73.9942},
                    'emergency_services': True,
                    'available_beds': 12
                }
            ]
        }
    
    def get_sample_ambulances(self):
        return [
            {
                'id': 1,
                'license_plate': 'AMB-001',
                'type': 'Advanced Life Support',
                'status': 'available',
                'location': {'latitude': 40.7589, 'longitude': -73.9851},
                'crew_count': 2,
                'equipment': ['defibrillator', 'ventilator', 'cardiac_monitor']
            },
            {
                'id': 2,
                'license_plate': 'AMB-002',
                'type': 'Basic Life Support',
                'status': 'available',
                'location': {'latitude': 40.7306, 'longitude': -73.9352},
                'crew_count': 2,
                'equipment': ['basic_supplies', 'oxygen', 'stretcher']
            },
            {
                'id': 3,
                'license_plate': 'AMB-003',
                'type': 'Critical Care',
                'status': 'dispatched',
                'location': {'latitude': 40.7505, 'longitude': -73.9934},
                'crew_count': 3,
                'equipment': ['ventilator', 'icu_equipment', 'blood_bank']
            }
        ]


def run_server(port=8000):
    """Run the EMS demo server"""
    handler = EMSHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"🚑 EMS Server running at http://localhost:{port}")
        print("📱 API endpoints available:")
        print("  • POST /api/auth/emergency-sos/")
        print("  • GET  /api/ambulances/")
        print("  • POST /api/ambulances/nearest/")
        print("  • GET  /api/emergencies/")
        print("  • GET  /api/hospitals/")
        print("\n🆘 Try the Emergency SOS button on the homepage!")
        print("Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped")


if __name__ == "__main__":
    run_server()