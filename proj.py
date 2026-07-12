import sqlite3 #database application use sql language
import csv

print("Database is being created from CSV...\n")

conn = sqlite3.connect('data/ecommerce.db') 
cursor = conn.cursor()#cursor is use for running commands

# Create Tables
print("1️Tables are being created...")

cursor.execute('''
DROP TABLE IF EXISTS customers
''')

cursor.execute('''
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    email TEXT,
    city TEXT
)
''')

cursor.execute('''
DROP TABLE IF EXISTS orders
''')

cursor.execute('''
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    order_amount REAL
)
''')

print("Tables have been created!\n")

# Load Customers CSV
print("Customers are being loaded...")

with open('data/customers.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cursor.execute('''
        INSERT INTO customers VALUES (?, ?, ?, ?)
        ''', (row['customer_id'], row['customer_name'], 
              row['email'], row['city']))

print("Customers loaded!\n")

# Load Orders CSV
print("Orders are being loaded...")

with open('data/orders.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cursor.execute('''
        INSERT INTO orders VALUES (?, ?, ?, ?)
        ''', (row['order_id'], row['customer_id'], 
              row['order_date'], row['order_amount']))

conn.commit()
print("Orders loaded!\n")

# Verify Data
print("Verifying...")

cursor.execute("SELECT COUNT(*) FROM customers")
customers_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM orders")
orders_count = cursor.fetchone()[0]

print(f"\n DATABASE READY!")
print(f"Customers: {customers_count}")
print(f"Orders: {orders_count}")
print(f"Database: data/ecommerce.db")

conn.close()