# 🔍 LOAF - Lost & Found Platform

> **Reuniting people with their lost belongings through intelligent technology**

A modern, full-stack lost and found management system designed for campuses, universities, and communities. LOAF leverages intelligent matching algorithms, real-time communication, AI-powered image recognition, and advanced filtering to connect people who've lost items with those who've found them.

[![Django](https://img.shields.io/badge/Django-5.0+-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14+-red.svg)](https://www.django-rest-framework.org/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3.0-blue.svg)](https://tailwindcss.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## ✨ Key Features

### 🎯 Core Functionality
- **Smart Item Reporting** - Submit lost or found item reports with detailed descriptions, multiple photo uploads, location data, and category tagging
- **Intelligent Matching Engine** - Automated matching algorithm analyzes attributes and generates confidence scores to connect lost items with found items
- **Real-time Messaging** - Built-in chat system enables secure, direct communication between users without exposing personal contact information
- **AI Image Recognition** - Computer vision-powered visual search matches items based on appearance and visual similarity
- **Advanced Search & Filtering** - Multi-dimensional filtering by category, status, date range, location, and keywords with saved search preferences
- **Date Range Search** - Quick filter presets (Today, Last 7 Days, Last 30 Days, Custom Range) for efficient temporal searching
- **Admin Dashboard** - Comprehensive management panel featuring analytics, user administration, report moderation, and system monitoring
- **User Dashboard** - Personalized interface for managing reports, viewing matches, tracking notifications, and communication history

### 🛡️ Security & Authentication
- **JWT Authentication** - Token-based auth with access/refresh token rotation and automatic expiration
- **Role-Based Access Control** - Granular permissions for User, Staff, and Admin roles
- **Secure File Uploads** - File type validation, size limits, and sanitization to prevent malicious uploads
- **CORS Protection** - Configured Cross-Origin Resource Sharing for secure API access
- **Permission Guards** - Fine-grained API endpoint protection based on user roles and ownership
- **Password Security** - Hashed passwords using Django's PBKDF2 algorithm with salt

##**Fully Responsive Design** - Mobile-first approach optimized for all screen sizes and devices
- **Dark/Light Theme** - System-wide theme toggle with localStorage persistence and smooth transitions
- **Floating Navigation Dock** - macOS-inspired dock with smooth animations, hover effects, and intuitive iconography
- **Real-time Notifications** - Live updates with unread indicators and notification badges
- **Advanced Search** - Powerful search engine supporting multiple simultaneous filters and saved searches
- **Glassmorphic UI** - Modern design language featuring backdrop blur, transparency, and depth
- **Accessible Design** - WCAG-compliant color contrast, keyboard navigation, and screen reader support
- **Contextual Empty States** - User-friendly messages with actionable guidance when no data is present
- **Loading Indicators** - Skeleton screens and progress indicators for improved perceived performanceiderations
- Empty states and loading indicators for better UX

---nology Stack

### Backend
- **Django 5.x** - High-level Python web framework
- **Django REST Framework** - Powerful toolkit for building RESTful APIs
- **SQLite** - Lightweight database (production-ready alternatives: PostgreSQL, MySQL)
- **Pillow** - Python Imaging Library for image processing and manipulation
- **djangorestframework-simplejwt** - JSON Web Token authentication
- **django-cors-headers** - CORS handling for cross-origin requests
- **Python 3.10+** - Modern Python features and performance improvements

### Frontend
- **Vanilla JavaScript (ES6+)** - Zero dependencies, modular architecture, native Web APIs
- **TailwindCSS** - Utility-first CSS framework with custom configuration
- **Modern CSS** - CSS custom properties, Grid, Flexbox, animations, backdrop filters
- **Responsive Design** - Mobile-first approach with breakpoints (sm, md, lg, xl, 2xl)
- **Web Storage API** - localStorage for theme preferences and cached data
- **Fetch API** - Native HTTP client for API communication

### Development Tools
- **Git** - Version control
- **pip** - Python package management
- **Python HTTP Server** - Development frontend serversmorphism
- **Responsive Design** - Mobile-first approach with breakpoints for all screen sizes
- **Theme System** - CSS-based dark/light mode with localStorage persistence

---

## 🚀 Quick Start
   ```bash
   git clone https://github.com/G-alileo/lost_and_found_project.git
   cd lost_and_found_project
   ```

2. **Set up Python virtual environment (recommended)**
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

4. **Configure environment variables**
   ```bash
   # Create .env file (see Configuration section below)
   cp .env.example .env  # If example exists, or create manually
   ```

5. **Run database migrations**
   `Access Points

After setup, you can access:
- **Backend API**: `http://localhost:8000/api/`
- **Django Admin Panel**: `http://localhost:8000/admin/` (use superuser credentials)
- **Frontend Application**: `http://localhost:8080/`
- **API Documentation**: `http://localhost:8000/api/docs/` (if configured)
6. **Load initial data (optional)**
   ```bash
   python manage.py loaddata items/fixtures/categories.json
   ```

7. **Create                     # Django backend application
│   ├── config/                 # Project configuration & root URLs
│   │   ├── settings.py         # Django settings
│   │   ├── urls.py             # Root URL configuration
│   │   └── wsgi.py/asgi.py     # Server deployment configs
│   ├── users/                  # User authentication & profile management
│   │   ├── models.py           # User model extensions
│   │   ├── serializers.py      # API serializers
│   │   ├── views.py            # Auth & profile endpoints
│   │   └── permissions.py      # Custom permission classes
│   ├── items/                  # Lost & found item management
│   │   ├── models.py           # Item model
│   │   ├── serializers.py      # Item serializers
│   │   ├── views.py            # CRUD operations
│   │   └── fixtures/           # Initial data (categories)
│   ├── matches/                # Intelligent matching system
│   │   ├── models.py           # Match model
│   │   ├── services.py         # Matching algorithm
│   │   └── views.py            # Match endpoints
│   ├── chat/                   # Real-time messaging system
│   │   ├── models.py           # Conversation & message models
│   │   ├── serializers.py      # Chat serializers
│   │   └── views.py            # Chat endpoints
│   ├── notifications/          # User notification system
│   │   ├── models.py           # Notification model
│   │   └── views.py            # Notification endpoints
│   ├── reports/                # Analytics & reporting
│   │   ├── models.py           # Report models
│   │   ├── dashboard_views.py  # Dashboard statistics
│   │   ├─Documentation

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/users/register/` | Register new user account | No |
| `POST` | `/api/users/login/` | Login & receive JWT tokens | No |
| `POST` | `/api/users/refresh/` | Refresh access token | Yes (Refresh Token) |
| `GET` | `/api/users/profile/` | Get current user profile | Yes |
| `PATCH` | `/api/users/profile/` | Update user profile | Yes |

### Item Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/items/` | List all items (with filters) | No |
| `POST` | `/api/items/` | Create new item report | Yes |
| `GET` | `/api/items/{id}/` | Get specific item details | No |
| `PATCH` | `/api/items/{id}/` | Update item (owner only) | Yes |
| `DELETE` | `/api/items/{id}/` | Delete item (owner/admin) | Yes |

### Match Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/matches/` | List user's matches | Yes |
| `POST` | `/api/matches/` | Create new match | Yes |
| `GET` | `/api/matches/{id}/` | Get match details | Yes |
| `PATCH` | `/api/matches/{id}/` | Update match status | Yes |

### Chat Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/chat/conversations/` | List user conversations | Yes |
| `POST` | `/api/chat/conversations/` | Start new conversation | Yes |
| `GET` | `/api/chat/messages/{conversation_id}/` | Get conversation messages | Yes |
| `POST` | `/api/chat/messages/` | Send message | Yes |
| `PATCH` | `/api/chat/messages/{id}/read/` | Mark message as read | Yes |

### Report & Analytics Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/reports/` | List reports with filters | Yes (Admin/Staff) |
| `GET` | `/api/reports/stats/` | Dashboard statistics | Yes |
| `GET` | `/api/reports/export/` | Export reports data | Yes (Admin/Staff) |

### Notification Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/notifications/` | List user notifications | Yes |
| `POST` | `/api/notifications/{id}/read/` | Mark notification as read | Yes |
| `DELETE` | `/api/notifications/{id}/` | Delete notification | Yes |

### Query Parameters & Filtering

The items and reports endpoints support extensive filtering via query parameters:

**Common Filters:**
- `?search=keyword` - Full-text search in title and description
- `?category=Electronics` - Filter by category name
- `?status=lost|found` - Filter by item status
- `?date_from=2026-01-01` - Items reported from this date
- `?date_to=2026-12-31` - Items reported until this date
- `?location=Building A` - Filter by location
- `?ordering=-created_at` - Sort results (prefix with `-` for descending)
- `?page=1&page_size=20` - Pagination controls

**Example Requests:**
```bash
# Search for lost electronics from last month
GET /api/items/?status=lost&category=Electronics&date_from=2025-12-01

# Get all items sorted by newest first
GET /api/items/?ordering=-created_at

# Search with keyword
GET /api/items/?search=iPhone%2015
```shboard.html` with admin credentials

---

## 📁 Project Structure


Create a `.env` file in the `backend/` directory:

```env
# Django Core Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DATABASE_URL=sqlite:///db.sqlite3

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=60  # minutes
JWT_REFRESH_TOKEN_LIFETIME=1  # days

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:8080,http://127.0.0.1:8080

# File Upload Settings
MAX_UPLOAD_SIZE=5242880  # 5MB in bytes

# Email Configuration (for notifications)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Database Configuration

**Development (Default):** SQLite - Zero configuration required

**Production:** PostgreSQL or MySQL recommended

**PostgreSQL Setup:**
```bash
# Install psycopg2
pip install psycopg2-binary

# Update .env
DATABASE_URL=postgresql://user:password@localhost:5432/loaf_db
```

**Manual Configuration** (in `backend/config/settings.py`):
```python
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

**MySQL Setup:**
### Running Tests

```bash
cd backend

# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test users
python manage.py test items
python manage.py test matches
python manage.py test chat
python manage.py test notifications

# Run tests with verbose output
python manage.py test --verbosity=2

# Run specific test class or method
python manage.py test users.tests.UserAuthTestCase
python manage.py test users.tests.UserAuthTestCase.test_user_registration
```

### TeRoadmap & Future Enhancements

### 🎯 Planned Features

**Short-term (v1.2 - v1.3)**
- [ ] Email notifications for matches and messages
- [ ] QR code generation for found items
- [ ] Enhanced image recognition with multiple model support
- [ ] Saved search preferences
- [ ] Advanced user reputation system

**Mid-term (v1.4 - v2.0)**
- [ ] Mobile applications (React Native/Flutter)
- [ ] WebSocket support for real-time updates
- [ ] Multi-language support (i18n)
- [ ] Social media integration for sharing found items
- [ ] SMS notifications via Twilio/similar service
- [ ] Progressive Web App (PWA) features

**Long-term (v2.0+)**
- [ ] Advanced AI image recognition with TensorFlow/PyTorch
- [ ] Geolocation-based search radius and mapping
- [ ] Item claim verification with proof requirements
- [ ] Integration with campus security systems
- [ ] Blockchain-based item ownership verification
- [ Development Guidelines

**Coding Standards:**
- Follow PEP 8 for Python code (use `black` and `flake8`)
- Use ESLint configuration for JavaScript
- Write meaningful variable and function names
- Add docstrings for functions and classes
- Comment complex business logic
- Keep functions small and focused

**Git Workflow:**
- Write clear, descriptive commit messages
- Reference issue numbers in commits
- Keep commits atomic and focused
- Rebase before submitting PRs

**Testing Requirements:**
- Write tests for all new features
- Maintain minimum 80% code coverage
- Include both unit and integration tests
- Test edge cases and error handling

**Documentation:**
- Update README for new features
- Add inline code documentation
- Update API documentation
- Include usage exampleswser

# Show missing lines
coverage report --show-missing
```

### Writing Tests

Tests are located in each app's `tests.py` file. Example:

```python
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

class ItemTestCase(APITestCase):
    def test_create_item(self):
        response = self.client.post('/api/items/', data={...})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)deployment, update to your production domain. Authentication
```
POST   /api/users/register/           # User registration
POST   /api/users/login/              # Login & get tokens
POST   /api/users/refresh/            # Refresh access token
GET    /api/users/profile/            # Get user profile
```

### Items
```
GET    /api/items/                    # List all items
POST   /api/items/                    # Create new item
GET    /api/items/{id}/               # Get item details
PATCH  /api/items/{id}/               # Update item
DELETE /api/items/{id}/               # Delete item
```

### Matcheslicensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License
 & Contributors

**James Murithi (G-alileo)** - *Creator & Lead Developer* - [@G-alileo](https://github.com/G-alileo)

See also the list of [contributors](https://github.com/G-alileo/lost_and_found_project/contributors) who participated in this project.
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to**Django** & **Django REST Framework** communities for excellent documentation and support
- **TailwindCSS** team for the utility-first CSS framework
- **Pillow** contributors for powerful image processing capabilities
- Open source community for inspiration and tools
- All contributors who help improve this project
- Beta testers and early adopters for valuable feedbackditions:
 & Contact

### Getting Help

- **📖 Documentation**: Read through this README and inline code documentation
- **🐛 Bug Reports**: [Open an issue](https://github.com/G-alileo/lost_and_found_project/issues/new?template=bug_report.md)
- **💡 Feature Requests**: [Submit your ideas](https://github.com/G-alileo/lost_and_found_project/issues/new?template=feature_request.md)
- **❓ Questions**: Check [existing issues](https://github.com/G-alileo/lost_and_found_project/issues) or open a new discussion
- **🔍 Troubleshooting**: Review [closed issues](https://github.com/G-alileo/lost_and_found_project/issues?q=is%3Aissue+is%3Aclosed) for solutions

### Response Times

- Critical bugs: 24-48 hours
- Feature requests: 1-2 weeks
- General questions: 2-5 days

*Note: This is a community-driven project. Response times may vary.*  # List matches
POST   /api/matches/                  # Create match
GET    /api/matches/{id}/             # Match details
```

### Chat
```
GET    /api/chat/conversations/       # List conversations
POST   /api/chat/conversations/       # Start conversation
GET    /api/chat/messages/{conv_id}/  # Get messages
POST   /api/chat/messages/            # Send message
PATCH  /api/chat/messages/{id}/read/  # Mark message as read
```

### Reports & Analytics
```
GET    /api/reports/                  # List reports (with filtering)
GET    /api/reports/stats/            # Get dashboard statistics
GET    /api/reports/export/           # Export reports data
```
 & Limitations

### Current Known Issues

- **Image Recognition**: Advanced AI features are in active development
- **Mobile Performance**: Large image uploads (>5MB) may be slow on mobile networks
- **Browser Compatibility**: Best experience on Chrome, Firefox, Safari, and Edge (latest versions)
- **Real-time Updates**: Chat requires manual refresh; WebSocket support planned for v2.0

### Limitations
January 2026)
- ✨ **New**: Date range filtering with quick presets (Today, Last 7 Days, Last 30 Days)
- ✨ **New**: Custom date range picker for precise temporal searching
- 🎨 **Improved**: Full dark/light theme support across all pages with smooth transitions
- 🎨 **Improved**: Enhanced glassmorphic design with better contrast and accessibility
- 🔧 **Fixed**: Footer theme inconsistencies across different pages
- 🔧 **Fixed**: Mobile responsiveness issues in dashboard views
- 🐛 **Fixed**: Image upload validation edge cases
- 📱 **Enhanced**: Mobile user experience with touch-friendly controls
- 🚀 **Performance**: Optimized API queries and reduced payload sizes
- 📝 **Docs**: Comprehensive README updates with detailed API documentation

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
- 📱 **Feature**: Mobile-first responsive design

### Coming in v1.2.0
- 📧 Email notification system
- 🔍 Enhanced search with saved preferences
- ⭐ User reputation and rating system
- 📱 Progressive Web App features
5. Console error messageread
```

### Query Parameters for Filtering
The items/reports endpoints support advanced filtering:
- `?category=Electronics` - Filter by category
- `?status=found` - Filter by status (lost/found)
- `?date_from=2025-01-01` - Items reported from this date
- `?date_to=2025-12-31` - Items reported until this date
- `?search=iPhone` - Search in title and description

---

## 🎨 UI Components & Pages

### Pages
- **index.html** - Landing page with hero section and features showcase
- **browse.html** - Advanced search and filtering interface with date range support
- **report-lost.html** - Form for reporting lost items with image upload
- **report-found.html** - Form for reporting found items with image upload
- **user-dashboard.html** - Personal dashboard with reports, matches, and notifications
- **admin-dashboard.html** - Administrative panel with analytics and user management
- **messages.html** - Real-time chat interface for user communications
- **login.html** - User authentication page
- **register.html** - New user registration page

### Design Features
The frontend features a modern, glassmorphic design with:
- **Floating Dock Navigation** - macOS-inspired navigation bar with smooth animations
- **Theme System** - Complete dark/light mode with system-wide consistency
- **Responsive Grid** - Mobile-first, adaptive layouts for all screen sizes
- **Custom Animations** - Smooth transitions, hover effects, and micro-interactions
- **Professional Color Scheme** - Deep blue palette with cyan accents and accessible contrast
- **Glass Effect Cards** - Backdrop blur and translucent backgrounds
- **Status Badges** - Color-coded badges for lost/found/pending/confirmed states
- **Empty States** - User-friendly messages when no data is available

---

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Database
Default: SQLite (for development)

To use PostgreSQL/MySQL:
```python
# Update backend/config/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'loaf_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
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
python manage.py test items
python manage.py test matches
python manage.py test chat

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 🚧 Future Enhancements

- [ ] Email notifications for matches and messages
- [ ] Mobile app (React Native/Flutter)
- [ ] Advanced AI image recognition with TensorFlow
- [ ] Multi-language support
- [ ] Social media integration for sharing
- [ ] QR code generation for found items
- [ ] SMS notifications
- [ ] Geolocation-based search radius
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

**G-alileo** - *Initial work*

---

## 🙏 Acknowledgments

- TailwindCSS for the utility-first CSS framework
- Django community for excellent documentation
- All contributors who help improve this project

---

## 📞 Support

For issues and questions:
- Open an issue on [GitHub](https://github.com/G-alileo/lost_and_found_project/issues)
- Check existing documentation
- Review closed issues for solutions

---

## 🐛 Known Issues

- Date range filtering requires backend server to be running
- Image recognition feature is in development
- Mobile browser performance may vary with large image uploads

---

## 📝 Changelog

### Version 1.1.0 (December 2025)
- ✨ Added date range filtering with quick presets
- 🎨 Implemented full dark/light theme support across all pages
- 🔧 Fixed footer theme inconsistencies
- 🐛 Improved dashboard UI responsiveness
- 📱 Enhanced mobile experience

### Version 1.0.0 (Initial Release)
- 🎉 Core lost and found functionality
- 💬 Real-time chat system
- 🔐 JWT authentication
- 📊 Admin dashboard
- 🎨 Responsive UI with glassmorphic design

---

<div align="center">
  
**Made with ❤️ for communities everywhere**

⭐ Star this repo if you find it helpful!

[Report Bug](https://github.com/G-alileo/lost_and_found_project/issues) · [Request Feature](https://github.com/G-alileo/lost_and_found_project/issues)

</div>
