import streamlit as st
import pandas as pd
import sqlite3
import os

def init_db():
    db_file = "database.db"
    if os.path.exists(db_file):
        os.remove(db_file)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Customers (
        CustomerID INTEGER PRIMARY KEY,
        CustomerName TEXT NOT NULL,
        ContactName TEXT,
        Country TEXT
    )""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Categories (
        CategoryID INTEGER PRIMARY KEY,
        CategoryName TEXT NOT NULL
    )""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Suppliers (
        SupplierID INTEGER PRIMARY KEY,
        SupplierName TEXT NOT NULL,
        ContactName TEXT,
        Country TEXT
    )""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Products (
        ProductID INTEGER PRIMARY KEY,
        ProductName TEXT NOT NULL,
        SupplierID INTEGER,
        CategoryID INTEGER,
        UnitPrice REAL,
        FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID),
        FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
    )""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Orders (
        OrderID INTEGER PRIMARY KEY,
        CustomerID INTEGER,
        OrderDate TEXT,
        Amount REAL,
        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
    )""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS OrderDetails (
        OrderDetailID INTEGER PRIMARY KEY,
        OrderID INTEGER,
        ProductID INTEGER,
        Quantity INTEGER,
        FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
        FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
    )""")

    # Customers Data (50+ records)
    customers = [
        (1, "Global Mart", "John Smith", "USA"),
        (2, "Euro Foods", "Maria Garcia", "Spain"),
        (3, "Asian Delights", "Lee Wong", "Singapore"),
        (4, "Nordic Supplies", "Erik Anderson", "Sweden"),
        (5, "Mediterranean Traders", "Sofia Costa", "Italy"),
        (6, "Australian Goods", "Sarah Johnson", "Australia"),
        (7, "Canadian Supplies", "Michael Brown", "Canada"),
        (8, "German Imports", "Hans Weber", "Germany"),
        (9, "French Delicacies", "Pierre Dubois", "France"),
        (10, "Japanese Trading", "Yuki Tanaka", "Japan"),
        (11, "Brazilian Markets", "Carlos Silva", "Brazil"),
        (12, "Indian Spices", "Priya Patel", "India"),
        (13, "Mexican Foods", "Ana Rodriguez", "Mexico"),
        (14, "Russian Imports", "Ivan Petrov", "Russia"),
        (15, "Korean Mart", "Kim Min-ji", "South Korea"),
        (16, "Dutch Traders", "Jan de Vries", "Netherlands"),
        (17, "Swiss Quality", "Marc Mueller", "Switzerland"),
        (18, "Thai Flavors", "Somchai Lee", "Thailand"),
        (19, "Irish Goods", "Sean O'Connor", "Ireland"),
        (20, "Polish Imports", "Anna Kowalski", "Poland"),
        (21, "Portuguese Wines", "Manuel Santos", "Portugal"),
        (22, "Belgian Chocolates", "Emma Dubois", "Belgium"),
        (23, "Greek Delicacies", "Nikos Papadopoulos", "Greece"),
        (24, "Turkish Bazaar", "Mehmet Yilmaz", "Turkey"),
        (25, "Vietnamese Fresh", "Nguyen Van", "Vietnam"),
        (26, "Malaysian Spices", "Ahmad Abdullah", "Malaysia"),
        (27, "Indonesian Traders", "Siti Rahma", "Indonesia"),
        (28, "Filipino Mart", "Maria Santos", "Philippines"),
        (29, "Danish Dairy", "Lars Nielsen", "Denmark"),
        (30, "Finnish Foods", "Matti Virtanen", "Finland"),
        (31, "Norwegian Fish", "Ole Hansen", "Norway"),
        (32, "Icelandic Goods", "Gunnar Eriksson", "Iceland"),
        (33, "Czech Beverages", "Pavel Novak", "Czech Republic"),
        (34, "Hungarian Paprika", "Zsolt Nagy", "Hungary"),
        (35, "Romanian Wines", "Ion Popescu", "Romania"),
        (36, "Bulgarian Dairy", "Ivan Dimitrov", "Bulgaria"),
        (37, "Croatian Seafood", "Ana Kovac", "Croatia"),
        (38, "Serbian Meats", "Nikola Jovanovic", "Serbia"),
        (39, "Slovenian Alps", "Maja Kovac", "Slovenia"),
        (40, "Moroccan Spices", "Hassan Ahmed", "Morocco"),
        (41, "Egyptian Dates", "Ahmed Hassan", "Egypt"),
        (42, "South African Wines", "David Smith", "South Africa"),
        (43, "Nigerian Foods", "Chinua Achebe", "Nigeria"),
        (44, "Kenyan Coffee", "James Kamau", "Kenya"),
        (45, "Ethiopian Spices", "Solomon Desta", "Ethiopia"),
        (46, "Argentine Beef", "Diego Martinez", "Argentina"),
        (47, "Chilean Wines", "Carmen Rodriguez", "Chile"),
        (48, "Peruvian Goods", "Luis Garcia", "Peru"),
        (49, "Colombian Coffee", "Isabella Martinez", "Colombia"),
        (50, "Venezuelan Foods", "Carlos Ramirez", "Venezuela")
    ]

    # Categories Data (8 records - keeping focused as per business needs)
    categories = [
        (1, "Fresh Produce"),
        (2, "Dairy"),
        (3, "Bakery"),
        (4, "Beverages"),
        (5, "Snacks"),
        (6, "Frozen Foods"),
        (7, "Canned Goods"),
        (8, "Personal Care")
    ]

    # Suppliers Data (50+ records)
    suppliers = [
        (1, "Fresh Fields Co.", "James Wilson", "USA"),
        (2, "European Imports", "Hans Mueller", "Germany"),
        (3, "Asian Market Ltd.", "Liu Chen", "China"),
        (4, "Nordic Fresh", "Eva Larsson", "Sweden"),
        (5, "Mediterranean Supplies", "Marco Rossi", "Italy"),
        (6, "Pacific Trading", "David Chen", "Singapore"),
        (7, "American Foods", "Robert Johnson", "USA"),
        (8, "Euro Distributors", "Sophie Martin", "France"),
        (9, "Asian Exports", "Kim Lee", "South Korea"),
        (10, "Global Foods", "Mohammed Ahmed", "UAE"),
        (11, "Organic Farms Inc.", "Peter Brown", "Canada"),
        (12, "Quality Goods Ltd.", "Sarah Wilson", "UK"),
        (13, "Fresh Direct", "Michael Davis", "USA"),
        (14, "Euro Quality", "Anna Schmidt", "Germany"),
        (15, "Asian Specialties", "Wong Li", "China"),
        (16, "Nordic Goods", "Anders Nilsson", "Sweden"),
        (17, "Mediterranean Flavors", "Giuseppe Romano", "Italy"),
        (18, "Pacific Fresh", "Lucy Chen", "Singapore"),
        (19, "American Organics", "William Johnson", "USA"),
        (20, "Euro Fresh", "Marie Dupont", "France"),
        (21, "Asian Premium", "Park Jin", "South Korea"),
        (22, "Global Traders", "Ali Hassan", "UAE"),
        (23, "Farm Fresh Co.", "John Williams", "Canada"),
        (24, "Quality Foods", "Emma Thompson", "UK"),
        (25, "Direct Fresh", "Richard Miller", "USA"),
        (26, "Euro Premium", "Klaus Weber", "Germany"),
        (27, "Asian Delicacies", "Zhang Wei", "China"),
        (28, "Nordic Premium", "Erik Svensson", "Sweden"),
        (29, "Mediterranean Select", "Antonio Ferrari", "Italy"),
        (30, "Pacific Premium", "Thomas Tan", "Singapore"),
        (31, "American Select", "Jennifer Brown", "USA"),
        (32, "Euro Select", "Pierre Martin", "France"),
        (33, "Asian Select", "Kim Min", "South Korea"),
        (34, "Global Select", "Fatima Ahmed", "UAE"),
        (35, "Farm Select", "David Wilson", "Canada"),
        (36, "Quality Select", "James Smith", "UK"),
        (37, "Direct Select", "Thomas Davis", "USA"),
        (38, "Euro Delicacies", "Hans Schmidt", "Germany"),
        (39, "Asian Premium Foods", "Li Wei", "China"),
        (40, "Nordic Select", "Lars Anderson", "Sweden"),
        (41, "Mediterranean Premium", "Paolo Romano", "Italy"),
        (42, "Pacific Select", "Andrew Tan", "Singapore"),
        (43, "American Premium", "Mary Johnson", "USA"),
        (44, "Euro Premium Foods", "Sophie Dubois", "France"),
        (45, "Asian Premium Goods", "Lee Min", "South Korea"),
        (46, "Global Premium", "Hassan Ahmed", "UAE"),
        (47, "Farm Premium", "Michael Wilson", "Canada"),
        (48, "Quality Premium", "Oliver Smith", "UK"),
        (49, "Direct Premium", "Robert Miller", "USA"),
        (50, "Premium Imports", "Karl Schmidt", "Germany")
    ]

    # Products Data (50+ records)
    products = [
        (1, "Organic Apples", 1, 1, 2.99),
        (2, "Fresh Milk", 2, 2, 3.49),
        (3, "Whole Grain Bread", 3, 3, 4.99),
        (4, "Orange Juice", 4, 4, 3.99),
        (5, "Potato Chips", 5, 5, 2.49),
        (6, "Frozen Pizza", 6, 6, 6.99),
        (7, "Canned Tomatoes", 7, 7, 1.99),
        (8, "Shampoo", 8, 8, 5.99),
        (9, "Greek Yogurt", 9, 2, 4.49),
        (10, "Organic Bananas", 10, 1, 2.99),
        (11, "Cheddar Cheese", 11, 2, 5.99),
        (12, "Sourdough Bread", 12, 3, 5.49),
        (13, "Green Tea", 13, 4, 4.99),
        (14, "Tortilla Chips", 14, 5, 3.49),
        (15, "Ice Cream", 15, 6, 5.99),
        (16, "Canned Beans", 16, 7, 1.49),
        (17, "Toothpaste", 17, 8, 3.99),
        (18, "Cottage Cheese", 18, 2, 4.29),
        (19, "Fresh Strawberries", 19, 1, 4.99),
        (20, "Mozzarella", 20, 2, 5.49),
        (21, "Multigrain Bread", 21, 3, 4.79),
        (22, "Sparkling Water", 22, 4, 2.99),
        (23, "Popcorn", 23, 5, 2.99),
        (24, "Frozen Vegetables", 24, 6, 4.49),
        (25, "Canned Soup", 25, 7, 2.99),
        (26, "Body Wash", 26, 8, 6.99),
        (27, "Sour Cream", 27, 2, 3.49),
        (28, "Fresh Oranges", 28, 1, 3.99),
        (29, "Blue Cheese", 29, 2, 6.99),
        (30, "Rye Bread", 30, 3, 5.29),
        (31, "Coffee Beans", 31, 4, 9.99),
        (32, "Trail Mix", 32, 5, 4.99),
        (33, "Frozen Pizza Rolls", 33, 6, 5.49),
        (34, "Canned Tuna", 34, 7, 2.49),
        (35, "Hand Soap", 35, 8, 3.99),
        (36, "Butter", 36, 2, 4.99),
        (37, "Fresh Grapes", 37, 1, 3.99),
        (38, "Gouda Cheese", 38, 2, 6.49),
        (39, "Bagels", 39, 3, 4.49),
        (40, "Iced Tea", 40, 4, 3.99),
        (41, "Pretzels", 41, 5, 3.49),
        (42, "Frozen Waffles", 42, 6, 4.29),
        (43, "Canned Corn", 43, 7, 1.79),
        (44, "Deodorant", 44, 8, 4.99),
        (45, "Heavy Cream", 45, 2, 4.49),
        (46, "Fresh Pears", 46, 1, 3.49),
        (47, "Swiss Cheese", 47, 2, 7.99),
        (48, "Croissants", 48, 3, 5.99),
        (49, "Lemonade", 49, 4, 2.99),
        (50, "Crackers", 50, 5, 3.29)
    ]

    # Orders Data (100+ records)
    orders = [
        (1, 1, "2024-01-01", 150.50),
        (2, 2, "2024-01-01", 275.25),
        (3, 3, "2024-01-01", 420.75),
        (4, 4, "2024-01-01", 180.00),
        (5, 5, "2024-01-01", 350.50),
        (6, 6, "2024-01-02", 225.75),
        (7, 7, "2024-01-02", 190.25),
        (8, 8, "2024-01-02", 280.00),
        (9, 9, "2024-01-02", 310.50),
        (10, 10, "2024-01-02", 425.75),
        (11, 11, "2024-01-03", 175.50),
        (12, 12, "2024-01-03", 290.25),
        (13, 13, "2024-01-03", 430.75),
        (14, 14, "2024-01-03", 195.00),
        (15, 15, "2024-01-03", 365.50),
        (16, 16, "2024-01-04", 240.75),
        (17, 17, "2024-01-04", 205.25),
        (18, 18, "2024-01-04", 295.00),
        (19, 19, "2024-01-04", 325.50),
        (20, 20, "2024-01-04", 440.75),
        (21, 21, "2024-01-05", 160.50),
        (22, 22, "2024-01-05", 280.25),
        (23, 23, "2024-01-05", 410.75),
        (24, 24, "2024-01-05", 170.00),
        (25, 25, "2024-01-05", 340.50),
        (26, 26, "2024-01-06", 215.75),
        (27, 27, "2024-01-06", 180.25),
        (28, 28, "2024-01-06", 270.00),
        (29, 29, "2024-01-06", 300.50),
        (30, 30, "2024-01-06", 415.75),
        (31, 31, "2024-01-07", 185.50),
        (32, 32, "2024-01-07", 300.25),
        (33, 33, "2024-01-07", 450.75),
        (34, 34, "2024-01-07", 210.00),
        (35, 35, "2024-01-07", 380.50),
        (36, 36, "2024-01-08", 255.75),
        (37, 37, "2024-01-08", 220.25),
        (38, 38, "2024-01-08", 310.00),
        (39, 39, "2024-01-08", 340.50),
        (40, 40, "2024-01-08", 455.75),
        (41, 41, "2024-01-09", 165.50),
        (42, 42, "2024-01-09", 285.25),
        (43, 43, "2024-01-09", 415.75),
        (44, 44, "2024-01-09", 175.00),
        (45, 45, "2024-01-09", 345.50),
        (46, 46, "2024-01-10", 220.75),
        (47, 47, "2024-01-10", 185.25),
        (48, 48, "2024-01-10", 275.00),
        (49, 49, "2024-01-10", 305.50),
        (50, 50, "2024-01-10", 420.75),
        (51, 1, "2024-01-11", 155.50),
        (52, 2, "2024-01-11", 280.25),
        (53, 3, "2024-01-11", 425.75),
        (54, 4, "2024-01-11", 185.00),
        (55, 5, "2024-01-11", 355.50),
        (56, 6, "2024-01-12", 230.75),
        (57, 7, "2024-01-12", 195.25),
        (58, 8, "2024-01-12", 285.00),
        (59, 9, "2024-01-12", 315.50),
        (60, 10, "2024-01-12", 430.75),
        (61, 11, "2024-01-13", 180.50),
        (62, 12, "2024-01-13", 295.25),
        (63, 13, "2024-01-13", 435.75),
        (64, 14, "2024-01-13", 200.00),
        (65, 15, "2024-01-13", 370.50),
        (66, 16, "2024-01-14", 245.75),
        (67, 17, "2024-01-14", 210.25),
        (68, 18, "2024-01-14", 300.00),
        (69, 19, "2024-01-14", 330.50),
        (70, 20, "2024-01-14", 445.75),
        (71, 21, "2024-01-15", 165.50),
        (72, 22, "2024-01-15", 285.25),
        (73, 23, "2024-01-15", 415.75),
        (74, 24, "2024-01-15", 175.00),
        (75, 25, "2024-01-15", 345.50),
        (76, 26, "2024-01-16", 220.75),
        (77, 27, "2024-01-16", 185.25),
        (78, 28, "2024-01-16", 275.00),
        (79, 29, "2024-01-16", 305.50),
        (80, 30, "2024-01-16", 420.75),
        (81, 31, "2024-01-17", 190.50),
        (82, 32, "2024-01-17", 305.25),
        (83, 33, "2024-01-17", 455.75),
        (84, 34, "2024-01-17", 215.00),
        (85, 35, "2024-01-17", 385.50),
        (86, 36, "2024-01-18", 260.75),
        (87, 37, "2024-01-18", 225.25),
        (88, 38, "2024-01-18", 315.00),
        (89, 39, "2024-01-18", 345.50),
        (90, 40, "2024-01-18", 460.75),
        (91, 41, "2024-01-19", 170.50),
        (92, 42, "2024-01-19", 290.25),
        (93, 43, "2024-01-19", 420.75),
        (94, 44, "2024-01-19", 180.00),
        (95, 45, "2024-01-19", 350.50),
        (96, 46, "2024-01-20", 225.75),
        (97, 47, "2024-01-20", 190.25),
        (98, 48, "2024-01-20", 280.00),
        (99, 49, "2024-01-20", 310.50),
        (100, 50, "2024-01-20", 425.75)
    ]

    # Order Details Data (50+ records)
    order_details = [
        (1, 1, 1, 5),
        (2, 1, 2, 3),
        (3, 2, 3, 2),
        (4, 2, 4, 4),
        (5, 3, 5, 6),
        (6, 3, 6, 2),
        (7, 4, 7, 3),
        (8, 4, 8, 5),
        (9, 5, 9, 4),
        (10, 5, 10, 3),
        (11, 6, 11, 2),
        (12, 6, 12, 4),
        (13, 7, 13, 3),
        (14, 7, 14, 5),
        (15, 8, 15, 2),
        (16, 8, 16, 4),
        (17, 9, 17, 6),
        (18, 9, 18, 3),
        (19, 10, 19, 4),
        (20, 10, 20, 2),
        (21, 11, 21, 5),
        (22, 11, 22, 3),
        (23, 12, 23, 4),
        (24, 12, 24, 2),
        (25, 13, 25, 6),
        (26, 13, 26, 3),
        (27, 14, 27, 4),
        (28, 14, 28, 5),
        (29, 15, 29, 2),
        (30, 15, 30, 4),
        (31, 16, 31, 3),
        (32, 16, 32, 5),
        (33, 17, 33, 2),
        (34, 17, 34, 4),
        (35, 18, 35, 6),
        (36, 18, 36, 3),
        (37, 19, 37, 4),
        (38, 19, 38, 2),
        (39, 20, 39, 5),
        (40, 20, 40, 3),
        (41, 21, 41, 4),
        (42, 21, 42, 2),
        (43, 22, 43, 6),
        (44, 22, 44, 3),
        (45, 23, 45, 4),
        (46, 23, 46, 5),
        (47, 24, 47, 2),
        (48, 24, 48, 4),
        (49, 25, 49, 3),
        (50, 25, 50, 5)
    ]

    # Insert data
    cursor.executemany("INSERT INTO Customers VALUES (?, ?, ?, ?)", customers)
    cursor.executemany("INSERT INTO Categories VALUES (?, ?)", categories)
    cursor.executemany("INSERT INTO Suppliers VALUES (?, ?, ?, ?)", suppliers)
    cursor.executemany("INSERT INTO Products VALUES (?, ?, ?, ?, ?)", products)
    cursor.executemany("INSERT INTO Orders VALUES (?, ?, ?, ?)", orders)
    cursor.executemany("INSERT INTO OrderDetails VALUES (?, ?, ?, ?)", order_details)

    conn.commit()
    return conn

# Streamlit App

st.set_page_config(
    page_title="SQL Lab"
)
st.title(":red[SQL Lab]")
st.subheader("You one stop solution to Practice SQL")

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

