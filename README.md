# SOS — Student Online System

## Project Overview

**SOS (Student Online System)** is a full-stack Enterprise Academic Management Web Application built using **Python** and **Django**.  
The application is designed to manage the complete academic lifecycle of an educational institution — including student enrollment, academic records, faculty management, marksheet entry, timetable scheduling, and role-based administration.

The project follows a clean, modular, and scalable architecture using industry-standard enterprise design principles, and uniquely exposes **two independent interfaces** from a single codebase: a server-rendered web application and a JSON REST API.

---

# Technologies Used

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Web Framework | Django 3+ |
| REST Framework | Django REST Framework (DRF) |
| JWT | `djangorestframework-simplejwt` |
| CORS | `django-cors-headers` |
| Database | SQLite3 (dev); MySQL / PostgreSQL configs included |
| ORM | Django ORM with Paginator |
| Templating | Django Template Language (DTL) |
| UI Framework | Bootstrap 4, Font Awesome (CDN) |
| Email | SMTP via Gmail (`django.core.mail`) with async threading |
| PDF / Excel | `xhtml2pdf`, `xlwt` |
| Logging | Python `logging` module with named layered loggers |
| Testing | Django `TestCase` |

---

# Key Features

## Academic Management Modules

- College, Course, Subject, and Faculty master management
- Student registration linked with colleges
- Marksheet entry for:
  - Physics
  - Chemistry
  - Mathematics
- Auto-calculated:
  - Total marks
  - Percentage
- Individual student marksheet retrieval

---

## User & Access Management

- Role-based authentication:
  - Admin (`role_id = 1`)
  - Student / Regular User (`role_id = 2`)
- Dual authentication mechanisms:
  - **Session-based** for the web application (ORS)
  - **JWT (Access + Refresh tokens)** for the REST API (ORSAPI)
- User self-registration with email welcome notification
- Profile management with photo upload
- Forgot Password (email-based) and Change Password workflows

---

## REST API Layer

- JSON-based REST endpoints for all entities:
  - College, Course, Role, Faculty
  - Student, Subject, TimeTable
  - User (Login, Register, Change Password, Forgot Password)
- Uniform response contract across all endpoints:
  ```json
  { "error": false, "message": "...", "data": { ... } }
  ```
- JWT authentication with custom backend targeting the service-layer `User` model
- REST APIs coexist alongside the traditional web interface
- CORS configured for Angular SPA (`http://localhost:4200`)

---

## Pagination

- Built into the base DAO layer using Django's `Paginator`
- Every list module supports:
  - Configurable page size (default: 10)
  - Previous / Next navigation
  - "Showing X to Y of Z records" counter
  - Search filters preserved across page turns via hidden form field
- Implemented consistently across all 8 list modules:
  College, Course, Role, Student, User, Marksheet, Subject, TimeTable

---

## Email Notifications

- Async email delivery (background daemon thread — never blocks HTTP response)
- Template-based HTML emails using Python `string.Template`
- Three automated email events:
  - New user signup welcome
  - Password changed confirmation
  - Forgot password (password delivery)

---

## Robustness & Quality Features

- Centralized request lifecycle in `BaseCtl.execute()` — controllers never handle routing directly
- Server-side input validation before any persistence operation using `DataValidator` utility
- Session guard (`FrontController`) and JWT + role guard (`RestFrontCtl`) as dedicated middleware
- Named layered loggers: `ORS`, `ORSAPI`, `service` — independently configurable per layer
- Unit tests covering every controller in `ORS/test/`
- Custom `DropdownItem` abstraction — all SELECT elements generated uniformly via `HtmlUtility`
- 21 incremental tracked database migrations

---

# Architecture & Design

```
Browser / SPA / Mobile
        │
        ├── /ORS/**  (Web)          ├── /ORSAPI/**  (REST API)
        │                           │
  FrontController              RestFrontCtl
  (Session Guard)              (JWT + Role Guard)
        │                           │
  ORS/views.py              ORSAPI/urls.py
  (Dynamic Router)           (DRF URL Patterns)
        │                           │
  ORS Controllers           ORSAPI REST Controllers
  (BaseCtl → *Ctl)          (BaseRestCtl → *Ctl)
        │                           │
        └──────────┬────────────────┘
                   │
            Service Layer
          (BaseService → *Service)
                   │
              DAO Layer
           (BaseDAO → *DAO)
                   │
            Django ORM
          service/models.py
                   │
         SQLite / MySQL / PostgreSQL
```

---

# Design Patterns Used

| Pattern | Implementation |
|---|---|
| MVC | `ORS/views.py` as dispatcher, `ORS/ctl/*.py` as Controllers, DTL templates as Views |
| Template Method | `BaseCtl.execute()` and `BaseDAO.search()` define the invariant algorithm; subclasses override hooks |
| Service-DAO (Repository) | Controllers → Service (business logic) → DAO (queries) → ORM — strict layer separation |
| Front Controller | `FrontController` and `RestFrontCtl` middleware centralize auth before any controller runs |
| Abstract Factory / Strategy | `DropdownItem` base class; `HtmlUtility` works uniformly with any model via `get_key()` / `get_value()` |
| Dynamic Dispatch | `ORS/views.py` instantiates controllers by name from the URL: `eval(page + "Ctl()")` |
| REST + MVC Hybrid | Traditional server-rendered UI and stateless JSON REST API coexist on the same domain model |

