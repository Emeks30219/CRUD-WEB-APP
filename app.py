from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""  # XAMPP default password is blank
app.config["MYSQL_DB"] = "student_db"  # Matches your phpMyAdmin database name

mysql = MySQL(app)


@app.route("/")
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")  # Asks MySQL for all rows inside the students table
    students = cur.fetchall()  # Captures all rows into a Python variable
    cur.close()  # Closes the database request connection
    return render_template("index.html", students=students)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":  # This runs ONLY when the user clicks 'Save Record'
        name = request.form["name"]
        email = request.form["email"]
        matric_number = request.form["matric_number"]
        department = request.form["department"]
        faculty = request.form["faculty"]

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO students (name, email, matric_number, department, faculty) VALUES (%s, %s, %s, %s, %s)",
            (name, email, matric_number, department, faculty)
        )
        mysql.connection.commit()  # Tells XAMPP to permanently save the changes
        cur.close()
        return redirect("/")  # Bounces the user back to the homepage list
    return render_template("add.html")  # Runs if the user is just opening the empty form


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    cur = mysql.connection.cursor()
    if request.method == "POST":  # Runs when the user clicks 'Update Details'
        name = request.form["name"]
        email = request.form["email"]
        matric_number = request.form["matric_number"]
        department = request.form["department"]
        faculty = request.form["faculty"]

        cur.execute(
            "UPDATE students SET name=%s, email=%s, matric_number=%s, department=%s, faculty=%s WHERE id=%s",
            (name, email, matric_number, department, faculty, id)
        )
        mysql.connection.commit()
        cur.close()
        return redirect("/")

    cur.execute("SELECT * FROM students WHERE id = %s", (id,))
    student = cur.fetchone()
    cur.close()
    return render_template("edit.html", student=student)


@app.route("/delete/<int:id>", methods=["GET"])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id = %s", (id,))  # Deletes row matching this unique ID
    mysql.connection.commit()
    cur.close()
    return redirect("/")  # Returns to the updated homepage list


if __name__ == "__main__":
    app.run(debug=True)
