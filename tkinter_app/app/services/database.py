import sqlite3
import os

DB_NAME = "school.db"

def get_connection():
    # Ensure the database file is created in the current working directory
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # Create Students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            dob TEXT,
            gender TEXT,
            grade TEXT,
            contact_number TEXT,
            address TEXT
        )
    """)

    # Create Teachers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            subject TEXT,
            contact_number TEXT,
            email TEXT
        )
    """)

    # Create Classes table (Schedule)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            teacher_id INTEGER,
            schedule_time TEXT,
            FOREIGN KEY(teacher_id) REFERENCES teachers(id)
        )
    """)

    # Create Attendance table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    """)

    # Create Fees table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            amount REAL NOT NULL,
            payment_date TEXT,
            status TEXT NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    """)

    # Insert default admin if not exists
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin', 'admin')")

    conn.commit()
    conn.close()

def execute_query(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    lastrowid = cursor.lastrowid
    conn.close()
    return lastrowid

def fetch_all(query, params=()):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def fetch_one(query, params=()):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None
