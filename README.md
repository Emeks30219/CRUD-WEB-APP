# Student Management System (Flask + MySQL CRUD App)

A full CRUD (Create, Read, Update, Delete) web application built with Flask and MySQL for managing student records — deployed live, with search, PDF export, an analytics dashboard, and server-side validation.

**Live app:** https://crud-web-app-production-d90e.up.railway.app/

## Overview

This project started as a first-ever Flask + SQL build with no prior web development experience — plain, unstyled HTML templates focused purely on backend logic. It has since grown into a genuinely production-shaped application: a security fix (debug mode, environment-based secrets), real feature additions, a full interface redesign, and a working live deployment on Railway with a connected MySQL database.

## Features

- **Create** — Add a new student record, with server-side validation on every field
- **Read** — View all students, with live search by name, department, or faculty
- **Update** — Edit an existing student's information, with duplicate matric-number protection
- **Delete** — Remove a record, protected behind a POST request (not a plain link) to prevent accidental or automated deletion
- **PDF export** — Download the full student list as a formatted PDF
- **Analytics dashboard** — Visual breakdown of students by department and faculty
- **Flash messages** — Clear success/error feedback after every action
- A distinct grid-tech visual interface across all pages, sharing one design language with a unique accent color per screen

## Security

- Debug mode is off by default, controlled by an environment variable — never hardcoded on
- Database credentials and the app's secret key are loaded from environment variables, never committed to the repository
- All database queries use parameterized statements (no raw string SQL), protecting against SQL injection
- Delete requires a POST request with a confirmation prompt, not a plain clickable link
- Matric numbers are enforced unique both at the application level and the database level

## Tech stack

Python · Flask · MySQL · Jinja2 · fpdf2 (PDF export) · Railway (hosting + database)

## Project structure

```
CRUD-WEB-APP/
├── app.py
├── index.html
├── add.html
├── edit.html
├── analytics.html
├── requirements.txt
├── Procfile
└── .gitignore
```

## Running it locally

```bash
pip install -r requirements.txt
```

Create a `.env` file (never committed) with:
```
MYSQL_HOST=your-host
MYSQL_PORT=your-port
MYSQL_USER=your-user
MYSQL_PASSWORD=your-password
MYSQL_DB=your-database-name
SECRET_KEY=a-long-random-string
FLASK_DEBUG=False
```

Then:
```bash
python app.py
```

## Deployment

Deployed on **Railway**, with both the Flask app and its MySQL database hosted in the same project — database connection details are injected automatically via Railway's reference variables, rather than copied by hand between separate services.

## What I'd improve next

- Native-speaker-style review of form validation edge cases
- Automated tests for the database-facing routes
- Pagination for the student list once it grows past a page or two
