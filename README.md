FastAPI Ecommerce App Backend
**Description**

This repository contains the backend code for a FastAPI-based ecommerce application. It provides a set of API endpoints to handle various functionalities of an ecommerce platform, such as user authentication, product management, and order processing.

**Features**

User authentication (registration, login, logout)
Product management (CRUD operations)
Shopping cart functionality
Order processing and tracking

**Technologies Used**

FastAPI: A modern, fast (high-performance), web framework for building APIs with Python 3.7+.
SQLAlchemy/tortoise: SQL toolkit and Object-Relational Mapping (ORM) for Python.
Pydantic: Data validation and settings management using Python type annotations.
uvicorn: ASGI server for FastAPI.

**Installation**

git clone https://github.com/your-username/fastapi-ecommerce-backend.git
cd fastapi-ecommerce-backend
pip install -r requirements.txt
# config.py

DATABASE_URL = "sqlite:///./test.db"  # Use your preferred database URL
uvicorn main:app --reload
API Documentation
Access the Swagger documentation at http://localhost:8000/docs for detailed information about available API endpoints and how to use them.

**Contributing**

If you'd like to contribute to this project, please follow the Contribution Guidelines.

** License**

This project is licensed under the MIT License.



                                                                                  
