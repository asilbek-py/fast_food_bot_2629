import sqlite3
from config import DB_NAME

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        full_name TEXT,
        phone_number TEXT
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER,
        name TEXT,
        description TEXT,
        price INTEGER,
        image_url TEXT,
        image_file_id TEXT,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        status TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
    ''')
    conn.commit()
    conn.close()

# Category helpers
def get_all_categories():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM categories ORDER BY name')
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_category(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO categories (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()

def delete_category_by_name(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM categories WHERE name = ?', (name,))
    conn.commit()
    conn.close()

# Product helpers
def add_product(category_id, name, description, price, image_url=None, image_file_id=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (category_id, name, description, price, image_url, image_file_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (category_id, name, description, price, image_url, image_file_id))
    conn.commit()
    conn.close()

def get_products_by_category(category_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, price FROM products WHERE category_id = ?', (category_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_product_by_name_and_category(name, category_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, name, description, price, image_url, image_file_id
        FROM products
        WHERE name = ? AND category_id = ?
    ''', (name, category_id))
    row = cursor.fetchone()
    conn.close()
    return row

def get_product_by_id(product_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, description, price, image_url, image_file_id FROM products WHERE id = ?', (product_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def delete_product_by_name(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE name = ?', (name,))
    conn.commit()
    conn.close()
