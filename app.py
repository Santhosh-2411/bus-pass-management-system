from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "bus_pass_secret_key"


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def create_database():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            full_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            college TEXT NOT NULL,
            phone TEXT NOT NULL,
            source TEXT NOT NULL,
            destination TEXT NOT NULL,
            pass_type TEXT NOT NULL,
            start_date TEXT NOT NULL,
            duration TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO students (name, email, phone, password) VALUES (?, ?, ?, ?)",
                (name, email, phone, password)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "Email already registered!"
        conn.close()
        return redirect("/login")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        conn = get_db_connection()
        student = conn.execute(
            "SELECT * FROM students WHERE email = ? AND password = ?",
            (email, password)
        ).fetchone()
        conn.close()
        if student:
            session["student_id"] = student["id"]
            session["student_name"] = student["name"]
            return redirect("/dashboard")
        return "Invalid email or password!"
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "student_id" not in session:
        return redirect("/login")
    return render_template("dashboard.html", student_name=session["student_name"])


@app.route("/apply", methods=["GET", "POST"])
def apply():
    if "student_id" not in session:
        return redirect("/login")
    if request.method == "POST":
        values = (
            request.form["full_name"], request.form["age"], request.form["gender"],
            request.form["college"], request.form["phone"], request.form["source"],
            request.form["destination"], request.form["pass_type"],
            request.form["start_date"], request.form["duration"]
        )
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO applications
            (student_id, full_name, age, gender, college, phone, source,
             destination, pass_type, start_date, duration, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (session["student_id"], *values, "Pending"))
        conn.commit()
        conn.close()
        return redirect("/applications")
    return render_template("apply.html")


@app.route("/applications")
def applications():
    if "student_id" not in session:
        return redirect("/login")
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT * FROM applications WHERE student_id = ? ORDER BY id DESC",
        (session["student_id"],)
    ).fetchall()
    conn.close()
    return render_template("applications.html", applications=rows)


@app.route("/status")
def status():
    if "student_id" not in session:
        return redirect("/login")
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT * FROM applications WHERE student_id = ? ORDER BY id DESC",
        (session["student_id"],)
    ).fetchall()
    conn.close()
    return render_template("status.html", applications=rows)


@app.route("/my-pass")
def my_pass():
    if "student_id" not in session:
        return redirect("/login")
    conn = get_db_connection()
    approved = conn.execute("""
        SELECT * FROM applications
        WHERE student_id = ? AND status = 'Approved'
        ORDER BY id DESC LIMIT 1
    """, (session["student_id"],)).fetchone()
    conn.close()
    return render_template("my_pass.html", bus_pass=approved)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    create_database()
    app.run(debug=True)
