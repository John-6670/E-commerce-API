# E-Commerce Web API

---

## Overview
This project is a Django-based web API that includes user authentication, product management, order processing, and user email verification.

## Features
- User registration and authentication using JWT.
- Email verification after registration or email update.
- Secure password reset flow using verified email addresses.
- Profile management (excluding password changes).
- Product listing and management.
- Order creation and management.
- Signal handling for automatic cart creation.
- Custom permissions for user and staff.
- API documentation using Swagger and ReDoc.
- Admin panel for managing products and orders.
- JWT token authentication for protected endpoints.
- Uses PostgreSQL as the database.

## Authentication Updates
- After signing up or updating the email address, users receive a verification email.
- Only verified users can request a password reset link.
- **Password cannot be changed via the `/users/profile/` endpoint anymore**. It must be done through the password reset flow.

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

    EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
    # Replace the above with a real email backend if needed
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

## API Documentation
- Swagger: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`

## Authentication Flow
- Register → Verify email → Login
- Add/change email → Verify new email
- Forgot password → Request password reset → Check email → Reset password

## Testing
For testing email verification and password reset in development, console email backend is used. Emails will appear in the terminal.