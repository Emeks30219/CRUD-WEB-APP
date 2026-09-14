import os
import re
import pymysql
from flask import Flask, render_template, request, redirect, flash, Response
from dotenv import load_dotenv
from fpdf import FPDF

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-in-your-.env-file")

# Database connection helper using PyMySQL DictCursor
def get_db_connection():
    return pymysql.connect(
        host=os.environ.get("MYSQLHOST", os.environ.get("MYSQL_HOST", "localhost")),
        user=os.environ.get("MYSQLUSER", os.environ.get("MYSQL_USER", "root")),
        password=os.environ.get("MYSQLPASSWORD", os.environ.get("MYSQL_PASSWORD", "")),
        database=os.environ.get("MYSQLDATABASE", os.environ.get("MYSQL_DB", "railway")),
        port=int(os.environ.get("MYSQLPORT", os.environ.get("MYSQL_PORT", 3306))),
        cursorclass=pymysql.cursors.DictCursor
    )

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_student_form(name, email, matric_number, department, faculty):
    """Checks every field before it ever reaches the database.
    Returns a list of error messages - empty list means everything is valid."""
    errors = []

    if not name or len(name.strip()) < 2:
        errors.append("Name must be at least 2 characters long.")

    if not email or not EMAIL_PATTERN.match(email):
        errors.append("Please enter a valid email address.")

    if not matric_number or len(matric_number.strip()) < 3:
        errors.append("Matric number looks too short - please check it.")

    if not department or len(department.strip()) < 2:
        errors.append("Department is required.")

    if not faculty or len(faculty.strip()) < 2:
        errors.append("Faculty is required.")

    return errors


def matric_number_exists(matric_number, exclude_id=None):
    """Checks the database for a student who already has this matric number.
    exclude_id lets an edit ignore the student's own current record."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            if exclude_id:
                cur.execute(
                    "SELECT id FROM students WHERE matric_number = %s AND id != %s",
                    (matric_number, exclude_id),
                )
            else:
                cur.execute("SELECT id FROM students WHERE matric_number = %s", (matric_number,))
            result = cur.fetchone()
            return result is not None
    finally:
        conn.close()


@app.route("/")
def index():
    search_term = request.args.get("q", "").strip()
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            if search_term:
                like_pattern = f"%{search_term}%"
                cur.execute(
                    """SELECT * FROM students
                       WHERE name LIKE %s OR department LIKE %s OR faculty LIKE %s
                       ORDER BY name ASC""",
                    (like_pattern, like_pattern, like_pattern),
                )
            else:
                cur.execute("SELECT * FROM students ORDER BY name ASC")

            students = cur.fetchall()
        return render_template("index.html", students=students, search_term=search_term)
    finally:
        conn.close()


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        matric_number = request.form.get("matric_number", "").strip()
        department = request.form.get("department", "").strip()
        faculty = request.form.get("faculty", "").strip()

        errors = validate_student_form(name, email, matric_number, department, faculty)

        if not errors and matric_number_exists(matric_number):
            errors.append("A student with this matric number already exists.")

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template(
                "add.html",
                name=name, email=email, matric_number=matric_number,
                department=department, faculty=faculty,
            )

        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO students (name, email, matric_number, department, faculty) VALUES (%s, %s, %s, %s, %s)",
                    (name, email, matric_number, department, faculty),
                )
            conn.commit()
            flash(f"{name} was added successfully.", "success")
            return redirect("/")
        finally:
            conn.close()

    return render_template("add.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db_connection()
    try:
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip()
            matric_number = request.form.get("matric_number", "").strip()
            department = request.form.get("department", "").strip()
            faculty = request.form.get("faculty", "").strip()

            errors = validate_student_form(name, email, matric_number, department, faculty)

            if not errors and matric_number_exists(matric_number, exclude_id=id):
                errors.append("Another student already has this matric number.")

            if errors:
                for error in errors:
                    flash(error, "error")
                fallback_student = {
                    "id": id,
                    "name": name,
                    "email": email,
                    "matric_number": matric_number,
                    "department": department,
                    "faculty": faculty
                }
                return render_template("edit.html", student=fallback_student)

            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE students SET name=%s, email=%s, matric_number=%s, department=%s, faculty=%s WHERE id=%s",
                    (name, email, matric_number, department, faculty, id),
                )
            conn.commit()

            flash(f"{name}'s record was updated successfully.", "success")
            return redirect("/")

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM students WHERE id = %s", (id,))
            student = cur.fetchone()

        if student is None:
            flash("That student record could not be found.", "error")
            return redirect("/")

        return render_template("edit.html", student=student)
    finally:
        conn.close()


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT name FROM students WHERE id = %s", (id,))
            student = cur.fetchone()

            cur.execute("DELETE FROM students WHERE id = %s", (id,))
        conn.commit()

        if student:
            flash(f"{student['name']} was deleted.", "success")
        return redirect("/")
    finally:
        conn.close()


@app.route("/analytics")
def analytics():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT department, COUNT(*) AS count FROM students GROUP BY department ORDER BY count DESC")
            by_department_dict = cur.fetchall()

            cur.execute("SELECT faculty, COUNT(*) AS count FROM students GROUP BY faculty ORDER BY count DESC")
            by_faculty_dict = cur.fetchall()

            cur.execute("SELECT COUNT(*) AS total FROM students")
            total_students = cur.fetchone()["total"]

        # Convert dictionary rows to tuples so templates expecting row[0]/row[1] continue working seamlessly
        by_department = [(row["department"], row["count"]) for row in by_department_dict]
        by_faculty = [(row["faculty"], row["count"]) for row in by_faculty_dict]

        max_department_count = max([row[1] for row in by_department], default=1)
        max_faculty_count = max([row[1] for row in by_faculty], default=1)

        return render_template(
            "analytics.html",
            by_department=by_department,
            by_faculty=by_faculty,
            total_students=total_students,
            max_department_count=max_department_count,
            max_faculty_count=max_faculty_count,
        )
    finally:
        conn.close()


@app.route("/export/pdf")
def export_pdf():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM students ORDER BY name ASC")
            students = cur.fetchall()
    finally:
        conn.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 12, "Student Records", ln=True, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.ln(4)

    headers = ["ID", "Name", "Email", "Matric No.", "Department", "Faculty"]
    col_widths = [12, 38, 50, 28, 32, 32]

    pdf.set_font("Helvetica", "B", 9)
    for header, width in zip(headers, col_widths):
        pdf.cell(width, 8, header, border=1)
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)
    for student in students:
        row = [
            str(student["id"]),
            str(student["name"]),
            str(student["email"]),
            str(student["matric_number"]),
            str(student["department"]),
            str(student["faculty"])
        ]
        for value, width in zip(row, col_widths):
            pdf.cell(width, 8, value[:width], border=1)
        pdf.ln()

    pdf_bytes = bytes(pdf.output())

    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={"Content-Disposition": "attachment; filename=student_records.pdf"},
    )


if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "False") == "True"
    app.run(debug=debug_mode)
