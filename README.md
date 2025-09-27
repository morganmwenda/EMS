# Emergency Management System (EMS) 🚑

A comprehensive emergency response application that allows users to instantly connect with and dispatch the nearest available ambulance. The solution includes both a responsive web application and cross-platform mobile applications for Android and iOS.

## 🌟 Features

### Core Functionality
- **🆘 Emergency SOS Button**: Instant one-tap emergency dispatch
- **📍 GPS Integration**: Real-time location tracking and nearest ambulance calculation
- **🚨 Smart Ambulance Allocation**: Match ambulances based on equipment and specialization
- **🗺️ Live Tracking**: Real-time ambulance movement tracking with ETA updates
- **🏥 Hospital Integration**: Automatic patient record sharing with local hospitals

### Patient Care Features
- **💓 Vitals Monitoring**: Basic vitals integration support
- **📞 Two-way Communication**: Voice/video consultation with healthcare professionals
- **📱 Multi-platform Access**: Web app, Android, and iOS applications

### Technical Features
- **🔐 Secure Authentication**: Google and Apple ID integration
- **🌐 Multi-language Support**: Accessible interface in multiple languages
- **⚡ Low Latency**: Optimized for speed and real-time responses
- **📳 Push Notifications**: SMS fallback for unstable internet connections
- **🔒 HIPAA/GDPR Compliant**: End-to-end encryption and privacy protection

## 🏗️ Architecture

### Backend (Django)
- **Framework**: Django 4.2+ with Django REST Framework
- **Database**: PostgreSQL with PostGIS for geospatial data
- **Real-time**: WebSocket support for live tracking
- **Authentication**: Multi-provider OAuth integration
- **APIs**: RESTful APIs for all functionality

### Frontend (React)
- **Framework**: React 18 with modern hooks
- **Mapping**: Leaflet integration for maps
- **State Management**: Context API and custom hooks
- **Responsive Design**: Mobile-first approach

### Mobile (Flutter)
- **Framework**: Flutter for cross-platform development
- **GPS**: High-accuracy location services
- **Push Notifications**: Firebase Cloud Messaging
- **Offline Support**: Queue requests when offline

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Node.js 18+
- Flutter 3.10+
- Docker & Docker Compose (recommended)

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone https://github.com/morganmwenda/EMS.git
   cd EMS
   ```

2. **Start all services**
   ```bash
   docker-compose up -d
   ```

3. **Access the applications**
   - Web App: http://localhost:3000
   - Backend API: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

### Manual Setup

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r ../requirements.txt

# Create migrations for all apps (important: correct order for custom user model)
python manage.py makemigrations authentication ambulances emergencies tracking notifications hospitals

# Apply all migrations
python manage.py migrate

# Create a superuser account
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

#### Mobile Setup
```bash
cd mobile
flutter pub get
flutter run
```

## 📱 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/emergency-sos/` - Emergency SOS dispatch

### Ambulances
- `GET /api/ambulances/` - List all ambulances
- `GET /api/ambulances/nearest/` - Find nearest ambulance
- `POST /api/ambulances/{id}/location/` - Update ambulance location

### Emergencies
- `GET /api/emergencies/` - List emergencies
- `POST /api/emergencies/create/` - Create emergency
- `GET /api/emergencies/{id}/` - Emergency details

### Real-time Tracking
- `WebSocket /ws/tracking/` - Live ambulance tracking
- `GET /api/tracking/` - Tracking history

## 🛡️ Security & Privacy

- **End-to-end Encryption**: All patient data is encrypted
- **HIPAA Compliant**: Healthcare data protection standards
- **GDPR Compliant**: European privacy regulations
- **Role-based Access**: Different permissions for users, crew, dispatchers
- **Secure Authentication**: OAuth 2.0 with major providers

## 🌍 Multi-language Support

The application supports multiple languages for wider accessibility:
- English (default)
- Spanish
- French
- German
- Portuguese
- More languages can be added easily

## 📊 Performance & Scalability

- **Low Latency**: Optimized for sub-second response times
- **Scalable Backend**: Handle thousands of simultaneous requests
- **Efficient Database**: PostGIS for optimized geospatial queries
- **CDN Ready**: Static assets optimized for global delivery
- **Caching**: Redis for session and data caching

## 🔧 Development

### Troubleshooting

#### Database Issues
If you encounter migration or database errors:

```bash
# Remove existing database and start fresh
rm backend/db.sqlite3

# Create migrations in correct order (authentication first due to custom user model)
python manage.py makemigrations authentication ambulances emergencies tracking notifications hospitals

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

#### GIS Support (Future Enhancement)
Currently, GIS features are commented out for easier setup. To enable full geospatial functionality:

1. Install spatial libraries:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install gdal-bin libgdal-dev
   sudo apt-get install libgeos-dev
   sudo apt-get install libproj-dev libproj-dev
   sudo apt-get install libspatialite-dev spatialite-bin
   ```

2. Uncomment GIS-related code in models and admin files
3. Update database settings to use spatial backend
4. Create new migrations for field type changes

### Project Structure
```
EMS/
├── backend/           # Django backend
│   ├── ems_project/   # Main Django project
│   └── apps/          # Django applications
├── frontend/          # React web application
├── mobile/            # Flutter mobile app
├── docker-compose.yml # Docker services
└── README.md          # This file
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Emergency Contacts

For immediate emergencies, always call your local emergency services:
- USA: 911
- Europe: 112
- UK: 999

This application is designed to supplement, not replace, traditional emergency services.

## 📧 Support

For technical support or questions, please contact:
- Email: support@ems-system.com
- GitHub Issues: [Create an issue](https://github.com/morganmwenda/EMS/issues)

---

**⚠️ Important**: This is a demonstration emergency management system. For production use, ensure compliance with local healthcare regulations and emergency service protocols.
