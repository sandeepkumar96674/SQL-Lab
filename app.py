import sqlite3
import pandas as pd
import streamlit as st
import os

# Initialize database with multiple tables and sample data
def init_db():
    db_file = "database.db"
    if os.path.exists(db_file):
        os.remove(db_file)  # Remove old database to restore fresh data
    conn = sqlite3.connect(db_file)  # Persistent database file
    cursor = conn.cursor()
    
    # Create tables with primary and foreign keys
    cursor.execute("""
    CREATE TABLE Customers (
        CustomerID INTEGER PRIMARY KEY,
        CustomerName TEXT NOT NULL,
        ContactName TEXT,
        Country TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE Orders (
        OrderID INTEGER PRIMARY KEY,
        CustomerID INTEGER,
        OrderDate TEXT,
        Amount REAL,
        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
    )
    """)
    cursor.execute("""
    CREATE TABLE Products (
        ProductID INTEGER PRIMARY KEY,
        ProductName TEXT NOT NULL,
        SupplierID INTEGER,
        CategoryID INTEGER,
        UnitPrice REAL,
        FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID),
        FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
    )
    """)
    cursor.execute("""
    CREATE TABLE Categories (
        CategoryID INTEGER PRIMARY KEY,
        CategoryName TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE Suppliers (
        SupplierID INTEGER PRIMARY KEY,
        SupplierName TEXT NOT NULL,
        ContactName TEXT,
        Country TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE OrderDetails (
        OrderDetailID INTEGER PRIMARY KEY,
        OrderID INTEGER,
        ProductID INTEGER,
        Quantity INTEGER,
        FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
        FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
    )
    """)

    # Populate tables with augmented data
    customers = [
        (1, "Alfreds Futterkiste", "Maria Anders", "Germany"),
        (2, "Ana Trujillo Emparedados", "Ana Trujillo", "Mexico"),
        (3, "Antonio Moreno Taqueria", "Antonio Moreno", "Mexico"),
        (4, "Around the Horn", "Thomas Hardy", "UK"),
        (5, "Berglunds snabbkop", "Christina Berglund", "Sweden")
    ] + [(i, f"Customer_{i}", f"Contact_{i}", f"Country_{i % 5}") for i in range(6, 56)]

    orders = [
        (1, 1, "2024-01-01", 1200.50),
        (2, 2, "2024-01-02", 800.00),
        (3, 3, "2024-01-03", 1500.00),
        (4, 4, "2024-01-04", 2000.00),
        (5, 5, "2024-01-05", 500.00)
    ] + [(i, i % 50 + 1, f"2024-02-{i % 28 + 1}", i * 100.0) for i in range(6, 56)]

    categories = [
        (1, "Beverages"),
        (2, "Condiments"),
        (3, "Confections"),
        (4, "Dairy Products"),
        (5, "Grains/Cereals")
    ] + [(i, f"Category_{i}") for i in range(6, 16)]

    suppliers = [
        (1, "Exotic Liquids", "Charlotte Cooper", "UK"),
        (2, "New Orleans Cajun Delights", "Shelley Burke", "USA"),
        (3, "Grandma Kelly's Homestead", "Regina Murphy", "USA"),
        (4, "Tokyo Traders", "Yoshi Nagase", "Japan"),
        (5, "Cooperativa de Quesos 'Las Cabras'", "Antonio del Valle Saavedra", "Spain")
    ] + [(i, f"Supplier_{i}", f"Contact_{i}", f"Country_{i % 5}") for i in range(6, 16)]

    products = [
        (1, "Chai", 1, 1, 18.00),
        (2, "Chang", 1, 1, 19.00),
        (3, "Aniseed Syrup", 1, 2, 10.00),
        (4, "Chef Anton's Cajun Seasoning", 2, 2, 22.00),
        (5, "Chef Anton's Gumbo Mix", 2, 2, 21.35)
    ] + [(i, f"Product_{i}", i % 10 + 1, i % 10 + 1, (i % 20) * 5.0) for i in range(6, 56)]

    order_details = [
        (1, 1, 1, 10),
        (2, 1, 2, 5),
        (3, 2, 3, 7),
        (4, 3, 4, 3),
        (5, 4, 5, 15)
    ] + [(i, i % 50 + 1, i % 50 + 1, (i % 10) + 1) for i in range(6, 56)]

    cursor.executemany("INSERT INTO Customers VALUES (?, ?, ?, ?)", customers)
    cursor.executemany("INSERT INTO Orders VALUES (?, ?, ?, ?)", orders)
    cursor.executemany("INSERT INTO Categories VALUES (?, ?)", categories)
    cursor.executemany("INSERT INTO Suppliers VALUES (?, ?, ?, ?)", suppliers)
    cursor.executemany("INSERT INTO Products VALUES (?, ?, ?, ?, ?)", products)
    cursor.executemany("INSERT INTO OrderDetails VALUES (?, ?, ?, ?)", order_details)

    conn.commit()
    return conn

# Streamlit App

st.set_page_config(
    page_title="SQL Lab",
    page_icon="📊"
)
st.title(":red[SQL Lab]")
st.subheader("You one stop solution to Learn SQL")

# Initialize or restore database
if "db_conn" not in st.session_state:
    st.session_state.db_conn = init_db()

if st.button("Restore Database"):
    st.session_state.db_conn = init_db()
    st.success("Database restored!")

# Query input
query = st.text_area("Enter your SQL query:")

if st.button("Run Query"):
    try:
        conn = st.session_state.db_conn
        result = pd.read_sql_query(query, conn)
        st.dataframe(result)
    except Exception as e:
        st.error(f"Error: {e}")

# Additional Features
st.subheader("Database Tables")
if st.button("Show Tables"):
    try:
        conn = st.session_state.db_conn
        tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = pd.read_sql_query(tables_query, conn)
        st.write(tables)
    except Exception as e:
        st.error(f"Error: {e}")

st.caption("Created by :red[Sandeep] ✨")

