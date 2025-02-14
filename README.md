# E-Commerce Web API

## Overview
This project is a Django-based web API that includes user authentication, product management, and order processing.

## Features
- User registration and authentication using JWT.
- Profile management.
- Product listing and management.
- Order creation and management.
- Signal handling for automatic cart creation.
- Custom permissions for user and staff.
- API documentation using Swagger and ReDoc.
- Admin panel for managing products and orders.
- JWT token authentication for protected endpoints.
- Uses PostgreSQL as the database.

## Installation

### Prerequisites
- Python 3.x
- pip

### Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/John-6670/E-commerce-API.git
    cd yourproject
    ```
2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration
1. Create a `.env` file in the root directory and add the following environment variables:
    ```env
    SECRET_KEY=your_secret_key
    DEBUG=True
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=your_db_host
    DB_PORT=your_db_port
    ```

## Usage
1. Apply migrations:
    ```bash
    python manage.py migrate
    ```
2. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```
3. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Documentation
1. Access the API documentation at `http://localhost:8000/swagger/`. or `http://localhost:8000/redoc/`
2. Use the JWT token to authenticate requests.
3. Create a user and log in to access the protected endpoints.
4. Use the admin panel to manage products and orders.