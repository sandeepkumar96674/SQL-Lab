## SQL Playground : A SQL Practice platform to test your SQL Conpets

### Try it [here](https://sql-lab.streamlit.app/)

![image](https://github.com/user-attachments/assets/413724ee-f2ea-49a5-a62b-301b23cd5caa)


### In SQL Playgroud, You can use the already created Tables. In which you can perform all type of SQL operations and can Execute desired Query.

#### The reason behind the SQL Playground is to build a Platform where you can learn SQL without any Account Sign-in/Sign-up. 


Database Schema
Tables and Columns
Customers:

CustomerID (Primary Key)
CustomerName
ContactName
Country
Categories:

CategoryID (Primary Key)
CategoryName
Suppliers:

SupplierID (Primary Key)
SupplierName
ContactName
Country
Products:

ProductID (Primary Key)
ProductName
SupplierID (Foreign Key)
CategoryID (Foreign Key)
UnitPrice
Orders:

OrderID (Primary Key)
CustomerID (Foreign Key)
OrderDate
Amount
OrderDetails:

OrderDetailID (Primary Key)
OrderID (Foreign Key)
ProductID (Foreign Key)
Quantity
Sample Data Highlights
Customers:

Covers global customer base (e.g., USA, Spain, Japan, Brazil, etc.).
Categories:

Reflects diverse product categories (e.g., Fresh Produce, Dairy, Snacks, etc.).
Suppliers:

Represents a wide range of international suppliers.
Products:

Includes commonly sold goods with detailed pricing.
Orders:

Mimics real-world ordering patterns with diverse dates and amounts.
