# FeedbackHub - Web-Based Feedback Collection System

A Django-based feedback collection system for lecturers and students.

## Prerequisites

- Python 3.10+
- XAMPP (MySQL running on port 3306)
- pip (Python package manager)

## Setup Instructions

### 1. Create MySQL Database

Open XAMPP Control Panel, start **Apache** and **MySQL**, then open phpMyAdmin (http://localhost/phpmyadmin) and create a new database:

```sql
CREATE DATABASE feedback_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Create Virtual Environment

```bash
cd feedback_system
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note (Windows):** If `mysqlclient` fails to install, try:
> ```bash
> pip install mysqlclient‑2.2.0‑cp311‑cp311‑win_amd64.whl
> ```
> Or use `pip install PyMySQL` and add this to `feedback_project/__init__.py`:
> ```python
> import pymysql
> pymysql.install_as_MySQLdb()
> ```

### 4. Run Migrations

```bash
python manage.py makemigrations accounts
python manage.py makemigrations feedback
python manage.py migrate
```

### 5. Create Admin Superuser

```bash
python manage.py createsuperuser
```

After creating the superuser, update their role to `admin`:

```bash
python manage.py shell
```
```python
from accounts.models import User
u = User.objects.get(username='your_admin_username')
u.role = 'admin'
u.save()
exit()
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

## Project Structure

```
feedback_system/
├── manage.py
├── requirements.txt
├── feedback_project/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                  # User management app
│   ├── models.py              # Custom User model with roles
│   ├── views.py               # Login, register, dashboards
│   ├── forms.py               # Registration & edit forms
│   ├── decorators.py          # Role-based access decorators
│   ├── urls.py
│   └── templates/accounts/    # Account templates
├── feedback/                  # Feedback & courses app
│   ├── models.py              # Course, Feedback models
│   ├── views.py               # CRUD views
│   ├── forms.py               # Feedback & course forms
│   ├── urls.py
│   └── templates/feedback/    # Feedback templates
├── templates/                 # Base templates
│   ├── base.html
│   └── base_auth.html
└── static/
    ├── css/style.css
    └── js/main.js
```

## User Roles

| Role       | Capabilities                                                    |
|------------|----------------------------------------------------------------|
| **Student**   | Register, login, submit feedback, view own feedback         |
| **Lecturer**  | Login, view received feedback, see ratings & statistics      |
| **Admin**     | Manage users, courses, view/delete all feedback, export CSV  |

## Database Configuration

Default MySQL settings in `settings.py` (matches XAMPP defaults):

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'feedback_db',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

Adjust `USER` and `PASSWORD` if your XAMPP MySQL has different credentials.
