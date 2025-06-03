# 📦 Customer Registry API

A Django RESTful API that allows authenticated users to perform CRUD operations on Customer data using JWT authentication and PostgreSQL as the database.

---

## 📌 Features

- User Registration & JWT Authentication
- Protected CRUD APIs for Customer entity
- PostgreSQL database integration
- Input validation and error handling
- Optional: Search and Pagination (if implemented)

---

## 🛠️ Tech Stack

- **Backend**: Django, Django REST Framework
- **Authentication**: JWT (`djangorestframework-simplejwt`)
- **Database**: PostgreSQL
- **Tools**: Postman, Git, GitHub

---

## 📁 Project Structure
customer_registry/
├── customers/                        # Customer CRUD logic
│   ├── models.py                     # Customer model
│   ├── serializers.py                # Customer serializers
│   ├── views.py                      # Customer views (CRUD)
│   ├── urls.py                       # Customer API routes

├── users/                            # User registration & authentication
│   ├── models.py                     # Custom user model 
│   ├── serializers.py                # User serializers (registration, login)
│   ├── views.py                      # User registration/auth views
│   ├── urls.py                       # User auth API routes
│   ├── authentication.py             # Custom cookie-based JWT authentication class
│   ├── backends.py                   # Custom Auth Backends class to handle custom authentication
│   ├── middleware.py                 # Custom middleware for JWT token refresh

├── customer_registry/                # Main project configuration
│   ├── settings.py                   # Django settings (env, JWT config, etc.)
│   ├── urls.py                       # Root project URL conf

├── manage.py                 # Django CLI entry point
├── requirements.txt          # Project dependencies
├── .env                      # Environment variables (ignored in Git)
├── .gitignore                # Git ignore rules
├── README.md                 # Project documentation


---

## ⚙️ Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Ukartika567/Customer_Registry.git
cd Customer_Registry 
```

### 2. Create Virtual Environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

### 3. Install Requirements
pip install -r requirements.txt

### 4. Setup .env File
-- Create a .env file using .env.example:
```bash
cp .env.example .env
OR 
directly create file with name .env

-- Add your environment-specific values like:
# Project Config
DEBUG=True
SECRET_KEY=your-secret-key
# Database Config
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
# JWT Token Config
JWT_ACCESS_TOKEN_LIFETIME = your_jwt_access_token_lifetime_in_minute
JWT_REFRESH_TOKEN_LIFETIME = your_jwt_refresh_token_lifetime_in_day
JWT_ALGORITHM = your_jwt_algo (deafult:HS256)

### 🔐 SECRET_KEY
This project uses Django's `SECRET_KEY` from the `.env` file.  
For testing or local development.
If you'd like to generate your own key:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

## 🗄️ PostgreSQL Setup

Make sure PostgreSQL is installed and running.

Create Database:
CREATE DATABASE your_db_name;

Note: Add the DB credentials in your .env file as shown above.


### 🚀 Run the Project
python manage.py makemigrations
python manage.py migrate
python manage.py runserver


### 🔐 Authentication Endpoints
Method	Endpoint	          Description
POST	/api/register/	      Register a new user
POST	/api/token/	          Get JWT access + refresh
POST	/api/token/refresh/	  Refresh access token

###  👤 Customer CRUD Endpoints (JWT Protected)
Method	Endpoint	               Description
POST	/api/customers/	           Create a customer
GET	    /api/customers/	           List all customers
GET	    /api/customers/<id>/	   Retrieve a customer
PUT	    /api/customers/<id>/	   Update a customer
DELETE	/api/customers/<id>/	   Delete a customer

⚠️ All above endpoints require a valid JWT in the Authorization header:
For header-based auth:
Authorization: Bearer <access_token>

For cookie-based auth:
Set credentials: 'include' in frontend requests.


### 🔎 Features implemented
Search customers by name or email using query params.
Pagination for listing customers.

### 📬 Postman Collection
🔗 View Postman Collection
Postman collection is included in the this link. Import it into Postman to test the API easily.


## 🔒 This project uses **secure cookie-based JWT authentication**.  
All auth-protected requests must include `credentials: true` to allow the browser to send cookies automatically.
