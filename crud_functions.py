import sqlite3


def initiate_db():
    with sqlite3.connect('products_db.db') as connection:
        cursor = connection.cursor()
        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        price INT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INT NOT NULL,
        balance INT NOT NULL
        )
        ''')


def get_all_products():
    with sqlite3.connect('products_db.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Products')
        products = cursor.fetchall()
        return products


def add_user(username, email, age, balance=1000):
    with sqlite3.connect('products_db.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
        INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)
        ''', (username, email, age, balance))


def is_included(username):
    with sqlite3.connect('products_db.db') as connection:
        cursor = connection.cursor()
        user = cursor.execute("SELECT username FROM Users WHERE username = ?", (username,)).fetchone()
        return user is not None
