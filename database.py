import sqlite3


class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER NOT NULL
            )
        ''')
        self.connection.commit()

    def add_book(self, title, author, year):
        cursor = self.connection.cursor()
        cursor.execute('INSERT INTO books (title, author, year) VALUES (?, ?, ?)', (title, author, year))
        self.connection.commit()

    def get_all_books(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM books')
        return cursor.fetchall()

    def search_books(self, query):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR year = ?',
                       ('%' + query + '%', '%' + query + '%', query))
        return cursor.fetchall()

    def close(self):
        self.connection.close()
