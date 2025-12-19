# 🔍 LOAF - Lost & Found Platform

> **Never lose track of your belongings again**

A modern, full-stack lost and found management system designed for campuses, universities, and communities. LOAF connects people who've lost items with those who've found them through intelligent matching, real-time chat, AI-powered image recognition, and advanced filtering capabilities.

[![Django](https://img.shields.io/badge/Django-6.0-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16-red.svg)](https://www.django-rest-framework.org/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3.0-blue.svg)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## ✨ Features

### 🎯 Core Functionality
- **Smart Item Reporting** - Report lost or found items with detailed descriptions, photos, location data, and categorization
- **Intelligent Matching** - Automated matching algorithm with confidence scoring connects lost items with found items
- **Real-time Chat** - Built-in messaging system for secure, direct communication between users
- **Image Recognition** - AI-powered visual search to match items by appearance
- **Advanced Filtering** - Filter by category, status, date range, and keywords for precise search results
- **Date Range Search** - Quick filter presets (Today, Last 7 Days, Last 30 Days) and custom date range selection
- **Admin Dashboard** - Comprehensive management panel with analytics and user administration
- **User Dashboard** - Personal dashboard for managing reports, matches, and notifications

### 🛡️ Security & Auth
- JWT-based authentication with refresh token rotation
- Role-based access control (User, Staff, Admin)
- Secure file uploads with validation and size limits
- CORS-protected API endpoints
- Permission-based API access control

### 🎨 User Experience
- Fully responsive, mobile-first design
- **Smooth Dark/Light Theme** - System-wide theme toggle with persistent preferences
- Floating navigation dock with smooth animations and hover effects
- Real-time notifications with unread indicators
- Advanced search with multiple filter combinations
- Glassmorphic UI design with backdrop blur effects
- Professional color scheme with accessibility considerations
- Empty states and loading indicators for better UX

---

## 🏗️ Tech Stack

### Backend
- **Django 6.0** - Web framework
- **Django REST Framework** - RESTful API
- **SQLite** - Database (easily swappable)
- **Pillow** - Image processing
- **JWT** - Authentication

### Frontend
- **Vanilla JavaScript** - No framework dependencies, modular architecture
- **TailwindCSS** - Utility-first styling with custom configuration
- **Modern CSS** - Custom properties, animations, backdrop filters, and glassmorphism
- **Responsive Design** - Mobile-first approach with breakpoints for all screen sizes
- **Theme System** - CSS-based dark/light mode with localStorage persistence

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip
- Modern web browser

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/G-alileo/lost_and_found_project.git
cd lost_and_found_project
```

2. **Set up the backend**
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

3. **Run the development server**
```bash
python manage.py runserver
```

4. **Open the frontend**
```bash
# Open frontend/pages/index.html in your browser
# For best experience, serve via Python's HTTP server:
cd ../frontend/pages
python -m http.server 8080
# Then visit http://localhost:8080
```

The API will be available at `http://localhost:8000/api/`

### Default Admin Credentials
After creating a superuser, you can access the admin panel at:
- **Admin Panel**: `http://localhost:8000/admin/`
- **Admin Dashboard**: Open `frontend/pages/admin-dashboard.html` with admin credentials

---

## 📁 Project Structure

```
lost_and_found_project/
├── backend/
│   ├── config/              # Project settings & URLs
│   ├── users/               # User authentication & profiles
│   ├── items/               # Lost/found item management
│   ├── matches/             # Matching algorithm & services
│   ├── chat/                # Real-time messaging
│   ├── notifications/       # User notifications
│   ├── reports/             # Reporting & analytics
│   ├── image_recognition/   # AI visual search
│   ├── adminpanel/          # Admin dashboard APIs
│   └── chatbot/             # Automated assistance
│
└── frontend/
    ├── pages/               # HTML pages
    ├── js/                  # JavaScript modules
    ├── css/                 # Stylesheets
    └── assets/              # Images & media
```

---

## 🔑 API Endpoints

### Authentication
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

### Matches
```
GET    /api/matches/                  # List matches
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

### Notifications
```
GET    /api/notifications/            # List user notifications
POST   /api/notifications/{id}/read/  # Mark notification as read
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
