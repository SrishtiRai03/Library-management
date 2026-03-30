"""
database.py — SQLite database layer for Library Management System
"""

import sqlite3
import os
from datetime import datetime, timedelta


DB_PATH = os.path.join(os.path.dirname(__file__), 'library.db')


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def setup(self):
        """Create tables if they don't exist."""
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS books (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                title     TEXT NOT NULL,
                author    TEXT NOT NULL,
                genre     TEXT DEFAULT 'General',
                year      INTEGER,
                copies    INTEGER DEFAULT 1,
                available INTEGER DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS members (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT NOT NULL,
                email      TEXT,
                phone      TEXT,
                joined     TEXT DEFAULT (date('now'))
            );

            CREATE TABLE IF NOT EXISTS issued_books (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id   INTEGER NOT NULL,
                book_id     INTEGER NOT NULL,
                issue_date  TEXT DEFAULT (date('now')),
                due_date    TEXT NOT NULL,
                return_date TEXT,
                fine        REAL DEFAULT 0,
                FOREIGN KEY (member_id) REFERENCES members(id),
                FOREIGN KEY (book_id)   REFERENCES books(id)
            );
        """)
        self.conn.commit()

    def seed_sample_data(self):
        """Insert sample data only on first run."""
        self.cursor.execute("SELECT COUNT(*) FROM books")
        if self.cursor.fetchone()[0] > 0:
            return  # Already seeded

        books = [
            ("The Great Gatsby",         "F. Scott Fitzgerald", "Fiction",       1925, 3),
            ("To Kill a Mockingbird",    "Harper Lee",          "Fiction",       1960, 2),
            ("1984",                     "George Orwell",       "Dystopia",      1949, 4),
            ("Brave New World",          "Aldous Huxley",       "Dystopia",      1932, 2),
            ("The Alchemist",            "Paulo Coelho",        "Philosophy",    1988, 5),
            ("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "Fantasy", 1997, 6),
            ("The Da Vinci Code",        "Dan Brown",           "Thriller",      2003, 3),
            ("Sapiens",                  "Yuval Noah Harari",   "History",       2011, 4),
            ("Atomic Habits",            "James Clear",         "Self-Help",     2018, 5),
            ("The Lean Startup",         "Eric Ries",           "Business",      2011, 3),
            ("Deep Work",                "Cal Newport",         "Self-Help",     2016, 2),
            ("Rich Dad Poor Dad",        "Robert Kiyosaki",     "Finance",       1997, 4),
            ("Introduction to Algorithms","Thomas Cormen",      "Computer Sci.", 2009, 3),
            ("Clean Code",               "Robert C. Martin",    "Computer Sci.", 2008, 2),
            ("The Pragmatic Programmer", "Andrew Hunt",         "Computer Sci.", 1999, 2),
            ("Dune",                     "Frank Herbert",       "Science Fiction",1965,3),
            ("The Hobbit",               "J.R.R. Tolkien",     "Fantasy",       1937, 4),
            ("Pride and Prejudice",      "Jane Austen",         "Romance",       1813, 3),
            ("The Psychology of Money",  "Morgan Housel",       "Finance",       2020, 4),
            ("Thinking, Fast and Slow",  "Daniel Kahneman",     "Psychology",    2011, 2),
        ]

        members = [
            ("Aarav Sharma",    "aarav@email.com",   "9876543210"),
            ("Priya Patel",     "priya@email.com",   "9123456789"),
            ("Rohan Verma",     "rohan@email.com",   "9988776655"),
            ("Sneha Gupta",     "sneha@email.com",   "9871234567"),
            ("Amit Kumar",      "amit@email.com",    "9765432109"),
        ]

        self.cursor.executemany(
            "INSERT INTO books (title, author, genre, year, copies, available) VALUES (?,?,?,?,?,?)",
            [(b[0], b[1], b[2], b[3], b[4], b[4]) for b in books]
        )
        self.cursor.executemany(
            "INSERT INTO members (name, email, phone) VALUES (?,?,?)",
            members
        )

        # Sample issue history for AI recommendations
        today = datetime.now()
        sample_issues = [
            (1, 1, (today - timedelta(days=30)).strftime('%Y-%m-%d'), (today - timedelta(days=16)).strftime('%Y-%m-%d'), (today - timedelta(days=18)).strftime('%Y-%m-%d')),
            (1, 9, (today - timedelta(days=20)).strftime('%Y-%m-%d'), (today - timedelta(days=6)).strftime('%Y-%m-%d'),  (today - timedelta(days=8)).strftime('%Y-%m-%d')),
            (1, 11,(today - timedelta(days=10)).strftime('%Y-%m-%d'), (today + timedelta(days=4)).strftime('%Y-%m-%d'),  None),
            (2, 6, (today - timedelta(days=25)).strftime('%Y-%m-%d'), (today - timedelta(days=11)).strftime('%Y-%m-%d'), (today - timedelta(days=12)).strftime('%Y-%m-%d')),
            (2, 17,(today - timedelta(days=12)).strftime('%Y-%m-%d'), (today + timedelta(days=2)).strftime('%Y-%m-%d'),  None),
            (3, 13,(today - timedelta(days=8)).strftime('%Y-%m-%d'),  (today + timedelta(days=6)).strftime('%Y-%m-%d'),  None),
            (3, 14,(today - timedelta(days=40)).strftime('%Y-%m-%d'), (today - timedelta(days=26)).strftime('%Y-%m-%d'), (today - timedelta(days=27)).strftime('%Y-%m-%d')),
            (4, 8, (today - timedelta(days=20)).strftime('%Y-%m-%d'), (today - timedelta(days=6)).strftime('%Y-%m-%d'),  None),  # overdue
            (5, 12,(today - timedelta(days=18)).strftime('%Y-%m-%d'), (today - timedelta(days=4)).strftime('%Y-%m-%d'),  None),  # overdue
        ]

        for issue in sample_issues:
            member_id, book_id, issue_date, due_date, return_date = issue
            self.cursor.execute(
                "INSERT INTO issued_books (member_id, book_id, issue_date, due_date, return_date) VALUES (?,?,?,?,?)",
                (member_id, book_id, issue_date, due_date, return_date)
            )
            if return_date is None:
                self.cursor.execute("UPDATE books SET available = available - 1 WHERE id = ?", (book_id,))

        self.conn.commit()

    # ── BOOKS ──────────────────────────────────────────────────────

    def add_book(self, title, author, genre, year, copies):
        self.cursor.execute(
            "INSERT INTO books (title, author, genre, year, copies, available) VALUES (?,?,?,?,?,?)",
            (title, author, genre, year, copies, copies)
        )
        self.conn.commit()

    def get_all_books(self):
        self.cursor.execute("SELECT id, title, author, genre, year, copies, available FROM books ORDER BY title")
        return self.cursor.fetchall()

    def get_book_by_id(self, book_id):
        self.cursor.execute("SELECT * FROM books WHERE id=?", (book_id,))
        return self.cursor.fetchone()

    def search_books_exact(self, query):
        q = f"%{query}%"
        self.cursor.execute(
            "SELECT id, title, author, genre, year, copies, available FROM books WHERE title LIKE ? OR author LIKE ? OR genre LIKE ?",
            (q, q, q)
        )
        return self.cursor.fetchall()

    def delete_book(self, book_id):
        self.cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
        self.conn.commit()

    # ── MEMBERS ────────────────────────────────────────────────────

    def add_member(self, name, email, phone):
        self.cursor.execute(
            "INSERT INTO members (name, email, phone) VALUES (?,?,?)",
            (name, email, phone)
        )
        self.conn.commit()

    def get_all_members(self):
        self.cursor.execute("SELECT id, name, email, phone, joined FROM members ORDER BY name")
        return self.cursor.fetchall()

    def get_member_by_id(self, member_id):
        self.cursor.execute("SELECT * FROM members WHERE id=?", (member_id,))
        return self.cursor.fetchone()

    # ── TRANSACTIONS ───────────────────────────────────────────────

    def issue_book(self, member_id, book_id, due_date):
        self.cursor.execute(
            "INSERT INTO issued_books (member_id, book_id, issue_date, due_date) VALUES (?,?,date('now'),?)",
            (member_id, book_id, due_date)
        )
        self.cursor.execute("UPDATE books SET available = available - 1 WHERE id=?", (book_id,))
        self.conn.commit()

    def return_book(self, issue_id):
        self.cursor.execute(
            "SELECT * FROM issued_books WHERE id=? AND return_date IS NULL", (issue_id,)
        )
        rec = self.cursor.fetchone()
        if not rec:
            return None

        due_date    = datetime.strptime(rec['due_date'], '%Y-%m-%d')
        today       = datetime.now()
        overdue_days = (today - due_date).days
        fine        = max(0, overdue_days) * 2.0  # ₹2 per day

        self.cursor.execute(
            "UPDATE issued_books SET return_date=date('now'), fine=? WHERE id=?",
            (fine, issue_id)
        )
        self.cursor.execute("UPDATE books SET available = available + 1 WHERE id=?", (rec['book_id'],))
        self.conn.commit()
        return fine

    def get_issued_books(self):
        self.cursor.execute("""
            SELECT ib.id, m.name, b.title, ib.issue_date, ib.due_date
            FROM issued_books ib
            JOIN members m ON m.id = ib.member_id
            JOIN books b   ON b.id = ib.book_id
            WHERE ib.return_date IS NULL
            ORDER BY ib.due_date
        """)
        return self.cursor.fetchall()

    def get_member_borrow_history(self, member_id):
        self.cursor.execute("""
            SELECT b.id, b.title, b.author, b.genre
            FROM issued_books ib
            JOIN books b ON b.id = ib.book_id
            WHERE ib.member_id = ?
            ORDER BY ib.issue_date DESC
        """, (member_id,))
        return self.cursor.fetchall()

    def get_all_overdue(self):
        today = datetime.now().strftime('%Y-%m-%d')
        self.cursor.execute("""
            SELECT ib.id, m.name, b.title, ib.due_date,
                   julianday('now') - julianday(ib.due_date) AS days_overdue
            FROM issued_books ib
            JOIN members m ON m.id = ib.member_id
            JOIN books b   ON b.id = ib.book_id
            WHERE ib.return_date IS NULL AND ib.due_date < ?
            ORDER BY days_overdue DESC
        """, (today,))
        return self.cursor.fetchall()

    def get_genre_stats(self):
        self.cursor.execute("""
            SELECT b.genre, COUNT(*) as borrow_count
            FROM issued_books ib
            JOIN books b ON b.id = ib.book_id
            GROUP BY b.genre
            ORDER BY borrow_count DESC
        """)
        return self.cursor.fetchall()

    def get_most_borrowed_books(self):
        self.cursor.execute("""
            SELECT b.title, b.author, COUNT(*) as borrow_count
            FROM issued_books ib
            JOIN books b ON b.id = ib.book_id
            GROUP BY b.id
            ORDER BY borrow_count DESC
            LIMIT 5
        """)
        return self.cursor.fetchall()

    def get_total_stats(self):
        self.cursor.execute("SELECT COUNT(*) FROM books")
        total_books = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT SUM(available) FROM books")
        available   = self.cursor.fetchone()[0] or 0
        self.cursor.execute("SELECT COUNT(*) FROM members")
        total_members = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(*) FROM issued_books WHERE return_date IS NULL")
        currently_issued = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(*) FROM issued_books WHERE return_date IS NOT NULL")
        total_returned = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COALESCE(SUM(fine), 0) FROM issued_books WHERE return_date IS NOT NULL")
        total_fines = self.cursor.fetchone()[0]
        return {
            'total_books':       total_books,
            'available_books':   available,
            'total_members':     total_members,
            'currently_issued':  currently_issued,
            'total_returned':    total_returned,
            'total_fines':       total_fines,
        }
