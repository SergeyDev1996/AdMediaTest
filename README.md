# AdMediaTest

AdMediaTest is a Django-based project designed to track and analyze advertisement spend and revenue statistics. This project helps organizations make informed decisions based on comprehensive ad performance data.


## Features

- **Spend Statistics**: Track and analyze advertisement spend data.
- **Revenue Statistics**: Monitor and assess advertisement revenue data.
- **Comprehensive API**: Interact with the system through a robust set of API endpoints.

## Prerequisites

- Python 3.x
- Django 3.x
- Additional packages and dependencies are listed in `requirements.txt`.

## Installation

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/your_username/AdMediaTest.git
2. **Set up the virtual environment:**
   ```sh
   cd AdMediaTest
   python -m venv venv
   source venv/bin/activate  # For Windows use `venv\Scripts\activate`
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
4. **Apply migrations**
   ```sh
   python manage.py migrate
   python manage.py createsuperuser

### Usage
To run the server:
```shell
python manage.py runserver 
```

### Creating Test Data
Execute the create_test_data.py script to populate the database with sample spend and revenue statistics for testing purposes:
```shell
python test_data.py
```

### API Endpoints
```shell
http://127.0.0.1:8000/revenue-statistic/
http://127.0.0.1:8000/spend-statistic/
```