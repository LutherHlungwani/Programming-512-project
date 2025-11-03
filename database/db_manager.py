import sqlite3
from datetime import datetime
from config import DB_PATH

def add_book(isbn, title, author, publisher, publication_year, category, description, cover_image_url, page_count, language, total_copies, shelf_location):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Books (isbn, title, author, publisher, publication_year, category, description, cover_image_url, page_count, language, total_copies, available_copies, shelf_location)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (isbn, title, author, publisher, publication_year, category, description, cover_image_url, page_count, language, total_copies, total_copies, shelf_location))
    conn.commit()
    conn.close()

def get_book_by_isbn(isbn):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Books WHERE isbn = ?", (isbn,))
    book = cursor.fetchone()
    conn.close()
    return book

def get_all_books():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()
    conn.close()
    return books

def update_book(book_id, isbn, title, author, publisher, publication_year, category, description, cover_image_url, page_count, language, total_copies, shelf_location):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Books SET isbn=?, title=?, author=?, publisher=?, publication_year=?, category=?, description=?, cover_image_url=?, page_count=?, language=?, total_copies=?, available_copies=?, shelf_location=?
        WHERE book_id=?
    """, (isbn, title, author, publisher, publication_year, category, description, cover_image_url, page_count, language, total_copies, total_copies, shelf_location, book_id))
    conn.commit()
    conn.close()

def delete_book(book_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Books WHERE book_id = ?", (book_id,))
    conn.commit()
    conn.close()

def add_member(membership_number, first_name, last_name, email, phone, address, membership_type):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Members (membership_number, first_name, last_name, email, phone, address, join_date, membership_type, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (membership_number, first_name, last_name, email, phone, address, datetime.now().strftime("%Y-%m-%d"), membership_type, "Active"))
    conn.commit()
    conn.close()

def get_member_by_id(member_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Members WHERE member_id = ?", (member_id,))
    member = cursor.fetchone()
    conn.close()
    return member

def get_all_members():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Members")
    members = cursor.fetchall()
    conn.close()
    return members

def issue_book(member_id, book_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Check if book is available
    cursor.execute("SELECT available_copies FROM Books WHERE book_id = ?", (book_id,))
    available = cursor.fetchone()
    if available and available[0] > 0:
        # Update available copies
        cursor.execute("UPDATE Books SET available_copies = available_copies - 1 WHERE book_id = ?", (book_id,))
        # Insert transaction
        from datetime import datetime, timedelta
        issue_date = datetime.now().strftime("%Y-%m-%d")
        due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        cursor.execute("""
            INSERT INTO Transactions (member_id, book_id, issue_date, due_date, status)
            VALUES (?, ?, ?, ?, ?)
        """, (member_id, book_id, issue_date, due_date, "Issued"))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False

def return_book(transaction_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT book_id FROM Transactions WHERE transaction_id = ?", (transaction_id,))
    book_id = cursor.fetchone()
    if book_id:
        book_id = book_id[0]
        # Update available copies
        cursor.execute("UPDATE Books SET available_copies = available_copies + 1 WHERE book_id = ?", (book_id,))
        # Update transaction
        from datetime import datetime
        return_date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("UPDATE Transactions SET return_date = ?, status = 'Returned' WHERE transaction_id = ?", (return_date, transaction_id))
        conn.commit()
    conn.close()

def get_all_transactions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.transaction_id, m.first_name || ' ' || m.last_name as member_name, b.title, t.issue_date, t.due_date, t.return_date, t.fine_amount, t.status
        FROM Transactions t
        JOIN Members m ON t.member_id = m.member_id
        JOIN Books b ON t.book_id = b.book_id
    """)
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def get_overdue_transactions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.transaction_id, m.first_name || ' ' || m.last_name as member_name, b.title, t.due_date
        FROM Transactions t
        JOIN Members m ON t.member_id = m.member_id
        JOIN Books b ON t.book_id = b.book_id
        WHERE t.status = 'Issued' AND t.due_date < date('now')
    """)
    overdue = cursor.fetchall()
    conn.close()
    return overdue

def get_member_borrowing_history(member_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.title, t.issue_date, t.due_date, t.return_date, t.fine_amount, t.status
        FROM Transactions t
        JOIN Books b ON t.book_id = b.book_id
        WHERE t.member_id = ?
        ORDER BY t.issue_date DESC
    """, (member_id,))
    history = cursor.fetchall()
    conn.close()
    return history

def get_recent_transactions(limit=5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.transaction_id, m.first_name || ' ' || m.last_name as member_name, b.title, t.issue_date, t.status
        FROM Transactions t
        JOIN Members m ON t.member_id = m.member_id
        JOIN Books b ON t.book_id = b.book_id
        ORDER BY t.issue_date DESC
        LIMIT ?
    """, (limit,))
    recent = cursor.fetchall()
    conn.close()
    return recent

def get_popular_books(limit=5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.title, COUNT(t.transaction_id) as issue_count
        FROM Books b
        JOIN Transactions t ON b.book_id = t.book_id
        GROUP BY b.book_id
        ORDER BY issue_count DESC
        LIMIT ?
    """, (limit,))
    popular = cursor.fetchall()
    conn.close()
    return popular