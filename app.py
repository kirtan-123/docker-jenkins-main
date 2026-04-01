import sqlite3
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "students.db"

app = Flask(__name__, template_folder=".")


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                department TEXT NOT NULL,
                semester TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def fetch_students():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT id, name, email, phone, department, semester, created_at
            FROM students
            ORDER BY id DESC
            LIMIT 10
            """
        ).fetchall()
    return rows


@app.route("/")
def home():
    students = fetch_students()
    saved = request.args.get("saved") == "1"
    return render_template("index.html", students=students, saved=saved)


@app.route("/students", methods=["GET"])
def students_page():
    return redirect(url_for("home"))


@app.route("/student", methods=["GET"])
def student_page_alias():
    return redirect(url_for("home"))


@app.route("/students", methods=["POST"])
def add_student():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    department = request.form.get("department", "").strip()
    semester = request.form.get("semester", "").strip()

    if not all([name, email, phone, department, semester]):
        return redirect(url_for("home"))

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO students (name, email, phone, department, semester)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, email, phone, department, semester),
        )
        conn.commit()

    return redirect(url_for("home", saved=1))

@app.route("/about")
def about():
    return "This is deployed using Jenkins and Docker on AWS EC2"


@app.errorhandler(404)
def page_not_found(_error):
    return redirect(url_for("home"))


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
