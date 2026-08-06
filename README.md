# E-Commerce API
 
A modular, production-ready backend for an e-commerce platform, built with **FastAPI** and **SQLAlchemy**. It provides authentication, product catalog management, shopping cart, order processing, payments/transactions, reviews, and admin operations behind a clean, versioned REST API.
 
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)
![License](https://img.shields.io/badge/License-MIT-green)
 
---
 
## Table of Contents
 
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the App](#running-the-app)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
---
 
## Features
 
- 🔐 **Authentication & Authorization** — JWT-based auth with OAuth2 password flow
- 🛍️ **Product Catalog** — Products and categories management
- 🛒 **Shopping Cart** — Add, update, and remove cart items
- 📦 **Order Management** — Order creation and order item tracking
- 💳 **Payments & Transactions** — Payment processing and transaction records
- ⭐ **Reviews** — Product review system
- 🛠️ **Admin Panel** — Admin-level endpoints for platform management
- 📧 **Email Notifications** — Transactional email service
- 🚦 **Rate Limiting** — API request throttling for abuse prevention
- ✅ **Robust Error Handling** — Centralized exception handling
## Tech Stack
 
| Category            | Technology                     |
|----------------------|--------------------------------|
| Framework            | [FastAPI](https://fastapi.tiangolo.com/) |
| ORM                   | [SQLAlchemy](https://www.sqlalchemy.org/) |
| Data Validation       | [Pydantic](https://docs.pydantic.dev/) |
| Authentication        | JWT / OAuth2 Password Flow      |
| Package Management    | [uv](https://docs.astral.sh/uv/) |
| Testing               | [pytest](https://docs.pytest.org/) |
 
## Project Structure
 
```
e_commerce/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/       # Route handlers (auth, product, order, cart, admin, transaction)
│   │   │   └── api.py           # API router aggregation
│   │   └── dependencies.py      # Shared dependency injection (auth, db session, etc.)
│   ├── core/
│   │   ├── config.py            # App settings & environment configuration
│   │   ├── exception.py         # Custom exception handlers
│   │   ├── mail.py              # Email client/config
│   │   ├── rate_limiting.py     # Rate limiting configuration
│   │   └── security.py          # Password hashing, JWT utilities
│   ├── db/
│   │   └── database.py          # Database engine & session setup
│   ├── models/                  # SQLAlchemy ORM models
│   ├── schemas/                 # Pydantic request/response schemas
│   ├── services/
│   │   └── email_service.py     # Email sending logic
│   ├── tasks/                   # Background/async tasks
│   └── main.py                  # Application entry point
├── tests/                       # Test suite
├── pyproject.toml
├── uv.lock
└── requirement.txt
```
 
## Getting Started
 
### Prerequisites
 
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or `pip`
- A running database instance (PostgreSQL recommended)
### Installation
 
Clone the repository:
 
```bash
git clone https://github.com/<your-username>/e_commerce.git
cd e_commerce
```
 
Install dependencies using `uv`:
 
```bash
uv sync
```
 
Or, using `pip`:
 
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirement.txt
```
 
### Environment Variables
 
Create a `.env` file in the project root and configure the following:
 
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ecommerce_db
 
# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
 
# Email
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-email-password
MAIL_FROM=your-email@example.com
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
```
 
> Adjust variable names to match what's referenced in `app/core/config.py`.
 
### Running the App
 
```bash
uv run uvicorn app.main:app --reload
```
 
Or, if using a virtual environment directly:
 
```bash
uvicorn app.main:app --reload
```
 
The API will be available at `http://127.0.0.1:8000`.
 
## API Documentation
 
FastAPI automatically generates interactive API documentation:
 
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`
## Testing
 
Run the test suite with `pytest`:
 
```bash
uv run pytest
```
 
Or:
 
```bash
pytest
```
 
## Contributing
 
Contributions are welcome! To contribute:
 
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add your feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request
## License
 
This project is licensed under the [MIT License](LICENSE).