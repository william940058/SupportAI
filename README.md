
# SupportAI

An AI-powered customer support system under development, built with Python, FastAPI, and PostgreSQL.

Currently, the project provides a REST API for managing customer orders. Future development will integrate retrieval-augmented generation (RAG) and an LLM to answer customer support questions.

## Features

- RESTful API built with FastAPI
- PostgreSQL database integration
- Create, read, update, and delete orders
- Request validation using Pydantic
- HTTP error handling
- Automated API testing using Pytest
- Mock-based database testing
- Interactive API documentation using Swagger UI

## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL
- Psycopg 3
- Pydantic
- Pytest
- HTTPX
- Git and GitHub

## Project Structure

```text
SupportAI/
├── main.py
├── database.py
├── test_main.py
├── test_db.py
├── requirements.txt
├── .gitignore
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Welcome message |
| GET | /health | Health check |
| POST | /chat | Echo chat message |
| GET | /orders/{order_id} | Retrieve an order |
| POST | /orders | Create an order |
| PATCH | /orders/{order_id} | Update order status |
| DELETE | /orders/{order_id} | Delete an order |

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/william940058/SupportAI.git
cd SupportAI
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a PostgreSQL database named `supportai_db`.

The current development version expects a local PostgreSQL connection configured in `database.py`.

Database schema initialization and environment-variable configuration will be improved in future versions.

### 5. Run the API

```bash
python -m uvicorn main:app --reload
```

Open Swagger UI:

http://127.0.0.1:8000/docs

## Running Tests

```bash
python -m pytest -v
```

The current test suite contains 9 automated test cases covering API health checks, input validation, order retrieval, error handling, and order creation.

Database-dependent tests use mocks to avoid modifying real data.

## Roadmap

- [x] FastAPI backend
- [x] PostgreSQL integration
- [x] Order CRUD APIs
- [x] Automated testing
- [ ] Authentication and authorization
- [ ] Database migrations and configuration
- [ ] RAG-based knowledge retrieval
- [ ] LLM-powered customer support
- [ ] Streamlit frontend
- [ ] Docker deployment

## Project Status

Work in progress. Currently intended for local development and learning, not production deployment.
