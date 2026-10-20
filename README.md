# Datheon Backend Internship - Python + FastAPI Development Track

**Candidate:** Hamza  
**Track:** Python + FastAPI Backend Development Internship  
**Repository Name:** Datheon_Python_+_FastAPI_Backend_Development_Internship  

---

## 📌 Project Overview
This repository contains the end-to-end implementation of all 4 required backend tasks for the Datheon Internship. The project encompasses REST API architecture, JWT authentication with Role-Based Access Control (RBAC), SQL database persistence using SQLAlchemy ORM, asynchronous background job processing, request rate-limiting, and Docker containerization[cite: 8, 13].

---

## 🚀 Tasks Implemented

### Task 1: BookStore REST API (`main.py`)
- Full asynchronous CRUD operations for bookstore inventory management.
- Request validation using Pydantic schemas.
- Path parameters, status codes, and optional query filtering (e.g., `max_price`).
- Interactive Swagger documentation at `/docs`.

### Task 2: User Authentication & RBAC (`auth_app.py`)
- User registration with secure cryptographic password hashing[cite: 8].
- OAuth2 password flow issuing signed JSON Web Tokens (JWT)[cite: 8].
- Role-Based Access Control (RBAC) protecting endpoints (`/users/me` and `/admin/dashboard`)[cite: 8].

### Task 3: Database Persistence with SQLAlchemy & SQLite (`db_app.py`)
- Relational data modeling using SQLAlchemy ORM (One-to-Many: `Users` -> `Notes`)[cite: 13].
- Local file persistence via SQLite (`app_data.db`) across server reboots[cite: 13].
- Clean architecture separating database session management and dependency injection[cite: 13].

### Task 4: Microservice with Background Tasks & Rate Limiting (`bg_app.py`, `Dockerfile`)
- Asynchronous task queuing using FastAPI `BackgroundTasks` for non-blocking operations.
- In-memory sliding-window IP rate limiter preventing service overload (`429 Too Many Requests`).
- Production-ready multi-stage `Dockerfile` for microservice containerization.

### Unified Server (`all_tasks.py`)
- Master FastAPI application mounting all 4 sub-applications under distinct sub-paths:
  - `/bookstore/docs/` -> Task 1 Interactive Docs
  - `/auth/docs/` -> Task 2 Interactive Docs
  - `/database/docs/` -> Task 3 Interactive Docs
  - `/background/docs/` -> Task 4 Interactive Docs

---

## 🛠️ Tech Stack & Dependencies
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **ASGI Server:** Uvicorn
- **ORM / Database:** SQLAlchemy, SQLite[cite: 13]
- **Validation:** Pydantic
- **Security:** PyJWT / Python-Jose, Cryptography, Passlib
- **Containerization:** Docker

---

