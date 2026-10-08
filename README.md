# Healthcare Backend API System

[![Django](https://img.shields.io/badge/Django-5.1-green.svg)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.17-red.svg)](https://www.django-rest-framework.org/)
[![JWT](https://img.shields.io/badge/JWT-SimpleJWT-orange.svg)](https://django-rest-framework-simplejwt.readthedocs.io/)
[![Database](https://img.shields.io/badge/PostgreSQL-Ready-blue.svg)](https://www.postgresql.org/)
[![Tests](https://img.shields.io/badge/Tests-26%20Passed-brightgreen.svg)]()

A robust, secure backend system for a healthcare application built using **Django**, **Django REST Framework (DRF)**, **SimpleJWT**, and **PostgreSQL**. The platform enables secure user authentication, patient and doctor record management, and doctor-patient mapping with ownership protection and validation.

---

## 🚀 Key Features

- **JWT Authentication**: Secure user registration and login using `djangorestframework-simplejwt` with custom user model (email-based login).
- **Patient Management**: Full CRUD operations for patients with multi-tenant data isolation (users only access patients they registered).
- **Doctor Management**: Full CRUD operations for doctors with specialization, contact details, and hospital affiliation.
- **Patient-Doctor Mapping**: Assign doctors to patients, retrieve all mappings, retrieve doctors assigned to a specific patient, and remove assignments with duplicate-prevention validation.
- **Interactive Documentation**: Auto-generated **Swagger UI** (`/api/docs/`) and **ReDoc** (`/api/redoc/`) via `drf-spectacular`.
- **Database Flexibility**: Native PostgreSQL integration with seamless SQLite toggle via `.env` for zero-configuration local runs.
- **Automated Test Suite**: 26 unit and integration test cases covering authentication, CRUD operations, permissions, and edge cases.
- **Ready-to-Use Postman Collection**: Complete pre-configured Postman collection with automatic token capture scripts.

---

## 🏗️ Architecture & Project Structure

```text
vishwajeet-whatbytes-assignment/
├── authentication/                  # User accounts, registration, login & JWT
│   ├── management/commands/seed_data.py # Demo database seeder
│   ├── models.py                    # Custom User model (email authentication)
│   ├── serializers.py               # Register, Login & User serializers
│   ├── views.py                     # Auth API views
│   ├── urls.py                      # Auth endpoints
│   └── tests.py                     # Auth test suite
├── patients/                        # Patient records & ownership isolation
│   ├── models.py                    # Patient model
│   ├── serializers.py               # Patient serializer & validation
│   ├── views.py                     # Patient List/Create & Detail views
│   ├── urls.py                      # Patient routes
│   └── tests.py                     # Patient test suite
├── doctors/                         # Medical practitioner management
│   ├── models.py                    # Doctor model
│   ├── serializers.py               # Doctor serializer & validation
│   ├── views.py                     # Doctor List/Create & Detail views
│   ├── urls.py                      # Doctor routes
│   └── tests.py                     # Doctor test suite
├── mappings/                        # Patient-Doctor associations
│   ├── models.py                    # PatientDoctorMapping model
│   ├── serializers.py               # Mapping serializers & uniqueness validation
│   ├── views.py                     # Mapping List/Create, Patient & Delete views
│   ├── urls.py                      # Mapping routes
│   └── tests.py                     # Mapping test suite
├── healthcare_backend/              # Django project core
│   ├── settings.py                  # Settings, SimpleJWT, DB & DRF configuration
│   ├── urls.py                      # Root URL routing & Swagger endpoints
│   └── wsgi.py
├── Healthcare_Backend.postman_collection.json # Exportable Postman collection
├── .env.example                     # Environment variables template
├── .env                             # Environment configuration
├── requirements.txt                 # Project dependencies
└── manage.py
```

---

## 🛠️ Tech Stack

- **Framework**: Django 5.1 & Django REST Framework (DRF) 3.17
- **Authentication**: `djangorestframework-simplejwt`
- **Database**: PostgreSQL (driver: `psycopg2-binary`) / SQLite fallback
- **Configuration**: `python-dotenv`
- **CORS**: `django-cors-headers`
- **API Documentation**: `drf-spectacular` (OpenAPI 3.0 / Swagger UI)
- **Testing**: Django Test Runner & `pytest-django`

---

## 📦 Setup & Installation Guide

### 1. Clone & Enter Project Directory
```bash
git clone <repository-url>
cd vishwajeet-whatbytes-assignment
```

### 2. Create and Activate Virtual Environment
On Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
On Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` to configure your PostgreSQL credentials:
```ini
# Django Settings
SECRET_KEY=your-secure-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,testserver

# Database Configuration (PostgreSQL)
# Set USE_SQLITE=False to connect to PostgreSQL:
USE_SQLITE=False
DB_ENGINE=django.db.backends.postgresql
DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

# JWT Lifetime Settings
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=1
```

> **Note**: For quick local evaluation without running PostgreSQL, leave `USE_SQLITE=True`. To connect to PostgreSQL, create the database in Postgres (`CREATE DATABASE healthcare_db;`) and set `USE_SQLITE=False`.

### 5. Apply Database Migrations
```bash
python manage.py migrate
```

### 6. (Optional) Seed Sample Healthcare Data
Populate the database with demo users, doctors, patients, and mappings:
```bash
python manage.py seed_data
```
**Sample credentials created by seeder:**
- **Superuser (Admin Panel)**: `admin@healthcare.com` / `AdminPassword123!`
- **User 1 (Doctor)**: `dr.john@healthcare.com` / `Password123!`
- **User 2 (Nurse)**: `nurse.mary@healthcare.com` / `Password123!`

### 7. Run the Development Server
```bash
python manage.py runserver
```
The server will start at `http://127.0.0.1:8000/`.

---

## 📖 API Documentation & Swagger UI

Once the server is running, explore the interactive OpenAPI 3 documentation:
- **Swagger UI**: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- **ReDoc**: [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)
- **OpenAPI Schema (JSON/YAML)**: [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)

---

## 📡 API Endpoints Reference

All endpoints (except registration and login) require the JWT Bearer token in the `Authorization` header:
```http
Authorization: Bearer <your_access_token>
```

### 1. Authentication APIs

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/auth/register/` | Register a new user with name, email, password | No |
| `POST` | `/api/auth/login/` | Authenticate user & return JWT tokens | No |
| `GET` | `/api/auth/me/` | Get current authenticated user details | Yes |
| `POST` | `/api/auth/token/refresh/` | Refresh expired access token | No |

#### `POST /api/auth/register/`
**Request Body:**
```json
{
  "name": "Dr. Alice Martin",
  "email": "alice@healthcare.com",
  "password": "SecurePassword123!"
}
```
**Response (201 Created):**
```json
{
  "message": "User registered successfully.",
  "user": {
    "id": 1,
    "name": "Dr. Alice Martin",
    "email": "alice@healthcare.com",
    "created_at": "2026-10-08T19:55:00Z"
  },
  "tokens": {
    "access": "eyJhbGciOi...",
    "refresh": "eyJhbGciOi..."
  }
}
```

#### `POST /api/auth/login/`
**Request Body:**
```json
{
  "email": "alice@healthcare.com",
  "password": "SecurePassword123!"
}
```
**Response (200 OK):**
```json
{
  "message": "Login successful.",
  "user": {
    "id": 1,
    "name": "Dr. Alice Martin",
    "email": "alice@healthcare.com"
  },
  "tokens": {
    "access": "eyJhbGciOi...",
    "refresh": "eyJhbGciOi..."
  }
}
```

---

### 2. Patient Management APIs

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/patients/` | Add a new patient | Yes |
| `GET` | `/api/patients/` | Retrieve all patients created by the authenticated user | Yes |
| `GET` | `/api/patients/<id>/` | Get details of a specific patient | Yes |
| `PUT` | `/api/patients/<id>/` | Update patient details | Yes |
| `PATCH` | `/api/patients/<id>/` | Partially update patient details | Yes |
| `DELETE` | `/api/patients/<id>/` | Delete a patient record | Yes |

#### `POST /api/patients/`
**Request Body:**
```json
{
  "name": "Johnathan Doe",
  "age": 35,
  "gender": "Male",
  "contact_number": "+1-555-0199",
  "email": "johnathan@example.com",
  "address": "123 Elm Street, Cityville",
  "medical_history": "No known allergies. Seasonal asthma."
}
```
**Response (201 Created):**
```json
{
  "id": 1,
  "name": "Johnathan Doe",
  "age": 35,
  "gender": "Male",
  "contact_number": "+1-555-0199",
  "email": "johnathan@example.com",
  "address": "123 Elm Street, Cityville",
  "medical_history": "No known allergies. Seasonal asthma.",
  "created_by": 1,
  "created_by_name": "Dr. Alice Martin",
  "created_by_email": "alice@healthcare.com",
  "created_at": "2026-10-08T19:56:00Z",
  "updated_at": "2026-10-08T19:56:00Z"
}
```

---

### 3. Doctor Management APIs

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/doctors/` | Add a new doctor | Yes |
| `GET` | `/api/doctors/` | Retrieve all doctors | Yes |
| `GET` | `/api/doctors/<id>/` | Get details of a specific doctor | Yes |
| `PUT` | `/api/doctors/<id>/` | Update doctor details | Yes |
| `PATCH` | `/api/doctors/<id>/` | Partially update doctor details | Yes |
| `DELETE` | `/api/doctors/<id>/` | Delete a doctor record | Yes |

#### `POST /api/doctors/`
**Request Body:**
```json
{
  "name": "Gregory House",
  "specialization": "Diagnostic Medicine",
  "contact_number": "+1-555-8888",
  "email": "dr.house@princeton.edu",
  "years_of_experience": 20,
  "hospital_affiliation": "Princeton-Plainsboro Teaching Hospital"
}
```
**Response (201 Created):**
```json
{
  "id": 1,
  "name": "Gregory House",
  "specialization": "Diagnostic Medicine",
  "contact_number": "+1-555-8888",
  "email": "dr.house@princeton.edu",
  "years_of_experience": 20,
  "hospital_affiliation": "Princeton-Plainsboro Teaching Hospital",
  "created_by": 1,
  "created_by_name": "Dr. Alice Martin",
  "created_at": "2026-10-08T19:57:00Z",
  "updated_at": "2026-10-08T19:57:00Z"
}
```

---

### 4. Patient-Doctor Mapping APIs

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/mappings/` | Assign a doctor to a patient | Yes |
| `GET` | `/api/mappings/` | Retrieve all patient-doctor mappings | Yes |
| `GET` | `/api/mappings/<patient_id>/` | Get all doctors assigned to a specific patient | Yes |
| `DELETE` | `/api/mappings/<id>/` | Remove a doctor from a patient (delete mapping by mapping ID) | Yes |

#### `POST /api/mappings/`
**Request Body:**
```json
{
  "patient": 1,
  "doctor": 1,
  "notes": "Assigned for diagnostic evaluation and ongoing follow-up."
}
```
**Response (201 Created):**
```json
{
  "message": "Doctor assigned to patient successfully.",
  "mapping": {
    "id": 1,
    "patient_id": 1,
    "patient": {
      "id": 1,
      "name": "Johnathan Doe",
      "age": 35,
      "gender": "Male",
      "contact_number": "+1-555-0199"
    },
    "doctor_id": 1,
    "doctor": {
      "id": 1,
      "name": "Gregory House",
      "specialization": "Diagnostic Medicine",
      "contact_number": "+1-555-8888",
      "email": "dr.house@princeton.edu",
      "hospital_affiliation": "Princeton-Plainsboro Teaching Hospital"
    },
    "notes": "Assigned for diagnostic evaluation and ongoing follow-up.",
    "assigned_date": "2026-10-08T19:58:00Z"
  }
}
```

#### `GET /api/mappings/<patient_id>/`
**Response (200 OK):**
```json
{
  "patient_id": 1,
  "patient_name": "Johnathan Doe",
  "total_assigned": 1,
  "assigned_doctors": [
    {
      "id": 1,
      "patient_id": 1,
      "doctor_id": 1,
      "doctor": {
        "id": 1,
        "name": "Gregory House",
        "specialization": "Diagnostic Medicine",
        "contact_number": "+1-555-8888",
        "email": "dr.house@princeton.edu",
        "hospital_affiliation": "Princeton-Plainsboro Teaching Hospital"
      },
      "notes": "Assigned for diagnostic evaluation and ongoing follow-up.",
      "assigned_date": "2026-10-08T19:58:00Z"
    }
  ]
}
```

#### `DELETE /api/mappings/<id>/`
**Response (204 No Content)**

---

## 🧪 Running the Automated Tests

Run the comprehensive test suite verifying all 26 test cases:
```bash
python manage.py test
```
Or with `pytest`:
```bash
pytest
```
**Test Coverage Includes:**
- User registration with valid and invalid data (duplicate emails, password validations)
- JWT token generation, refresh, and authentication rejection
- User isolation (User A cannot view, edit, or delete User B's patient records)
- Patient CRUD operations
- Doctor CRUD operations
- Doctor assignment to patients, duplicate assignment validation, and mapping deletion

---

## 📮 Testing with Postman

A complete Postman collection is included in the project root:
📁 `Healthcare_Backend.postman_collection.json`

### How to use:
1. Open **Postman** and click **Import**.
2. Select `Healthcare_Backend.postman_collection.json`.
3. In the collection, run `1. Authentication -> Login User`.
4. The test script automatically stores the returned JWT access token into the collection variable `{{jwt_token}}`.
5. Run any Patient, Doctor, or Mapping requests seamlessly!
