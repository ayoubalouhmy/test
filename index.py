import mysql.connector
from datetime import datetime

# Connect to MySQL server
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=""
)

cursor = db.cursor()

# Create database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS supermarket_db")
cursor.execute("USE supermarket_db")

# Create products table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL
)
""")

# Create sales table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATETIME NOT NULL,
    total DECIMAL(10, 2) NOT NULL
)
""")

# Create sale_items table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sale_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sale_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (sale_id) REFERENCES sales(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
)
""")

db.commit()
print("Database and tables created successfully!")

# Add sample products if the table is empty
cursor.execute("SELECT COUNT(*) FROM products")
count = cursor.fetchone()[0]

if count == 0:
    products = [
        ("Milk", 2.99, 50),
        ("Bread", 1.99, 30),
        ("Eggs", 3.49, 40),
        ("Apples", 2.49, 100),
        ("Chicken", 5.99, 25),
        ("Rice", 8.99, 20),
        ("Toothpaste", 3.99, 45),
        ("Soap", 2.29, 60),
        ("Soft Drink", 1.99, 70),
        ("Chips", 3.49, 80)
    ]
    
    cursor.executemany("INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)", products)
    db.commit()
    print(f"Added {len(products)} sample products")

# Simple function to display all products
def show_products():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    
    print("\n--- PRODUCT LIST ---")
    print("ID | Name | Price | Stock")
    print("-" * 40)
    
    for product in products:
        print(f"{product[0]} | {product[1]} | ${product[2]:.2f} | {product[3]}")

# Function to calculate total for products
def calculate_total():
    cart = []
    total = 0
    
    while True:
        product_id = input("\nEnter product ID (or 0 to finish): ")
        
        if product_id == "0":
            break
            
        try:
            product_id = int(product_id)
            cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            product = cursor.fetchone()
            
            if product:
                quantity = input(f"Enter quantity for {product[1]} (${product[2]:.2f}): ")
                try:
                    quantity = int(quantity)
                    if quantity <= 0:
                        print("Quantity must be positive")
                        continue
                        
                    if quantity > product[3]:
                        print(f"Not enough stock. Only {product[3]} available.")
                        continue
                        
                    item_total = quantity * product[2]
                    total += item_total
                    
                    cart.append({
                        "id": product[0],
                        "name": product[1],
                        "price": product[2],
                        "quantity": quantity,
                        "subtotal": item_total
                    })
                    
                    print(f"Added {quantity} x {product[1]} = ${item_total:.2f}")
                    
                except ValueError:
                    print("Invalid quantity. Please enter a number.")
            else:
                print("Product not found.")
                
        except ValueError:
            print("Invalid product ID. Please enter a number.")
    
    # Display cart contents
    if cart:
        print("\n--- YOUR CART ---")
        print("Product | Quantity | Price | Subtotal")
        print("-" * 50)
        
        for item in cart:
            print(f"{item['name']} | {item['quantity']} | ${item['price']:.2f} | ${item['subtotal']:.2f}")
            
        print("-" * 50)
        print(f"TOTAL: ${total:.2f}")
        
        # Save the sale to database
        save = input("\nSave this sale to database? (y/n): ")
        
        if save.lower() == "y":
            # Insert into sales table
            cursor.execute(
                "INSERT INTO sales (date, total) VALUES (%s, %s)",
                (datetime.now(), total)
            )
            sale_id = cursor.lastrowid
            
            # Insert each item into sale_items table
            for item in cart:
                cursor.execute(
                    "INSERT INTO sale_items (sale_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                    (sale_id, item['id'], item['quantity'], item['price'])
                )
                
                # Update stock
                cursor.execute(
                    "UPDATE products SET stock = stock - %s WHERE id = %s",
                    (item['quantity'], item['id'])
                )
                
            db.commit()
            print(f"Sale #{sale_id} saved successfully!")
    else:
        print("Cart is empty.")

# Main menu
def main_menu():
    while True:
        print("\n=== SUPERMARKET SYSTEM ===")
        print("1. Show All Products")
        print("2. Calculate Total")
        print("3. View Sales History")
        print("4. Add New Product")
        print("0. Exit")
        
        choice = input("\nSelect an option: ")
        
        if choice == "1":
            show_products()
        elif choice == "2":
            calculate_total()
        elif choice == "3":
            view_sales()
        elif choice == "4":
            add_product()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

# Function to view sales history
def view_sales():
    cursor.execute("""
        SELECT s.id, s.date, s.total, COUNT(si.id) as items
        FROM sales s
        JOIN sale_items si ON s.id = si.sale_id
        GROUP BY s.id
        ORDER BY s.date DESC
    """)
    
    sales = cursor.fetchall()
    
    if sales:
        print("\n--- SALES HISTORY ---")
        print("ID | Date | Items | Total")
        print("-" * 50)
        
        for sale in sales:
            sale_date = sale[1].strftime("%Y-%m-%d %H:%M")
            print(f"{sale[0]} | {sale_date} | {sale[3]} | ${sale[2]:.2f}")
            
        # Option to view details of a sale
        sale_id = input("\nEnter sale ID to view details (or 0 to return): ")
        
        if sale_id != "0":
            try:
                sale_id = int(sale_id)
                view_sale_details(sale_id)
            except ValueError:
                print("Invalid sale ID.")
    else:
        print("No sales found.")

# Function to view details of a specific sale
def view_sale_details(sale_id):
    cursor.execute("""
        SELECT si.id, p.name, si.quantity, si.price, (si.quantity * si.price) as subtotal
        FROM sale_items si
        JOIN products p ON si.product_id = p.id
        WHERE si.sale_id = %s
    """, (sale_id,))
    
    items = cursor.fetchall()
    
    if items:
        print(f"\n--- SALE #{sale_id} DETAILS ---")
        print("Product | Quantity | Price | Subtotal")
        print("-" * 50)
        
        total = 0
        for item in items:
            print(f"{item[1]} | {item[2]} | ${item[3]:.2f} | ${item[4]:.2f}")
            total += item[4]
            
        print("-" * 50)
        print(f"TOTAL: ${total:.2f}")
    else:
        print(f"No details found for sale #{sale_id}")

# Function to add a new product
def add_product():
    name = input("Enter product name: ")
    
    if not name:
        print("Product name cannot be empty.")
        return
        
    try:
        price = float(input("Enter product price: "))
        if price <= 0:
            print("Price must be positive.")
            return
            
        stock = int(input("Enter initial stock: "))
        if stock < 0:
            print("Stock cannot be negative.")
            return
            
        cursor.execute(
            "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)",
            (name, price, stock)
        )
        db.commit()
        
        print(f"Product '{name}' added successfully with ID {cursor.lastrowid}")
        
    except ValueError:
        print("Invalid input. Price must be a number and stock must be an integer.")

# Start the program
if __name__ == "__main__":
    main_menu()