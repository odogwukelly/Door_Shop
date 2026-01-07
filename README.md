# Door Shop
A simple Flask-based e-commerce application with separate admin and customer areas. The app uses SQLAlchemy for the database, Flask-Login for authentication, Stripe for payments, and supports product management (images, categories), orders, and basic admin dashboards.
https://github.com/odogwukelly/Door_Shop

## Features
+ Admin dashboard to manage products, categories and orders
+ Customer-facing pages for browsing products and placing orders
+ Image upload and processing for product images
+ Authentication with Flask-Login and password hashing (Flask-Bcrypt)
+ Database models via Flask-SQLAlchemy
+ Stripe integration for payments (requires API keys)

## Tech stack
+ Python, Flask
+ Flask-Login, Flask-Bcrypt, Flask-WTF
+ Flask-SQLAlchemy (SQLAlchemy 2.x)
+ Stripe (stripe Python package)
+ MySQL (mysql-connector / PyMySQL compatible)
+ HTML, CSS, JavaScript for templates and static assets

## Quickstart / Installation
1. Clone the repository git clone https://github.com/odogwukelly/Door_Shop.git cd Door_Shop

2. Create and activate a virtual environment python -m venv venv source venv/bin/activate (macOS / Linux) venv\Scripts\activate (Windows)
3. Install dependencies pip install -r requirements.txt

4. Create a .env file in the project root with at least these variables: SECRET_KEY=your_secret_key DB_URI=your_sqlalchemy_database_uri STRIPE_SECRET_KEY=your_stripe_secret_key STRIPE_PUBLIC_KEY=your_stripe_public_key

    Example DB_URI for MySQL using PyMySQL: DB_URI=mysql+pymysql://db_user:db_password@localhost/door_shop

5. Database setup

    - The repo includes a helper script create_db.py that attempts to create a MySQL database named door_Shop using mysql-connector. That script uses local credentials inside it — update it or run your preferred database creation steps.
    - To create the app tables from models, run: python db.py Note: db.py currently calls db.drop_all() followed by db.create_all() — be careful as this will drop existing tables.
6. Run the app python run.py Then open http://127.0.0.1:5000 in your browser.

## Configuration / Environment variables
+ SECRET_KEY — Flask secret key
+ DB_URI — SQLAlchemy database URI (used by Flask-SQLAlchemy)
+ STRIPE_SECRET_KEY — Stripe secret key for server-side operations
+ STRIPE_PUBLIC_KEY — Stripe public key for client-side forms

Set these in a .env file (python-dotenv is included in requirements). Example:

```
SECRET_KEY=supersecretvalue
DB_URI=mysql+pymysql://user:password@localhost/door_shop
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLIC_KEY=pk_test_...
```

## Project structure (high level)
+ run.py — small launcher for the Flask app
+ config.py — configuration class (loads environment variables)
+ create_db.py — creates database via mysql-connector (local helper)
+ db.py — runs create_all (and currently drops all tables first)
+ requirements.txt — Python dependencies
+ shop/
    + init.py — Flask app, extensions initialised (bcrypt, db, login_manager) and blueprint imports
    + admin/ — admin forms, routes, models (product/category/order management)
    + customer/ — customer forms, routes, models (customer accounts, checkout, orders)
    + static/ — product images and other static files
    + templates/ — Jinja2 templates for admin and customer pages

## Notes & warnings
+ db.py currently drops all tables (db.drop_all()) before creating them. Only run on a development DB or update the script if you want to preserve data.
+ create_db.py contains hard-coded MySQL credentials and attempts to create a DB named door_Shop. Edit it or use your own DB provisioning.
+ Image upload code stores files in static/product_images. Ensure that folder exists and is writable by the application.
+ There are references to Stripe — you must set your Stripe keys to use payment flows.
+ If you plan to deploy, set DEBUG = False and configure SECRET_KEY and DB_URI appropriately; consider using a proper WSGI server (gunicorn is in requirements).

## Admin / Usage
+ Admin pages are available under routes defined in shop/admin/routes.py (dashboard, add-product, all-product, all-customers, etc.). Admin access is guarded by login checks and an is_admin flag on users.
+ Product forms and validation are in shop/admin/form.py.
+ Customer flows (registration/login, product browsing, checkout) live in shop/customer/*.


## Contributing
Contributions are welcome. Suggested steps:

+ Fork the repository
+ Create a feature branch
+ Open a PR with a clear description of changes

Please add tests for new features and follow existing code style.

## License
No license file found in the repository. Add a LICENSE to clarify allowed usage (MIT, Apache-2.0, etc.) if you plan to make this public.

## Troubleshooting
+ DB connection errors: verify DB_URI and that the database server is reachable.
+ Missing dependencies: ensure virtual environment is active, then pip install -r requirements.txt.
+ Image upload errors: check file permissions on static/product_images and the allowed file extensions in forms.

## Author
+ odogwu kelly <odogwukellyice@gmail.com>