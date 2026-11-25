
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection
def get_db():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create database table
def create_table():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Home page
@app.route("/")
def index():
    conn = get_db()
    students = conn.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return render_template("index.html", students=students)

# Add student
@app.route("/add", methods=["POST"])
def add_student():
    name = request.form["name"]
    email = request.form["email"]
    course = request.form["course"]
    age = request.form["age"]

    conn = get_db()
    conn.execute(
        "INSERT INTO students (name, email, course, age) VALUES (?, ?, ?, ?)",
        (name, email, course, age)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

# Edit student
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    conn = get_db()

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]
        age = request.form["age"]

        conn.execute("""
            UPDATE students
            SET name=?, email=?, course=?, age=?
            WHERE id=?
        """, (name, email, course, age, id))

        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    student = conn.execute(
        "SELECT * FROM students WHERE id=?", (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return "Student not found", 404

    return render_template("edit.html", student=student)

# Delete student
@app.route("/delete/<int:id>", methods=["POST"])
def delete_student(id):
    conn = get_db()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

if __name__ == "__main__":
    create_table()
    app.run(debug=True)
