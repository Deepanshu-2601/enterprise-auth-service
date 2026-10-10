# enterprise-auth-service
# 🛡️ Enterprise Authentication & RBAC Microservice

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com/)

A production-ready RESTful authentication and authorization microservice built with **FastAPI**, **SQLAlchemy**, and **Pydantic**. It features stateless JSON Web Token (JWT) session handling, cryptographic password hashing, role-based access control (RBAC), and pure-Python relational persistence.

---

## 🚀 Live Demo & Documentation

- **Interactive Swagger UI:**[https://enterprise-auth-service-kd1g.onrender.com/docs](https://enterprise-auth-service-kd1g.onrender.com/docs)
- **Service Base URL:**[https://enterprise-auth-service-kd1g.onrender.com/docs](https://enterprise-auth-service-kd1g.onrender.com)
---

## ✨ Features

- **User Registration & Validation:** Strong input validation using Pydantic models and `email-validator`.
- **Cryptographic Security:** Secure password hashing and verification workflows.
- **Stateless Authentication:** Cryptographic JWT token generation with expiration tracking (`python-jose`).
- **Role-Based Access Control (RBAC):** Protected internal endpoints accessible only via valid Bearer tokens.
- **Relational Persistence:** Pure-Python SQLite integration using SQLAlchemy ORM.
- **Automated API Documentation:** Auto-generated interactive Swagger UI and ReDoc endpoints.

---

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **ASGI Server:** Uvicorn
- **ORM / Database:** SQLAlchemy / SQLite
- **Security & Tokens:** Python-Jose (JWT), Cryptography
- **Data Validation:** Pydantic v2
- **Deployment Platform:** Render Cloud

---

## 📡 API Endpoints

| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/` | Health check & service entry | Public |
| `POST` | `/register` | Register a new user | Public |
| `POST` | `/login` | Authenticate user & return JWT token | Public |
| `GET` | `/profile` | Retrieve authenticated user profile | Bearer Token Required |
| `GET` | `/docs` | Interactive OpenAPI Swagger UI | Public |

---

## 💻 Local Setup & Execution

### 1. Clone the Repository
```bash
git clone [https://github.com/Deepanshu-2601/enterprise-auth-service.git](https://github.com/Deepanshu-2601/enterprise-auth-service.git)
cd enterprise-auth-service
