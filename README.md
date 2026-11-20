<div align="center">

# Job Platform

### A job recruitment and application web platform built with Django

A web application that connects job seekers and employers. Job seekers can create profiles, upload résumés, explore job listings, and submit applications, while employers can publish vacancies and manage received applications.

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/Status-In%20Development-orange)](#current-scope)

</div>

---

## Overview

**Job Platform** is a Django-based recruitment application designed to bring job seekers and employers together in one place.

A single user account can be used to participate in the platform as a job seeker and as an employer. Users can authenticate with their mobile phone number through a one-time password (OTP), maintain their profile, and interact with job listings according to their needs.

The application uses Django's server-rendered templates for its frontend and PostgreSQL for data storage. Mobile verification is integrated with the Kavenegar SMS service.

## Features

### Accounts and authentication
- Register and log in using a mobile phone number.
- Verify phone numbers with a six-digit, one-time password (OTP).
- Send verification codes through the Kavenegar SMS service.
- OTP expiration and resend time limits.
- Session-based authentication using a custom Django user model.
- Django Admin access for administrative users.

### Job seeker profiles
- Create and update a personal profile.
- Upload a résumé in PDF format.
- Keep profile information available when applying for jobs.
- View submitted job applications and their latest statuses.

### Job listings
- Browse available job listings.
- Explore jobs by category.
- View job details, including the information provided by the employer.
- Search and discover opportunities from the home page.
- Create, update, and manage job listings as an employer.
- Set job information such as title, description, location, salary, and application deadline.

### Job applications
- Apply for a job using the job seeker's profile.
- Save a separate résumé snapshot for each application.
- Add a cover letter to an application.
- Prevent duplicate applications to the same job.
- Track application statuses, including submitted, reviewing, interview, rejected, and accepted.

### Employer features
- Publish and manage job listings.
- View applications received for owned job listings.
- Filter received applications by job.
- Review applicant information and résumé snapshots.
- Update the status of an application.

### Interface and administration
- Server-rendered pages using Django Templates.
- Responsive interface built with Bootstrap, HTML, CSS, and JavaScript.
- Django messages for user feedback.
- Django Admin integration for managing application data.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Main programming language |
| Django 5.2 | Web framework, URL routing, class-based views, forms, authentication, and ORM |
| PostgreSQL | Relational database |
| HTML5 | Page structure |
| CSS3 | Custom interface styling |
| Bootstrap 5 | Responsive layout and UI components |
| JavaScript | Client-side interface interactions |
| Django Templates | Server-rendered frontend |
| Kavenegar | Sending OTP verification messages via SMS |
| `python-decouple` | Reading configuration and environment variables |
| Pillow | Image processing support |

## Project Structure

The project is organized into separate Django apps, each responsible for a specific part of the platform.

```text
job_platform/
├── apps/
│   ├── accounts/
│   │   ├── migrations/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── signals.py
│   │   ├── urls.py
│   │   ├── utils.py
│   │   └── views.py
│   │
│   ├── applications/
│   │   ├── migrations/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── core/
│   │   ├── migrations/
│   │   ├── apps.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   └── jobs/
│       ├── migrations/
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── urls.py
│       └── views.py
│
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── asgi.py
│   ├── urls.py
│   └── wsgi.py
│
├── templates/
│   ├── accounts/
│   ├── applications/
│   ├── core/
│   ├── jobs/
│   └── base.html
│
├── static/
├── .env.example
├── .gitignore
├── manage.py
└── requirements.txt
```

### Django apps

- **`accounts`** — custom user model, phone-number authentication, OTP verification, user profiles, and résumé uploads.
- **`jobs`** — job categories, job listings, and employer job management.
- **`applications`** — job applications, résumé snapshots, application tracking, and employer-side application management.
- **`core`** — home page and shared platform entry point.
- **`config`** — Django project configuration, settings, and root URL configuration.

## Getting Started

Follow these steps to run the project locally.

### 1. Clone the repository

```bash
git clone https://github.com/armanghorbanpour/job_platform.git
cd job_platform
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the environment file

Create a `.env` file in the project root, next to `manage.py`, and configure the required values.

```env
SECRET_KEY=your-django-secret-key
DEBUG=True

DB_NAME=job_platform
DB_USER=postgres
DB_PASSWORD=your-database-password
DB_HOST=127.0.0.1
DB_PORT=5432

KAVENEGAR_API_KEY=your-kavenegar-api-key
KAVENEGAR_SENDER=your-sender-number
SEND_REAL_SMS=False
```

Update the database values to match your local PostgreSQL configuration.

Set `SEND_REAL_SMS=True` when you want OTP messages to be sent through Kavenegar. Keep it set to `False` for local development without sending real SMS messages.

### 5. Apply database migrations

```powershell
python manage.py migrate
```

### 6. Create an administrator account

```powershell
python manage.py createsuperuser
```

### 7. Run the development server

```powershell
python manage.py runserver
```

Open the application in your browser:

- Website: `http://127.0.0.1:8000/`
- Django Admin: `http://127.0.0.1:8000/admin/`

## Main Application Areas

| Area | Description |
|---|---|
| Home | Browse the platform, search for jobs, and explore categories |
| Accounts | Phone-number login, OTP verification, and profile management |
| Jobs | Browse job listings and manage employer vacancies |
| Applications | Submit applications and track their statuses |
| Employer applications | Review applications received for employer-owned jobs |
| Django Admin | Administrative management of platform data |

## Data Models

The platform uses Django models to represent its main data.

### `User`
A custom Django user model that uses a mobile phone number as the account identifier.

### `OtpCode`
Stores the one-time verification code data used during phone-number authentication, along with its creation time and attempt count.

### `Profile`
Stores additional information associated with a user, including profile details and the uploaded résumé.

### `Category`
Represents a category used to organize job listings.

### `Job`
Stores a job listing and its related employer, category, description, location, salary information, and other vacancy details.

### `Application`
Connects a job seeker to a job listing. It stores application information, status, cover letter, and an independent résumé snapshot.

## OTP Authentication

The platform uses one-time passwords to authenticate users through their mobile phone numbers.

1. The user submits a phone number.
2. The application generates a six-digit verification code.
3. The code is sent through Kavenegar when real SMS sending is enabled.
4. The user submits the received code.
5. After successful verification, the user is authenticated and can continue to the platform.

OTP codes are configured with a five-minute validity period and a resend interval.

## Application Workflow

The application process connects job seekers with employers through a status-based workflow.

1. An employer creates and publishes a job listing.
2. A job seeker opens the listing and submits an application.
3. The application stores a snapshot of the résumé available at submission time.
4. The employer views applications received for their job listings.
5. The employer updates each application's status as the recruitment process progresses.
6. The job seeker can view the status of submitted applications.

## Configuration

The project uses separate settings modules for different environments:

- `config.settings.base` — shared Django settings.
- `config.settings.development` — development settings.
- `config.settings.production` — production settings.

The default `manage.py` configuration uses the development settings module.

Sensitive configuration values, database credentials, and the Kavenegar API key are read from environment variables.

## Current Scope

The current version focuses on the core recruitment workflow: phone-number authentication, user profiles, job publishing, résumé submission, and application management.

The platform supports both job seeker and employer functionality within the same user account.

## Development

To make changes to the database models, create and apply Django migrations:

```powershell
python manage.py makemigrations
python manage.py migrate
```

To run Django's system checks:

```powershell
python manage.py check
```

---

<div align="center">

**Built with Python, Django, and PostgreSQL.**

</div>
