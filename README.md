# Vending Machine Site for LHR16

The vending_machine project is a Django-based web application designed specifically for Amazon's LHR16 facility. This application manages and simulates the dispensing of items from vending machines located within the facility. Whether it's essential tools, safety equipment, or stationery, the application ensures that Amazon employees have quick and efficient access to the items they need.

## Features

- Display available items with their details.
- Handle user registration and authentication.
- Process payments for selected items.
- Track purchase history for each user.
- Admin dashboard to view usage trends.

## Setup and Run Locally

### Prerequisites

- Python

### Installation

1. Clone the repository:

```bash
git clone https://github.com/maishams/VendingMachine
cd vending_machine
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Set environment variables
You will need to set the below variables in order to run the app locally. 
Note: if you do not have the secret key, refer to [this](https://stackoverflow.com/questions/41298963/is-there-a-function-for-generating-settings-secret-key-in-django)
```bash
export DJANGO_SECRET_KEY=<secretkey>
export TESTING=TRUE
```

3. Set up the database:

The project uses SQLite as its database if run locally. To set it up, run:

```bash
python manage.py migrate
```

This will create a `db.sqlite3` file in the project directory. 

### Running the Application

To run the application, use the `manage.py` script:

```bash
python3 manage.py runsslserver
```

The application will be accessible at `http://127.0.0.1:8000/`.

### Running Tests

The project contains tests for models, views, and admin functionalities. To run the tests, use:

```bash
python manage.py test
```

## Configuration

The project's settings can be found in `VendingMachine/settings.py`. Here you can configure various aspects of the application, such as:

- Installed apps
- Middleware
- Database settings
- Static and media file paths

## Database Models

The project defines two main models:

1. `Item`: Represents each equipment item in the vending machine. Fields include item type, description, price, quantity, and image.
2. `History`: Keeps track of equipment purchase history for each user.

## Views and URLs

The application's views are defined in `item/views.py` and the corresponding URLs in `item/urls.py`. The main views include:

- Index page displaying all items.
- Payment page for a specific item.
- User registration and login pages.
- User account page displaying purchase history.
- Admin dashboard showing usage trends.