---

# Modules at a Glance

| Module | Operations |
|---|---|
| College | Add, Edit, Delete, Search, Pagination |
| Course | Add, Edit, Delete, Search, Pagination |
| Subject | Add, Edit, Delete, Search, Pagination |
| Faculty | Add, Edit, Delete, Search, Pagination |
| Student | Add, Edit, Delete, Search, Pagination |
| Marksheet | Add, Edit, Delete, Search, Auto Total & Percentage |
| TimeTable | Add, Edit, Delete, Search, Pagination |
| Role | Add, Edit, Delete |
| User | Register, Login, Profile, Photo Upload, Change/Forgot Password |
| REST API | All entities as JSON endpoints with JWT auth |

---

# What Makes This Project Stand Out

## 1. Dual Interface from a Single Domain Model

The same `service/models.py`, `service/service/`, and `service/dao/` layer powers:

- A full server-rendered **Bootstrap web application** (ORS) with session auth
- A stateless **JWT-secured REST API** (ORSAPI) for SPA/mobile consumption

No duplication of business logic. One source of truth.

---

## 2. Generic Layered Architecture

A single `BaseCtl`, `BaseService`, and `BaseDAO` power **all modules** using Python abstract base classes, making the codebase:

- DRY (Don't Repeat Yourself)
- Reusable across every entity
- Easy to extend — adding a new module requires only four files: `*Ctl.py`, `*Service.py`, `*DAO.py`, `*Serializer`
- Highly maintainable — a fix in the base reaches every module instantly

---

## 3. Enterprise-Level Practices

The project incorporates production-grade engineering standards:

- Async email delivery using Python threads
- Structured logging per application layer
- Centralized middleware-based authentication
- Paginated search on every list module
- 21-step schema migration history
- Unit tests for all controllers

---

## 4. Clean Authentication Architecture

Two authentication mechanisms coexist without conflict:

- **Session-based** authentication for the traditional web UI — handled entirely by `FrontController` middleware before the request reaches any controller
- **JWT (Access + Refresh)** authentication for the REST API — handled by `RestFrontCtl` middleware with a custom `ServiceUserJWTAuthentication` backend that targets the application `User` model rather than Django's built-in user

---

## 5. Separation of Concerns at Every Layer

```
Controller   →  knows nothing about the database
Service      →  owns business rules (email, password logic, calculations)
DAO          →  owns query construction, filtering, pagination
Model        →  defines entity structure and DropdownItem contract
Middleware   →  owns authentication and access control
Utility      →  owns HTML generation and data validation
```

No layer crosses into another's responsibility.

---

## 6. REST API Design Discipline

Every entity follows a uniform contract inherited from `BaseRestCtl`:

- Consistent HTTP methods and status codes across all endpoints
- Uniform JSON response envelope (`error`, `message`, `data`)
- Serializer-based validation before any persistence
- Role-based write protection infrastructure ready to activate

---

# Logging Architecture

Three named loggers map to the three application layers:

```python
logger = logging.getLogger('ORS')      # Web controller events
logger = logging.getLogger('ORSAPI')   # REST API events
logger = logging.getLogger('service')  # Service / DAO events
```

All loggers share a timestamped format:
```
[2025-05-28 10:30:00] DEBUG ORS - Processing login for: admin@ors.com
```

Loggers can be independently redirected to files, silenced, or escalated to ERROR in production without touching application code.

---

# Project Structure

```
SOS_django_projects/
├── SOS_django_projects/   # Django project config (settings, root urls, wsgi)
├── ORS/                   # Web application layer
│   ├── ctl/               # 20+ controller classes (BaseCtl + entity controllers)
│   ├── template/ors/      # 20 Bootstrap 4 HTML templates
│   ├── utility/           # HtmlUtility (dynamic SELECT generator)
│   ├── middleware.py       # FrontController (session auth guard)
│   ├── views.py           # Dynamic request dispatcher
│   └── urls.py            # URL patterns
├── ORSAPI/                # REST API layer
│   ├── rest/              # BaseRestCtl + entity REST controllers + JWTAuth
│   ├── middleware.py       # RestFrontCtl (JWT + role guard)
│   └── urls.py            # REST URL patterns
├── service/               # Shared domain layer (used by both ORS and ORSAPI)
│   ├── models.py          # 9 domain models (Role, User, College, Course,
│   │                      #   Faculty, Student, Marksheet, Subject, TimeTable)
│   ├── Serializers.py     # DRF ModelSerializers for all 9 models
│   ├── service/           # Business logic (BaseService + entity services)
│   ├── dao/               # Data access (BaseDAO + entity DAOs)
│   ├── mail/              # Async email (EmailMessage, EmailService, EmailBuilder)
│   ├── utility/           # DataValidator (8 static validation helpers)
│   └── migrations/        # 21 incremental schema migrations
├── static/                # CSS, JS, images
├── media/                 # User uploads (profile photos)
├── templates/             # Root-level templates
└── manage.py
```

---

# Built With

**Built by:** Sunil Sahu  
**Technology Stack:** Python 3 · Django · Django REST Framework · SQLite / MySQL · Bootstrap 4
