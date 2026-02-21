from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from scraper import scrape_all
from datetime import datetime, timedelta
app = Flask(__name__)
app.secret_key = "ivyintel_secret_key"

DB_PATH = "database/ivyintel.db"


# DATABASE CONNECTION
def connect_db():
    return sqlite3.connect(DB_PATH)


# HOME PAGE → LOGIN PAGE
@app.route("/")
def home():
    
    return render_template("login.html")
@app.route("/fetch")
def fetch():

    if "user" not in session:
        return redirect("/")

    # Run scraper
    scrape_all()

    # Increase InCoScore for fetching new data
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET incoscore = incoscore + 10 WHERE email=?",
        (session["user"],)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")
# SIGNUP PAGE
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        interest = request.form["interest"]

        conn = connect_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (name, email, password, interest) VALUES (?, ?, ?, ?)",
                (name, email, password, interest)
            )
            conn.commit()

        except:
            return "User already exists"

        conn.close()

        return redirect("/")

    return render_template("signup.html")


# LOGIN ROUTE
@app.route("/login", methods=["POST"])
def login():

    email = request.form["email"]
    password = request.form["password"]

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    if user and check_password_hash(user[3], password):

        session["user"] = user[2]

        return redirect("/dashboard")

    else:
        return "Invalid login credentials"

LOGOS = {
    "Harvard": "logos/harvard.png",
    "Yale": "logos/yale.png",
    "Princeton": "logos/princeton.png",
    "Columbia": "logos/columbia.png",
    "UPenn": "logos/upenn.png"
}
# DASHBOARD
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    if "user" not in session:
        return redirect("/")

    # If form submitted, save filters in session
    if request.method == "POST":
        session["selected_university"] = request.form.get("university")
        session["selected_category"] = request.form.get("category")

    # Read filters from session
    university = session.get("selected_university")
    category = session.get("selected_category")

    conn = connect_db()
    cursor = conn.cursor()

    query = """
        SELECT id, title, university, category, deadline, link, created_at
        FROM opportunities
        WHERE 1=1
    """
    params = []

    if university:
        query += " AND university=?"
        params.append(university)

    if category:
        query += " AND category=?"
        params.append(category)

    query += " ORDER BY created_at DESC"

    cursor.execute(query, params)
    opportunities = cursor.fetchall()

    last_updated = None

    if opportunities:

        utc_time = datetime.strptime(opportunities[0][6], "%Y-%m-%d %H:%M:%S")

        ist_time = utc_time + timedelta(hours=5, minutes=30)

        last_updated = ist_time.strftime("%Y-%m-%d %H:%M:%S")
    conn.close()

    LOGOS = {
        "Harvard": "logos/harvard.png",
        "Yale": "logos/yale.png",
        "Princeton": "logos/princeton.png",
        "Columbia": "logos/columbia.png",
        "UPenn": "logos/upenn.png"
    }

    selected_logo = LOGOS.get(university)
    # Get user interest
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT interest FROM users WHERE email=?",
        (session["user"],)
    )

    user_interest = cursor.fetchone()[0]

    # Get recommended opportunities
    cursor.execute("""
    SELECT id, title, university, category, deadline, link, created_at
    FROM opportunities
    WHERE LOWER(category) = LOWER(?)
    ORDER BY created_at DESC
    LIMIT 5
    """, (user_interest,))

    recommended = cursor.fetchall()

# fallback if empty
    if not recommended:

        cursor.execute("""
        SELECT id, title, university, category, deadline, link, created_at
        FROM opportunities
        ORDER BY created_at DESC
        LIMIT 5
        """)

        recommended = cursor.fetchall()

    # Fetch InCoScore
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT incoscore FROM users WHERE email=?",
        (session["user"],)
    )

    incoscore = cursor.fetchone()[0]

    conn.close()
    return render_template(
        "dashboard.html",
        opportunities=opportunities,
        recommended=recommended,
        logos=LOGOS,
        incoscore=incoscore,
        selected_university=university,
        selected_category=category,
        selected_logo=selected_logo,
        last_updated=last_updated
    )
# LOGOUT
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")
@app.route("/opportunity/<int:opp_id>")
@app.route("/opportunity/<int:opp_id>")
def opportunity_detail(opp_id):

    if "user" not in session:
        return redirect("/")

    conn = connect_db()
    cursor = conn.cursor()

    # Fetch opportunity
    cursor.execute("""
        SELECT id, title, university, category,
               description, deadline, link, created_at
        FROM opportunities
        WHERE id = ?
    """, (opp_id,))

    opp = cursor.fetchone()

    if opp is None:
        conn.close()
        return "Opportunity not found"

    # Increase InCoScore when user views opportunity
    cursor.execute(
        "UPDATE users SET incoscore = incoscore + 5 WHERE email=?",
        (session["user"],)
    )

    conn.commit()

    conn.close()

    LOGOS = {
        "Harvard": "logos/harvard.png",
        "Yale": "logos/yale.png",
        "Princeton": "logos/princeton.png",
        "Columbia": "logos/columbia.png",
        "UPenn": "logos/upenn.png"
    }

    logo = LOGOS.get(opp[2])

    return render_template(
        "opportunity_detail.html",
        opp=opp,
        logo=logo
    )
# RUN SERVER
if __name__ == "__main__":
    app.run(debug=True)