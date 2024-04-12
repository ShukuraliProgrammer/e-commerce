# Bu E-Commerce Loyiha

## 1 - step 
**Clone the project from github**
```bash
git clone  https://github.com/ShukuraliProgrammer/e-commerce.git
```

## 2-step
**Enter the project directory**

## 3-step
**Create a virtual environment**
```bash
python3 -m venv venv
```

## 4-step
**Activate the virtual environment**
```bash
> For Linux
source venv/bin/activate 

> For Windows
venv\Scripts\activate
```


## 5-step
**Create Database in you local machine**
```bash
- sudo -i -u postgres
- psql
- CREATE DATABASE e_commerce;
- CREATE USER e_commerce WITH PASSWORD 'e_commerce';
- ALTER ROLE e_commerce SET client_encoding TO 'utf8';
- ALTER ROLE e_commerce SET default_transaction_isolation TO 'read committed';
- ALTER ROLE e_commerce SET timezone TO 'UTC';
- GRANT ALL PRIVILEGES ON DATABASE e_commerce TO e_commerce;
```

## 6-step
**Generate a secret key**
```bash
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

## 7- step
**Create `.env` file and paste all credentials that copied from `.env.example` like below, put in above generated secret key to `SECRET_KEY` variable**
```bash
# Base Configuration
SECRET_KEY=key
DEBUG=True
ALLOWED_HOSTS=127.0.0.0.1, localhost

# Database Configuration
DB_NAME=e_commerce
DB_USER=e_commerce
DB_PASSWORD=e_commerce
DB_HOST=localhost
DB_PORT=5432
```

## 8-step
**Install all requirements**
```bash
pip install -r requirements/develop.txt
```

## 9-step
**Migrate the database**
```bash
python manage.py migrate
```

## 10-step
**Create superuser**
```bash
python manage.py createsuperuser
```

## 11-step
**Run the project**
```bash
python manage.py runserver
```
