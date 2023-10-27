# library-service-api

Library API Service is a Django-based RESTful API for managing books borrowing and more. It optimizes the work of library administrators and make the service much more user-friendly.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Endpoints](#endpoints)
- [Presentation](#presentation)

## Introduction

Library API Service is designed to streamline the management of library-related data and user interactions.

### Features:
- Web-based
- Manage books inventory
- Manage books borrowing
- Manage customers
- Display notifications
- Handle payments
## Installation

1. Clone the repository:

   ```
   git clone https://github.com/MarianKovalyshyn/library-service-api.git
   ```
2. Create .env file and define environmental variables following .env.example:
   ```
   POSTGRES_HOST= your db host
   POSTGRES_DB= name of your db
   POSTGRES_USER= username of your db user
   POSTGRES_PASSWORD= your db password
   SECRET_key=" your django secret key "
   ```
3. Run command:
   ```
   docker-compose up --build
   ```
4. App will be available at: ```127.0.0.1:8000```
5. Login using next credentials:
   ```
   admin@gmail.com
   creds
   ```
## Endpoints
   ```
   "book_service" : 
                "http://127.0.0.1:8000/api/book-service/books/"

   "borrowing_service" : 
                   "http://127.0.0.1:8000/api/borrowing-service/borrowings/"
                   "http://127.0.0.1:8000/api/borrowing-service/borrowings/{id}/return_borrowing/"
                   "http://127.0.0.1:8000/api/user/token/"
                   "http://127.0.0.1:8000/api/user/token/refresh/"
   "customers_service": 
                   "http://127.0.0.1:8000/api/doc/"
                   "http://127.0.0.1:8000/api/swagger/"
                   "http://127.0.0.1:8000/api/redoc/"

   "notifications_service" : 
                   "http://127.0.0.1:8000/api/user/register/"
                   "http://127.0.0.1:8000/api/user/me/"
                   "http://127.0.0.1:8000/api/user/token/"
                   "http://127.0.0.1:8000/api/user/token/refresh/"
   "payment_service": 
                   "http://127.0.0.1:8000/api/payment-service/payments/"
  
   "documentation": 
                   "http://127.0.0.1:8000/api/doc/"
                   "http://127.0.0.1:8000/api/swagger/"
                   "http://127.0.0.1:8000/api/redoc/"                                          
   ```

## Architecture
![architecture.jpg](media/architecture.jpg)

## Presentation
![swagger.png](media/swagger.png)
