AIDHAMURA
Architecting the Digital Frontier. A real-time chat application and tech collective platform built with Django Channels.

AIDHAMURA is a full-featured web application designed as a hub for a modern tech collective. It features a robust, real-time chat system, comprehensive user authentication, and a scalable architecture ready for production deployment.

Live Site: https://aidhamura-app.onrender.com

Key Features
Real-Time Chat: Instant messaging between users, powered by Django Channels and WebSockets.

Comprehensive Authentication: A complete user management system built with django-allauth, including:

Username/Email & Password Registration

Secure "Sign in with Google" (OAuth 2.0)

Mandatory Email Verification

Password Reset ("Forgot Password") and Change flows

User Profiles & Friends System: Customizable user profiles with profile pictures, bios, and a functional friends list.

Global User Search: A navigation bar search to easily find and connect with other members.

Cloud Media Storage: All user-uploaded profile pictures are handled by Cloudinary, ensuring persistence and fast delivery via CDN.

Production-Ready Deployment: Configured for a professional deployment pipeline on Render with PostgreSQL, Gunicorn, and Uvicorn.

Tech Stack
Backend: Python, Django, Django Channels

Frontend: HTML, Tailwind CSS, Alpine.js

Database: PostgreSQL (Production), SQLite3 (Development)

Real-Time Server: Daphne, Uvicorn

Deployment: Render, Gunicorn

Services:

Cloudinary for media storage

SendGrid for transactional emails

🚀 Getting Started (Local Development)
Follow these instructions to set up the project on your local machine for development and testing.

1. Prerequisites
Python 3.10 or higher

Git

A code editor (like VS Code)

2. Clone the Repository
git clone [https://github.com/laky-r-k/aidhamura-.git](https://github.com/laky-r-k/aidhamura-.git)
cd aidhamura-

3. Set Up the Virtual Environment
Create and activate a virtual environment to manage project dependencies.

# Create the virtual environment
python3 -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# Or on Windows
# .\venv\Scripts\activate

4. Install Dependencies
Install all the required Python packages from the requirements.txt file.

pip install -r requirements.txt

5. Configure Environment Variables
The project uses a .env file to manage secret keys for local development.

Create a new file named .env in the root of the project.

Copy the content from the example below and fill in your own secret values.

.env file structure:

# --- SECURITY ---
SECRET_KEY='generate_a_new_django_secret_key'

# --- EMAIL (SendGrid) ---
SENDGRID_API_KEY='your_sendgrid_api_key_here'
DEFAULT_FROM_EMAIL='your_verified_sendgrid_email@example.com'

# --- DATABASE ---
# Keep this blank to use the local SQLite database
DATABASE_URL=

# --- DEBUG & HOSTS ---
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

6. Run Database Migrations
Create the local db.sqlite3 file and set up all the necessary database tables.

python manage.py migrate

7. Create a Local Superuser
To access the Django admin panel, you need to create a local superuser.

python manage.py createsuperuser

Follow the prompts to set up your admin username and password.

8. Run the Development Server
You're all set! Start the local development server.

python manage.py runserver

The application will now be running at http://127.0.0.1:8000/.

☁️ Deployment
This project is configured for deployment on Render. The deployment is automated via the run.sh script. The following environment variables must be set on the Render dashboard for a successful deployment.

Required Environment Variables
SECRET_KEY

DATABASE_URL (provided by Render when you connect the database)

ALLOWED_HOSTS (your live URL, e.g., aidhamura-app.onrender.com)

PYTHON_VERSION

SENDGRID_API_KEY

DEFAULT_FROM_EMAIL

CLOUDINARY_URL

SITE_DOMAIN (for the Django Sites framework, e.g., aidhamura-app.onrender.com)

Automatic Superuser & Site Creation
This project uses Django data migrations to automatically set up the application on the first deployment. This is necessary for platforms like Render that do not have a persistent shell.

To use this feature, you must also set the following environment variables on Render:

ADMIN_USER: The desired username for the admin account (e.g., admin).

ADMIN_EMAIL: The email address for the admin account.

ADMIN_PASS: The secure password for the admin account.

On the first migrate command during deployment, the migrations will read these variables and create the superuser, as well as set up the correct domain for the Django Sites framework. On subsequent deployments, these migrations will see that the data already exists and will safely skip these steps.
