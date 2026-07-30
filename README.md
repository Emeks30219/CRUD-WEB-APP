# Student Management System (Flask + MySQL CRUD App)

A full CRUD (Create, Read, Update, Delete) web application built with Flask and MySQL for managing student records. The frontend uses plain HTML only — no CSS — keeping the focus on backend logic, routing, and database operations.

## Overview

This project was built from the ground up with no prior experience in Flask, SQL, or web development. It demonstrates a complete web application flow: a Flask server handling HTTP requests, a MySQL database storing student data, and HTML templates rendering the results — all wired together with basic routing and forms.

## Features

- **Create** — Add a new student record via an HTML form
- **Read** — View a list of all students, and view individual student details
- **Update** — Edit an existing student's information
- **Delete** — Remove a student record from the database
- Plain, unstyled HTML templates (no CSS) so the structure and logic of the app are front and center

## Tech Stack

- **Backend:** Python, Flask
- **Database:** MySQL
- **Frontend:** HTML (Jinja2 templating via Flask, no CSS)
- **Connector:** `flask-mysqldb` or `mysql-connector-python`

## Requirements

```
flask
flask-mysqldb
```
*(or `mysql-connector-python`, depending on which connector is used)*

Install with:
```bash
pip install flask flask-mysqldb
```

## Database Setup

1. Create a MySQL database, e.g. `student_db`.
2. Create a `students` table:
   ```sql
   CREATE TABLE students (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(100) NOT NULL,
       email VARCHAR(100),
       course VARCHAR(100),
       age INT
   );
   ```
3. Update the database credentials (host, user, password, database name) in the app's config section.

## Usage

```bash
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

### Routes

| Route | Method | Description |
|---|---|---|
| `/` | GET | List all students |
| `/add` | GET, POST | Form to add a new student |
| `/edit/<id>` | GET, POST | Form to update a student's details |
| `/delete/<id>` | GET/POST | Delete a student record |

*(Adjust route names/paths above to match your actual `app.py` if they differ.)*

## Project Structure

```
student-management-system/
├── app.py                # Flask application and routes
├── templates/
│   ├── index.html        # List of students
│   ├── add.html          # Add student form
│   └── edit.html         # Edit student form
└── requirements.txt
```

## Key Concepts Demonstrated

- Flask routing and request handling (GET/POST)
- Jinja2 templating for dynamic HTML rendering
- MySQL CRUD operations via Python
- Basic form handling and data validation
- Connecting a Python backend to a relational database end-to-end

## Project Background

Built as a graded university assignment, including a full technical defense/viva explaining the architecture, database schema, and code decisions — completed with zero prior background in web development or SQL.

## Author

Emeka — Computer Science student, Bingham University
GitHub: [Emeks30219](https://github.com/Emeks30219)
