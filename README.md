# SnapLink - URL Shortener API 🔗

A production-ready URL shortening service built with Django REST Framework, Redis caching, and Docker.

## 🚀 Live Demo
Base URL: `https://snaplink.onrender.com` *(coming soon)*

## ✨ Features
- JWT Authentication (register/login)
- Create short URLs with auto-generated codes
- Redirect with 302 status
- Click analytics (IP, device type, timestamp)
- Redis caching for high-speed redirects
- Django Admin panel
- Docker containerization
- MySQL database

## 🛠️ Tech Stack
- **Backend:** Python, Django, Django REST Framework
- **Database:** MySQL
- **Caching:** Redis
- **Auth:** JWT (SimpleJWT)
- **Container:** Docker, Docker Compose
- **Deployment:** Render

## 📋 API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/register/` | Register new user | No |
| POST | `/api/auth/login/` | Get JWT token | No |
| POST | `/api/auth/token/refresh/` | Refresh token | No |
| POST | `/api/auth/shorten/` | Create short URL | Yes |
| GET | `/<short_code>/` | Redirect to original URL | No |
| GET | `/api/auth/analytics/<short_code>/` | Get click analytics | Yes |

## 🏃 Quick Start

### Run Locally
```bash
git clone https://github.com/dhivyanrrd/snaplink.git
cd snaplink

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

cd snaplink
python manage.py migrate
python manage.py runserver
```

### Run with Docker
```bash
git clone https://github.com/dhivyanrrd/snaplink.git
cd snaplink
docker-compose up --build
```

## 📊 Sample API Calls

### Register
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"test1234","email":"test@gmail.com"}'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"test1234"}'
```

### Create Short URL
```bash
curl -X POST http://localhost:8000/api/auth/shorten/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"original_url":"https://www.google.com"}'
```

### Get Analytics
```bash
curl -X GET http://localhost:8000/api/auth/analytics/<short_code>/ \
  -H "Authorization: Bearer <your_token>"
```

## ⚡ Performance
- Redis caching reduces redirect response time significantly
- Cache hit: ~1ms vs Database query: ~150ms

## 👤 Author
Dhivyan R  
[LinkedIn](https://linkedin.com/in/dhivyan-rd) | [GitHub](https://github.com/dhivyanrrd)
