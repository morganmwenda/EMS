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

### Quick Start for Developers

**One-minute setup:**
```bash
# Clone and setup backend
git clone https://github.com/morganmwenda/EMS.git
cd EMS/backend
python -m venv venv && source venv/bin/activate
pip install -r ../requirements.txt
python manage.py makemigrations authentication ambulances emergencies tracking notifications hospitals
python manage.py migrate
python manage.py createsuperuser

# In another terminal - setup frontend  
cd EMS/frontend
npm install && npm start

# Backend will run on http://localhost:8000
# Frontend will run on http://localhost:3000
```

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
# Note: You may see deprecation warnings - these are common in React projects and generally safe to ignore for development
npm start
# Note: "development build is not optimized" message is normal - this is for development with debugging features
# The app will be available at http://localhost:3000
```

#### Mobile Setup
```bash
cd mobile
flutter pub get
flutter run
```

### Running Both Frontend and Backend Together

#### Option 1: Using Multiple Terminals (Recommended for Development)

**Terminal 1 - Django Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python manage.py runserver
# Backend will be available at http://localhost:8000
```

**Terminal 2 - React Frontend:**
```bash
cd frontend
npm start
# Frontend will be available at http://localhost:3000
```

#### Option 2: Using Process Managers

**Using concurrently (install globally):**
```bash
npm install -g concurrently
cd EMS  # project root
concurrently "cd backend && source venv/bin/activate && python manage.py runserver" "cd frontend && npm start"
```

#### Accessing the Applications
- **Web App**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin
- **API Documentation**: http://localhost:8000/api/ (REST browsable API)

#### Verifying Connection
1. Open http://localhost:3000 in your browser
2. Check the API Connection Status widget in the top-right corner
3. All three APIs (Emergencies, Ambulances, Hospitals) should show "✅ Connected"
4. Visit the Dashboard page to see live data from the backend

## � Frontend-Backend Integration

### API Configuration
The React frontend is configured to communicate with the Django backend through:

- **Base URL**: `http://localhost:8000` (development)
- **CORS Enabled**: Cross-origin requests allowed from `http://localhost:3000`
- **Authentication**: Token-based authentication ready
- **Error Handling**: Comprehensive error handling and loading states

### Environment Variables
Create a `.env` file in the frontend directory for custom configuration:

```bash
# frontend/.env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_APP_NAME=Emergency Management System
```

### Backend Configuration
The Django backend includes:

- **Django REST Framework**: For API development
- **CORS Headers**: Allowing frontend requests
- **JSON Responses**: All endpoints return JSON data
- **Sample Data**: Test data for development

## �📱 API Endpoints

### Authentication  
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile
- `POST /api/auth/emergency-sos/` - Emergency SOS dispatch

### Ambulances
- `GET /api/ambulances/` - List all ambulances with status
- `GET /api/ambulances/nearest/?lat=<lat>&lng=<lng>` - Find nearest ambulance
- `GET /api/ambulances/{id}/` - Get ambulance details
- `POST /api/ambulances/{id}/location/` - Update ambulance location

### Emergencies
- `GET /api/emergencies/` - List all emergencies
- `POST /api/emergencies/create/` - Create new emergency
- `GET /api/emergencies/{id}/` - Get emergency details
- `PUT /api/emergencies/{id}/update/` - Update emergency status
- `POST /api/emergencies/{id}/dispatch/` - Dispatch ambulance to emergency
- `GET /api/emergencies/types/` - Get emergency types

### Hospitals
- `GET /api/hospitals/` - List all hospitals with bed availability

### Real-time Tracking
- `GET /api/tracking/` - Get tracking data
- `WebSocket /ws/tracking/` - Live ambulance tracking (future feature)

### API Response Format
All API endpoints return JSON in this format:
```json
{
  "status": "success",
  "count": 2,
  "results": [...]
}
```

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

