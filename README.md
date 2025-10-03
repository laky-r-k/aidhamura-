🌐 AIDHAMURA

Architecting the Digital Frontier.
A real-time chat application and tech collective platform built with Django Channels.

🔗 Live Site: https://aidhamura-app.onrender.com


✨ Overview

AIDHAMURA is a full-featured web application designed as a hub for modern tech collectives.
It combines real-time messaging, social connections, and scalable deployment to create a production-ready digital space.

🔑 Key Features

💬 Real-Time Chat — Instant messaging powered by Django Channels + WebSockets

🔐 Authentication & Security with django-allauth:

Username / Email login

Secure Google OAuth 2.0 login

Mandatory email verification

Password reset & change flows

👤 User Profiles & Friends — Profile pictures, bios, and a working friends list

🔎 Global Search — Quickly discover and connect with other users

☁️ Cloud Media Storage — Profile pictures and uploads stored via Cloudinary CDN

🚀 Production-Ready Deployment — Preconfigured for Render with PostgreSQL, Gunicorn & Uvicorn

🛠️ Tech Stack

Backend: Python, Django, Django Channels
Frontend: HTML, TailwindCSS, Alpine.js
Database: PostgreSQL (prod) | SQLite (dev)
Real-Time Server: Daphne, Uvicorn
Deployment: Render + Gunicorn
Services:

Cloudinary → Media Storage

SendGrid → Transactional Emails

⚡ Getting Started (Local Development)
1️⃣ Prerequisites

Python 3.10+

Git

A code editor (VS Code recommended)

2️⃣ Clone the Repository
git clone https://github.com/laky-r-k/aidhamura-.git
cd aidhamura-

3️⃣ Set Up Virtual Environment
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# .\venv\Scripts\activate  # Windows

4️⃣ Install Dependencies
pip install -r requirements.txt

5️⃣ Configure Environment Variables

Create a .env file in the project root:

# --- SECURITY ---
SECRET_KEY=your_django_secret_key

# --- EMAIL (SendGrid) ---
SENDGRID_API_KEY=your_sendgrid_api_key
DEFAULT_FROM_EMAIL=your_verified_email@example.com

# --- DATABASE ---
DATABASE_URL=   # Leave blank to use SQLite locally

# --- DEBUG & HOSTS ---
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# --- CLOUDINARY ---
CLOUDINARY_URL=cloudinary://<API_KEY>:<API_SECRET>@<CLOUD_NAME>

6️⃣ Run Migrations
python manage.py migrate

7️⃣ Create Superuser
python manage.py createsuperuser

8️⃣ Start Development Server
python manage.py runserver


App available at 👉 http://127.0.0.1:8000/

☁️ Deployment on Render

This project is fully configured for deployment on Render.

Required Environment Variables

SECRET_KEY

DATABASE_URL (auto-provided by Render DB)

ALLOWED_HOSTS=aidhamura-app.onrender.com

PYTHON_VERSION

SENDGRID_API_KEY

DEFAULT_FROM_EMAIL

CLOUDINARY_URL

SITE_DOMAIN=aidhamura-app.onrender.com

Auto Superuser & Site Creation

To simplify first-time setup, migrations auto-create:

A superuser

The correct Django Sites domain

Set these on Render before first deploy:

ADMIN_USER (e.g., admin)

ADMIN_EMAIL

ADMIN_PASS

These run once on initial migration, and safely skip on future deployments.

🤝 Contributing

Contributions are welcome!

Fork the repo

Create a feature branch

Open a pull request 🚀

📜 License

This project is licensed under the MIT License.

⚡ AIDHAMURA: Building the future of collective digital communities.
🔗 Live Site: https://aidhamura-app.onrender.com
