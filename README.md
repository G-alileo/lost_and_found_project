# 🔍 LOAF - Lost & Found Platform

> **Reuniting people with their lost belongings through intelligent technology**

A modern, full-stack lost and found management system designed for campuses, universities, and communities. LOAF leverages intelligent matching algorithms, real-time communication, and advanced filtering to connect people who've lost items with those who've found them.

[![Django](https://img.shields.io/badge/Django-6.0-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16+-red.svg)](https://www.django-rest-framework.org/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3.0-blue.svg)](https://tailwindcss.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 📋 Table of Contents

- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [UI Components & Pages](#-ui-components--pages)
- [Configuration](#-configuration)
- [Testing](#-testing)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)
- [Changelog](#-changelog)

---

## ✨ Key Features

### 🎯 Core Functionality
- **Smart Item Reporting** - Submit lost or found item reports with detailed descriptions, photo uploads, location data, and category tagging
- **Intelligent Matching Engine** - Automated matching algorithm analyzes attributes and generates confidence scores to connect lost items with found items
- **Real-time Messaging** - Built-in chat system enables secure, direct communication between users without exposing personal contact information
- **Advanced Search & Filtering** - Multi-dimensional filtering by category, status, date range, location, and keywords
- **Date Range Search** - Quick filter presets (Today, Last 7 Days, Last 30 Days, Custom Range) for efficient temporal searching
- **Admin Dashboard** - Comprehensive management panel featuring analytics, user administration, report moderation, and system monitoring
- **User Dashboard** - Personalized interface for managing reports, viewing matches, tracking notifications, and communication history

### 🛡️ Security & Authentication
- **JWT Authentication** - Token-based auth with access/refresh token rotation and automatic expiration
- **Role-Based Access Control** - Granular permissions for Student, Staff, and Admin roles
- **Secure File Uploads** - File type validation, size limits, and sanitization to prevent malicious uploads
- **CORS Protection** - Configured Cross-Origin Resource Sharing for secure API access
- **Permission Guards** - Fine-grained API endpoint protection based on user roles and ownership
- **Password Security** - Hashed passwords using Django's PBKDF2 algorithm with salt

### 🎨 User Experience
- **Fully Responsive Design** - Mobile-first approach optimized for all screen sizes and devices
- **Dark/Light Theme** - System-wide theme toggle with localStorage persistence and smooth transitions
- **Floating Navigation Dock** - macOS-inspired dock with smooth animations, hover effects, and intuitive iconography
- **Real-time Notifications** - Live updates with unread indicators and notification badges
- **Glassmorphic UI** - Modern design language featuring backdrop blur, transparency, and depth
- **Accessible Design** - WCAG-compliant color contrast, keyboard navigation, and screen reader support
- **Contextual Empty States** - User-friendly messages with actionable guidance when no data is present
- **Loading Indicators** - Skeleton screens and progress indicators for improved perceived performance

---

## 🛠 Technology Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Django 6.0** | High-level Python web framework |
| **Django REST Framework 3.16** | RESTful API toolkit |
| **SQLite** | Lightweight database (PostgreSQL/MySQL for production) |
| **Pillow** | Image processing and manipulation |
| **djangorestframework-simplejwt** | JWT authentication |
| **django-cors-headers** | CORS handling for cross-origin requests |
| **Python 3.10+** | Modern Python features |

### Frontend
| Technology | Purpose |
|------------|---------|
| **Vanilla JavaScript (ES6+)** | Zero dependencies, modular architecture |
| **TailwindCSS** | Utility-first CSS framework |
| **Axios** | HTTP client for API communication |
| **Modern CSS** | Grid, Flexbox, animations, backdrop filters |

### Development Tools
| Tool | Purpose |
|------|---------|
| **Git** | Version control |
| **pip** | Python package management |
| **Live Server** | Frontend development server |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/G-alileo/lost_and_found_project.git
   cd lost_and_found_project
   ```

2. **Set up Python virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Load initial data (optional)**
   ```bash
   python manage.py loaddata items/fixtures/categories.json
   ```

6. **Create superuser (for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the backend server**
   ```bash
   python manage.py runserver
   ```

8. **Start the frontend** (in a new terminal)
   ```bash
   cd frontend
   # Using Python's built-in server
   python -m http.server 8080
   
   # Or use VS Code Live Server extension
   ```

### Access Points
| Service | URL |
|---------|-----|
| Backend API | `http://localhost:8000/api/` |
| Django Admin | `http://localhost:8000/admin/` |
| Frontend App | `http://localhost:8080/pages/` |

---

## 📁 Project Structure

```
lost_and_found_project/
├── backend/                    # Django backend application
│   ├── config/                 # Project configuration
│   │   ├── settings.py         # Django settings
│   │   ├── urls.py             # Root URL configuration
│   │   └── wsgi.py             # WSGI deployment config
│   ├── users/                  # User authentication & profiles
│   │   ├── models.py           # Custom User model
│   │   ├── serializers.py      # API serializers
│   │   ├── views.py            # Auth & profile endpoints
│   │   └── permissions.py      # Custom permissions
│   ├── items/                  # Category management
│   │   ├── models.py           # Category & SubCategory models
│   │   ├── serializers.py      # Item serializers
│   │   └── fixtures/           # Initial data (categories)
│   ├── reports/                # Lost & Found reports
│   │   ├── models.py           # Report model
│   │   ├── serializers.py      # Report serializers
│   │   ├── views.py            # CRUD operations
│   │   └── dashboard_views.py  # Dashboard statistics
│   ├── matches/                # Intelligent matching system
│   │   ├── models.py           # Match model
│   │   ├── services.py         # Matching algorithm
│   │   └── views.py            # Match endpoints
│   ├── chat/                   # Real-time messaging
│   │   ├── models.py           # Conversation & Message models
│   │   ├── serializers.py      # Chat serializers
│   │   └── views.py            # Chat endpoints
│   ├── notifications/          # User notifications
│   │   ├── models.py           # Notification model
│   │   └── views.py            # Notification endpoints
│   ├── adminpanel/             # Admin statistics
│   │   └── views.py            # Admin stats endpoints
│   ├── image_recognition/      # Image matching (placeholder)
│   │   ├── models.py           # ImageMatchLog model
│   │   └── views.py            # Image endpoints
│   └── media/                  # Uploaded files
│       └── reports/            # Report images
│
├── frontend/                   # Frontend application
│   ├── pages/                  # HTML pages
│   │   ├── index.html          # Landing page
│   │   ├── browse.html         # Search & browse items
│   │   ├── report-lost.html    # Report lost item form
│   │   ├── report-found.html   # Report found item form
│   │   ├── user-dashboard.html # User dashboard
│   │   ├── admin-dashboard.html# Admin dashboard
│   │   ├── messages.html       # Chat interface
│   │   ├── login.html          # Login page
│   │   └── register.html       # Registration page
│   ├── js/                     # JavaScript modules
│   │   ├── api.js              # API client & authentication
│   │   ├── auth.js             # Authentication handlers
│   │   ├── dashboard.js        # Dashboard functionality
│   │   ├── chat.js             # Chat functionality
│   │   ├── reports.js          # Report management
│   │   ├── admin.js            # Admin functionality
│   │   ├── theme.js            # Theme toggle
│   │   └── ui.js               # UI components
│   ├── css/                    # Stylesheets
│   │   └── custom-styles.css   # Custom styles
│   └── assets/                 # Static assets
│       └── favicon/            # Favicon files
│
└── README.md                   # Project documentation
```

---

## 📡 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/auth/register/` | Register new user | No |
| `POST` | `/api/auth/token/` | Login & get JWT tokens | No |
| `POST` | `/api/auth/token/refresh/` | Refresh access token | No |
| `GET` | `/api/users/me/` | Get current user profile | Yes |
| `PUT/PATCH` | `/api/users/me/` | Update user profile | Yes |
| `POST` | `/api/users/change-password/` | Change password | Yes |

### Report Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/reports/` | List all reports (with filters) | No |
| `POST` | `/api/reports/` | Create new report | Yes |
| `GET` | `/api/reports/{id}/` | Get report details | No |
| `PUT/PATCH` | `/api/reports/{id}/` | Update report (owner only) | Yes |
| `DELETE` | `/api/reports/{id}/` | Delete report (owner/admin) | Yes |

### Category Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/categories/` | List all categories | No |
| `POST` | `/api/categories/` | Create category | Admin |
| `GET` | `/api/subcategories/` | List subcategories | No |

### Match Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/matches/` | List user's matches | Yes |
| `GET` | `/api/matches/{id}/` | Get match details | Yes |
| `POST` | `/api/matches/{id}/confirm/` | Confirm match | Yes |
| `POST` | `/api/matches/{id}/reject/` | Reject match | Yes |

### Chat Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/chat/conversations/` | List user conversations | Yes |
| `POST` | `/api/chat/conversations/` | Start new conversation | Yes |
| `GET` | `/api/chat/conversations/{id}/messages/` | Get messages | Yes |
| `POST` | `/api/chat/conversations/{id}/send_message/` | Send message | Yes |
| `GET` | `/api/chat/conversations/unread_count/` | Get unread count | Yes |

### Dashboard Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/dashboard/stats/` | User dashboard statistics | Yes |
| `GET` | `/api/dashboard/reports/` | User's reports | Yes |
| `GET` | `/api/dashboard/matches/` | User's matches | Yes |
| `GET` | `/api/dashboard/notifications/` | User's notifications | Yes |
| `GET` | `/api/admin/stats/` | Admin statistics | Admin |

### Notification Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/notifications/` | List notifications | Yes |
| `POST` | `/api/notifications/{id}/mark-read/` | Mark as read | Yes |

### Query Parameters for Filtering

```bash
# Filter by report type
GET /api/reports/?type=lost
GET /api/reports/?type=found

# Filter by category
GET /api/reports/?category=1

# Filter by status
GET /api/reports/?status=pending

# Search in title, description, location
GET /api/reports/?q=iPhone

# Date range filtering
GET /api/reports/?created_at__date__gte=2025-01-01
GET /api/reports/?created_at__date__lte=2025-12-31

# Combined filters
GET /api/reports/?type=lost&category=1&q=phone
```

---

## 🎨 UI Components & Pages

### Pages Overview

| Page | Description |
|------|-------------|
| `index.html` | Landing page with hero section and features showcase |
| `browse.html` | Advanced search and filtering interface with date range support |
| `report-lost.html` | Form for reporting lost items with image upload |
| `report-found.html` | Form for reporting found items with image upload |
| `user-dashboard.html` | Personal dashboard with reports, matches, and notifications |
| `admin-dashboard.html` | Administrative panel with analytics and user management |
| `messages.html` | Real-time chat interface for user communications |
| `login.html` | User authentication page |
| `register.html` | New user registration page |

### Design Features

- **Floating Dock Navigation** - macOS-inspired navigation bar with smooth animations
- **Theme System** - Complete dark/light mode with system-wide consistency
- **Responsive Grid** - Mobile-first, adaptive layouts for all screen sizes
- **Custom Animations** - Smooth transitions, hover effects, and micro-interactions
- **Professional Color Scheme** - Deep blue palette with cyan accents
- **Glass Effect Cards** - Backdrop blur and translucent backgrounds
- **Status Badges** - Color-coded badges for lost/found/pending/confirmed states
- **Empty States** - User-friendly messages when no data is available

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Django Core Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (default: SQLite)
DATABASE_URL=sqlite:///db.sqlite3

# JWT Settings (optional - defaults in settings.py)
JWT_ACCESS_TOKEN_LIFETIME=120  # minutes
JWT_REFRESH_TOKEN_LIFETIME=7   # days

# Matching Algorithm Configuration
MATCHING_CONF_THRESHOLD=0.35
MATCHING_DATE_WINDOW_DAYS=14
MATCHING_WEIGHT_CATEGORY=0.6
MATCHING_WEIGHT_KEYWORD=0.4
MATCHING_WEIGHT_DATE_BOOST=0.05
```

### Database Configuration

**Development (Default):** SQLite - Zero configuration required

**Production (PostgreSQL):**
```python
# In backend/config/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'loaf_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 🧪 Testing

```bash
cd backend

# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test users
python manage.py test reports
python manage.py test matches
python manage.py test chat
python manage.py test notifications

# Run with verbose output
python manage.py test --verbosity=2

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 🚧 Future Enhancements

### Short-term (v1.2 - v1.3)
- [ ] Email notifications for matches and messages
- [ ] QR code generation for found items
- [ ] Enhanced image recognition with AI
- [ ] Saved search preferences
- [ ] User reputation system

### Mid-term (v1.4 - v2.0)
- [ ] Mobile applications (React Native/Flutter)
- [ ] WebSocket support for real-time updates
- [ ] Multi-language support (i18n)
- [ ] Social media integration
- [ ] SMS notifications
- [ ] Progressive Web App (PWA) features

### Long-term (v2.0+)
- [ ] Advanced AI image recognition with TensorFlow/PyTorch
- [ ] Geolocation-based search radius and mapping
- [ ] Item claim verification system
- [ ] Integration with campus security systems

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Coding Standards
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Write tests for new features
- Update documentation as needed

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👥 Authors

**James Murithi (G-alileo)** - *Creator & Lead Developer* - [@G-alileo](https://github.com/G-alileo)

---

## 🙏 Acknowledgments

- **Django** & **Django REST Framework** communities for excellent documentation
- **TailwindCSS** team for the utility-first CSS framework
- **Pillow** contributors for powerful image processing capabilities
- Open source community for inspiration and tools

---

## 🐛 Known Issues

- Image recognition feature is in active development (placeholder implementation)
- Large image uploads (>5MB) may be slow on mobile networks
- Chat requires manual refresh; WebSocket support planned for v2.0

---

## 📝 Changelog

### Version 1.1.0 (January 2026)
- ✨ **New**: Date range filtering with quick presets (Today, Last 7 Days, Last 30 Days)
- ✨ **New**: Custom date range picker for precise temporal searching
- 🎨 **Improved**: Full dark/light theme support across all pages
- 🎨 **Improved**: Enhanced glassmorphic design with better contrast
- 🔧 **Fixed**: Footer theme inconsistencies
- 🔧 **Fixed**: Mobile responsiveness issues in dashboard views
- 🐛 **Fixed**: Image upload validation edge cases
- 📱 **Enhanced**: Mobile user experience with touch-friendly controls
- 🚀 **Performance**: Optimized API queries and reduced payload sizes

### Version 1.0.0 (December 2025)
- 🎉 **Initial Release**: Core lost and found functionality
- 💬 **Feature**: Real-time chat messaging system
- 🔐 **Feature**: JWT-based authentication with token refresh
- 🔍 **Feature**: Intelligent matching algorithm with confidence scoring
- 📊 **Feature**: Admin dashboard with analytics and user management
- 👤 **Feature**: User dashboard for personal report tracking
- 🎨 **Feature**: Responsive UI with glassmorphic design language
- 🖼️ **Feature**: Image upload and preview capabilities
- 🔔 **Feature**: Notification system for matches and messages

---

<div align="center">
  
**Made with ❤️ for communities everywhere**

⭐ Star this repo if you find it helpful!

[Report Bug](https://github.com/G-alileo/lost_and_found_project/issues) · [Request Feature](https://github.com/G-alileo/lost_and_found_project/issues)

</div>
