# 🔍 LOAF - Lost & Found Platform

> **Never lose track of your belongings again**

A modern, full-stack lost and found management system designed for campuses and communities. LOAF connects people who've lost items with those who've found them through intelligent matching, real-time chat, and AI-powered image recognition.

[![Django](https://img.shields.io/badge/Django-6.0-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16-red.svg)](https://www.django-rest-framework.org/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3.0-blue.svg)](https://tailwindcss.com/)

---

## ✨ Features

### 🎯 Core Functionality
- **Smart Item Reporting** - Report lost or found items with detailed descriptions, photos, and location data
- **Intelligent Matching** - Automated matching algorithm connects lost items with found items
- **Real-time Chat** - Built-in messaging system for secure communication between users
- **Image Recognition** - AI-powered visual search to match items by appearance
- **Admin Dashboard** - Comprehensive management panel for platform administrators

### 🛡️ Security & Auth
- JWT-based authentication with refresh token rotation
- Role-based access control (User, Staff, Admin)
- Secure file uploads with validation
- CORS-protected API endpoints

### 🎨 User Experience
- Responsive, mobile-first design
- Dark/light theme toggle
- Floating navigation dock with smooth animations
- Real-time notifications
- Advanced search and filtering

---

## 🏗️ Tech Stack

### Backend
- **Django 6.0** - Web framework
- **Django REST Framework** - RESTful API
- **SQLite** - Database (easily swappable)
- **Pillow** - Image processing
- **JWT** - Authentication

### Frontend
- **Vanilla JavaScript** - No framework dependencies
- **TailwindCSS** - Utility-first styling
- **Modern CSS** - Custom properties, animations, backdrop filters

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
# Navigate to frontend/pages in your browser
# Example: file:///path/to/frontend/pages/index.html
# Or serve via local server on port 8000
```

The API will be available at `http://localhost:8000/api/`

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
```

---

## 🎨 UI Components

The frontend features a modern, glassmorphic design with:
- **Floating Dock Navigation** - macOS-inspired navigation bar
- **Theme System** - Smooth dark/light mode transitions
- **Responsive Grid** - Mobile-first, adaptive layouts
- **Custom Animations** - Smooth transitions and micro-interactions
- **Professional Color Scheme** - Deep blue palette with cyan accents

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
python manage.py test
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

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

<div align="center">
  
**Made with ❤️ for communities everywhere**

⭐ Star this repo if you find it helpful!

</div>
