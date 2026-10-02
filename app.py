from flask import Flask, render_template, request, redirect
import sqlite3
import string
import random
from urllib.parse import urlparse


app = Flask(__name__)


# ============================================================
# DATABASE
# ============================================================

def create_database():
    connection = sqlite3.connect("urls.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT UNIQUE NOT NULL,
            clicks INTEGER DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()


# ============================================================
# GENERATE SHORT CODE
# ============================================================

def generate_short_code(length=6):

    characters = string.ascii_letters + string.digits

    short_code = ''.join(
        random.choice(characters)
        for _ in range(length)
    )

    return short_code


# ============================================================
# GET TOTAL URL COUNT
# ============================================================

def get_total_urls():

    connection = sqlite3.connect("urls.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM urls")

    total_urls = cursor.fetchone()[0]

    connection.close()

    return total_urls


# ============================================================
# GET TOTAL CLICK COUNT
# ============================================================

def get_total_clicks():

    connection = sqlite3.connect("urls.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COALESCE(SUM(clicks), 0) FROM urls"
    )

    total_clicks = cursor.fetchone()[0]

    connection.close()

    return total_clicks


# ============================================================
# HOME PAGE / DASHBOARD
# ============================================================

@app.route("/")
def home():

    total_urls = get_total_urls()
    total_clicks = get_total_clicks()

    return render_template(
        "index.html",
        total_urls=total_urls,
        total_clicks=total_clicks
    )


# ============================================================
# SHORTEN URL
# ============================================================

@app.route("/shorten", methods=["POST"])
def shorten_url():

    # Get URL from form
    original_url = request.form["url"].strip()

    # --------------------------------------------------------
    # URL VALIDATION
    # --------------------------------------------------------

    parsed_url = urlparse(original_url)

    if parsed_url.scheme not in ["http", "https"] or not parsed_url.netloc:

        return render_template(
            "index.html",
            error="Please enter a valid URL.",
            total_urls=get_total_urls(),
            total_clicks=get_total_clicks()
        )

    # --------------------------------------------------------
    # CONNECT TO DATABASE
    # --------------------------------------------------------

    connection = sqlite3.connect("urls.db")
    cursor = connection.cursor()

    # --------------------------------------------------------
    # CHECK DUPLICATE URL
    # --------------------------------------------------------

    cursor.execute(
        "SELECT short_code FROM urls WHERE original_url = ?",
        (original_url,)
    )

    existing_url = cursor.fetchone()

    if existing_url:

        short_code = existing_url[0]

        connection.close()

        short_url = request.host_url + short_code

        return render_template(
            "index.html",
            short_url=short_url,
            message="This URL was already shortened.",
            total_urls=get_total_urls(),
            total_clicks=get_total_clicks()
        )

    # --------------------------------------------------------
    # GENERATE UNIQUE SHORT CODE
    # --------------------------------------------------------

    while True:

        short_code = generate_short_code()

        cursor.execute(
            "SELECT id FROM urls WHERE short_code = ?",
            (short_code,)
        )

        existing_code = cursor.fetchone()

        if existing_code is None:
            break

    # --------------------------------------------------------
    # SAVE URL TO DATABASE
    # --------------------------------------------------------

    cursor.execute(
        """
        INSERT INTO urls
        (original_url, short_code)
        VALUES (?, ?)
        """,
        (original_url, short_code)
    )

    connection.commit()
    connection.close()

    # --------------------------------------------------------
    # CREATE SHORT URL
    # --------------------------------------------------------

    short_url = request.host_url + short_code

    # --------------------------------------------------------
    # SHOW RESULT
    # --------------------------------------------------------

    return render_template(
        "index.html",
        short_url=short_url,
        total_urls=get_total_urls(),
        total_clicks=get_total_clicks()
    )


# ============================================================
# REDIRECT SHORT URL
# ============================================================

@app.route("/<short_code>")
def redirect_url(short_code):

    connection = sqlite3.connect("urls.db")
    cursor = connection.cursor()

    # Find original URL
    cursor.execute(
        """
        SELECT original_url, clicks
        FROM urls
        WHERE short_code = ?
        """,
        (short_code,)
    )

    result = cursor.fetchone()

    # --------------------------------------------------------
    # URL NOT FOUND
    # --------------------------------------------------------

    if result is None:

        connection.close()

        return "URL not found", 404

    # --------------------------------------------------------
    # GET URL DETAILS
    # --------------------------------------------------------

    original_url = result[0]
    clicks = result[1]

    # --------------------------------------------------------
    # INCREASE CLICK COUNT
    # --------------------------------------------------------

    cursor.execute(
        """
        UPDATE urls
        SET clicks = ?
        WHERE short_code = ?
        """,
        (clicks + 1, short_code)
    )

    connection.commit()
    connection.close()

    # --------------------------------------------------------
    # REDIRECT USER
    # --------------------------------------------------------

    return redirect(original_url)


# ============================================================
# URL HISTORY
# ============================================================

@app.route("/history")
def history():

    connection = sqlite3.connect("urls.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT original_url, short_code, clicks
        FROM urls
        ORDER BY id DESC
        """
    )

    urls = cursor.fetchall()

    connection.close()

    return render_template(
        "history.html",
        urls=urls
    )


# ============================================================
# DELETE URL
# ============================================================

@app.route("/delete/<short_code>", methods=["POST"])
def delete_url(short_code):

    connection = sqlite3.connect("urls.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM urls
        WHERE short_code = ?
        """,
        (short_code,)
    )

    connection.commit()
    connection.close()

    return redirect("/history")


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    create_database()

    app.run(
        debug=True
    )