#### Frontend Dependencies
If you encounter npm warnings or vulnerabilities:

```bash
# Check for security vulnerabilities
npm audit

# Fix automatically fixable vulnerabilities (may not fix all issues)
npm audit fix

# Note: Some vulnerabilities may require breaking changes to fix
# For development, these are generally safe to ignore
# The application will still function properly

# For production deployment, consider:
# 1. Updating to latest React version
# 2. Using npm audit fix --force (test thoroughly after)
# 3. Implementing security headers and proper deployment practices
```

#### Production Build
When ready to deploy to production:

```bash
# Create optimized production build
npm run build

# The build folder will contain optimized files for deployment
# Serve with any static file server (nginx, Apache, etc.)
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

## 🚀 Production Deployment

### Backend Deployment (Django)

#### Using Docker (Recommended)
```bash
# Build and run with docker-compose
docker-compose up -d

# Or build manually
docker build -t ems-backend ./backend
docker run -p 8000:8000 ems-backend
```

#### Manual Deployment
```bash
# Install production dependencies
pip install gunicorn
pip install whitenoise

# Collect static files
python manage.py collectstatic

# Run with Gunicorn
gunicorn ems_project.wsgi:application --bind 0.0.0.0:8000
```

#### Environment Configuration for Production
Create `backend/.env` file:
```bash
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:password@host:port/dbname

# CORS settings for production
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Frontend Deployment (React)

#### Build for Production
```bash
cd frontend
npm run build
# Creates optimized build in 'build' folder
```

#### Deploy to Static Hosting
```bash
# Deploy to services like:
# - Netlify: drag & drop build folder
# - Vercel: connect GitHub repo
# - AWS S3: upload build folder
# - GitHub Pages: configure in repo settings
```

#### Environment Configuration for Production
Create `frontend/.env.production`:
```bash
REACT_APP_API_URL=https://your-api-domain.com
REACT_APP_APP_NAME=Emergency Management System
```

### Production Considerations

#### Security
- Change Django `SECRET_KEY` for production
- Set `DEBUG=False` in Django settings
- Use HTTPS for all communications
- Configure proper CORS origins
- Set up rate limiting for APIs
- Enable Django security middleware

#### Database
- Use PostgreSQL instead of SQLite for production
- Set up database backups
- Configure connection pooling
- Enable database SSL connections

#### Monitoring & Logging
- Configure Django logging
- Set up error tracking (Sentry, etc.)
- Monitor API performance
- Set up health checks

#### Scaling
- Use load balancers for multiple instances
- Configure Redis for session storage
- Set up CDN for static files
- Implement database read replicas

### Production URLs Structure
```
Frontend:  https://ems.yourdomain.com
Backend:   https://api.yourdomain.com
Admin:     https://api.yourdomain.com/admin
```

4. Create new migrations for field type changes

#### Testing API Connection
Test the connection between frontend and backend:

```bash
# Test backend API directly
curl http://localhost:8000/api/emergencies/
curl http://localhost:8000/api/ambulances/
curl http://localhost:8000/api/hospitals/

# Check CORS headers
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: GET" \
     -X OPTIONS http://localhost:8000/api/emergencies/
```

#### Common Issues & Solutions

**CORS Errors:**
- Ensure `corsheaders` is installed: `pip install django-cors-headers`
- Check `CORS_ALLOWED_ORIGINS` in Django settings
- Verify frontend URL is correct in CORS settings

**API Connection Failures:**
- Confirm Django server is running on port 8000
- Check React is configured to call `http://localhost:8000`
- Verify firewall isn't blocking connections

**Database Issues:**
- Run migrations: `python manage.py migrate`
- Create superuser: `python manage.py createsuperuser`
- Check database file exists: `ls backend/db.sqlite3`

**Frontend Build Issues:**
- Clear node_modules: `rm -rf node_modules && npm install`
- Check for syntax errors in console
- Verify all imports are correct

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
