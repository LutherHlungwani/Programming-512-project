import sqlite3
import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import DB_PATH

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Books Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT UNIQUE,
            title TEXT NOT NULL,
            author TEXT,
            publisher TEXT,
            publication_year INTEGER,
            category TEXT,
            description TEXT,
            cover_image_url TEXT,
            page_count INTEGER,
            language TEXT,
            total_copies INTEGER NOT NULL,
            available_copies INTEGER NOT NULL,
            shelf_location TEXT
        )
    """)

    # Members Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Members (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            membership_number TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT,
            address TEXT,
            join_date DATE,
            membership_type TEXT,
            status TEXT CHECK(status IN ('Active', 'Suspended', 'Expired'))
        )
    """)

    # Transactions Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER,
            book_id INTEGER,
            issue_date DATE,
            due_date DATE,
            return_date DATE,
            fine_amount REAL DEFAULT 0.0,
            status TEXT CHECK(status IN ('Issued', 'Returned', 'Overdue')),
            FOREIGN KEY (member_id) REFERENCES Members(member_id),
            FOREIGN KEY (book_id) REFERENCES Books(book_id)
        )
    """)

    # Book_Reviews Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Book_Reviews (
            review_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            member_id INTEGER,
            rating INTEGER CHECK(rating BETWEEN 1 AND 5),
            review_text TEXT,
            review_date DATE,
            FOREIGN KEY (book_id) REFERENCES Books(book_id),
            FOREIGN KEY (member_id) REFERENCES Members(member_id)
        )
    """)

    conn.commit()
    conn.close()

def insert_sample_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insert sample books
    cursor.execute("""
        INSERT OR IGNORE INTO Books (isbn, title, author, publisher, publication_year, category, description, cover_image_url, page_count, language, total_copies, available_copies, shelf_location)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "9780134685991",
        "Effective Java",
        "Joshua Bloch",
        "Addison-Wesley Professional",
        2017,
        "Programming",
        "A guide to best practices for Java developers.",
        "https://books.google.com/books/content/images/frontcover/9780134685991.jpg?img=1",
        416,
        "English",
        3,
        3,
        "A-1"
    ))

    cursor.execute("""
        INSERT OR IGNORE INTO Books (isbn, title, author, publisher, publication_year, category, description, cover_image_url, page_count, language, total_copies, available_copies, shelf_location)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "9781449355739",
        "Learning Python",
        "Mark Lutz",
        "O'Reilly Media",
        2013,
        "Programming",
        "A comprehensive guide to Python programming.",
        "https://books.google.com/books/content/images/frontcover/9781449355739.jpg?img=1",
        1648,
        "English",
        2,
        2,
        "B-2"
    ))

    # Insert sample members
    cursor.execute("""
        INSERT OR IGNORE INTO Members (membership_number, first_name, last_name, email, phone, address, join_date, membership_type, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "M001",
        "John",
        "Doe",
        "john.doe@example.com",
        "1234567890",
        "123 Main St, City",
        "2025-01-15",
        "Standard",
        "Active"
    ))

    cursor.execute("""
        INSERT OR IGNORE INTO Members (membership_number, first_name, last_name, email, phone, address, join_date, membership_type, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "M002",
        "Jane",
        "Smith",
        "jane.smith@example.com",
        "0987654321",
        "456 Oak Ave, City",
        "2025-02-20",
        "Premium",
        "Active"
    ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    insert_sample_data()
    print("Database and sample data created successfully!")