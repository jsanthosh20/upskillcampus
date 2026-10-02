#  Python URL Shortener

A web-based URL Shortener developed using Python, Flask, SQLite, HTML and CSS.

##  Project Description

The URL Shortener converts long URLs into shorter and more manageable links.

Users can enter a long URL and generate a unique shortened URL. When the shortened URL is opened, the application redirects the user to the original URL.

##  Features

- Generate short URLs
- Validate URLs
- Handle duplicate URLs
- Redirect to original URLs
- Store URL mappings in SQLite
- Track number of clicks
- View URL history
- Search URLs
- Copy shortened URLs
- Delete shortened URLs
- Dashboard statistics

##  Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript

##  Project Structure

URL_Shortener/

    app.py

    urls.db

    templates/
        index.html
        history.html

    static/
        style.css

##  Installation

Clone or download the project.

Create a virtual environment:

    python -m venv venv

Activate the virtual environment:

Windows:

    venv\Scripts\activate

Install dependencies:

    pip install flask

##  Run the Application

Run:

    python app.py

Open the browser and visit:

    http://127.0.0.1:5000

##  Database

The project uses SQLite to store:

- Original URLs
- Short codes
- Click counts

The database is automatically created when the application starts.

## Working

1. User enters a long URL.
2. Application validates the URL.
3. Application checks whether the URL already exists.
4. A unique short code is generated if necessary.
5. The URL mapping is stored in SQLite.
6. The shortened URL is displayed.
7. Opening the shortened URL redirects the user to the original URL.
8. Click count is updated.

##  Project Purpose

This project was developed as part of a Python internship to gain practical experience in Python programming, web development, database handling and application development.