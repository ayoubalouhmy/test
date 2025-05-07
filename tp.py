import mysql.connector
import datetime
import os
from tabulate import tabulate  

class SupermarketSystem:
    def __init__(self, host, user, password, database):
        """Initialize connection to the MySQL database"""
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor(dictionary=True)
        self.setup_database()
        self.cart = []
        
    def setup_database(self):
        """Create necessary tables if they don't exist"""
        # Products table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                stock INT NOT NULL,
                barcode VARCHAR(50) UNIQUE,
                category VARCHAR(50)
            )
        ''')
        
        # Sales table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date DATETIME NOT NULL,
                total DECIMAL(10, 2) NOT NULL,
                payment_method VARCHAR(50)
            )
        ''')
        
        # Sale items table (details of each sale)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sale_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sale_id INT NOT NULL,
                product_id INT NOT NULL,
                quantity INT NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (sale_id) REFERENCES sales(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        ''')
        
        self.connection.commit()
        
        # Add some sample products if the products table is empty
        self.cursor.execute("SELECT COUNT(*) as count FROM products")
        result = self.cursor.fetchone()
        
        if result['count'] == 0:
            sample_products = [
                ("Milk", 2.99, 50, "8901072000113", "Dairy"),
                ("Bread", 1.99, 30, "8901072000114", "Bakery"),
                ("Eggs (dozen)", 3.49, 40, "8901072000115", "Dairy"),
                ("Apples (kg)", 2.49, 100, "8901072000116", "Produce"),
                ("Chicken (kg)", 5.99, 25, "8901072000117", "Meat"),
                ("Rice (5kg)", 8.99, 20, "8901072000118", "Grains"),
                ("Toothpaste", 3.99, 45, "8901072000119", "Personal Care"),
                ("Soap", 2.29, 60, "8901072000120", "Personal Care"),
                ("Soft Drink (2L)", 1.99, 70, "8901072000121", "Beverages"),
                ("Chips", 3.49, 80, "8901072000122", "Snacks")
            ]
            
            self.cursor.executemany(
                "INSERT INTO products (name, price, stock, barcode, category) VALUES (%s, %s, %s, %s, %s)",
                sample_products
            )
            self.connection.commit()
    
    def get_all_products(self):
        """Retrieve all products from the database"""
        self.cursor.execute("SELECT * FROM products ORDER BY category, name")
        return self.cursor.fetchall()
    
    def get_product_by_barcode(self, barcode):
        """Find a product by its barcode"""
        self.cursor.execute("SELECT * FROM products WHERE barcode = %s", (barcode,))
        return self.cursor.fetchone()
    
    def search_products(self, search_term):
        """Search products by name or category"""
        search_pattern = f"%{search_term}%"
        self.cursor.execute(
            "SELECT * FROM products WHERE name LIKE %s OR category LIKE %s",
            (search_pattern, search_pattern)
        )
        return self.cursor.fetchall()
    
    def add_to_cart(self, product_id, quantity=1):
        """Add a product to the shopping cart"""
        # Get product details
        self.cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = self.cursor.fetchone()
        
        if not product:
            return False, "Product not found"
        
        if product['stock'] < quantity:
            return False, f"Insufficient stock. Only {product['stock']} available."
        
        # Check if product already in cart, if so update quantity
        for item in self.cart:
            if item['product_id'] == product_id:
                item['quantity'] += quantity
                item['subtotal'] = item['quantity'] * item['price']
                return True, f"Added {quantity} more {product['name']} to cart"
        
        # Add new item to cart
        self.cart.append({
            'product_id': product_id,
            'name': product['name'],
            'price': product['price'],
            'quantity': quantity,
            'subtotal': product['price'] * quantity
        })
        
        return True, f"Added {quantity} {product['name']} to cart"
    
    def remove_from_cart(self, index):
        """Remove an item from the cart by its index"""
        if 0 <= index < len(self.cart):
            removed_item = self.cart.pop(index)
            return True, f"Removed {removed_item['name']} from cart"
        return False, "Invalid cart item index"
    
    def view_cart(self):
        """Display the current cart contents"""
        if not self.cart:
            return "Cart is empty"
        
        # Calculate total
        total = sum(item['subtotal'] for item in self.cart)
        
        # Format cart for display
        cart_items = [[i+1, item['name'], item['quantity'], f"${item['price']:.2f}", f"${item['subtotal']:.2f}"] 
                      for i, item in enumerate(self.cart)]
        
        table = tabulate(
            cart_items,
            headers=["#", "Product", "Quantity", "Price", "Subtotal"],
            tablefmt="grid"
        )
        
        return f"{table}\n\nTotal: ${total:.2f}"
        
    def checkout(self, payment_method="Cash"):
        """Complete the purchase and record the sale"""
        if not self.cart:
            return False, "Cart is empty"
        
        total = sum(item['subtotal'] for item in self.cart)
        
        # Record the sale
        now = datetime.datetime.now()
        self.cursor.execute(
            "INSERT INTO sales (date, total, payment_method) VALUES (%s, %s, %s)",
            (now, total, payment_method)
        )
        sale_id = self.cursor.lastrowid
        
        # Record each sale item and update inventory
        for item in self.cart:
            # Record sale item
            self.cursor.execute(
                "INSERT INTO sale_items (sale_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                (sale_id, item['product_id'], item['quantity'], item['price'])
            )
            
            # Update inventory
            self.cursor.execute(
                "UPDATE products SET stock = stock - %s WHERE id = %s",
                (item['quantity'], item['product_id'])
            )
        
        self.connection.commit()
        
        # Generate receipt
        receipt = self.generate_receipt(sale_id, now, payment_method)
        
        # Clear the cart
        self.cart = []
        
        return True, receipt
    
    def generate_receipt(self, sale_id, date, payment_method):
        """Generate a formatted receipt for a sale"""
        receipt = [
            "===================================",
            "          SUPERMARKET POS          ",
            "===================================",
            f"Date: {date.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Receipt #: {sale_id}",
            "-----------------------------------"
        ]
        
        # Get sale items
        self.cursor.execute("""
            SELECT p.name, si.quantity, si.price, (si.quantity * si.price) as subtotal
            FROM sale_items si
            JOIN products p ON si.product_id = p.id
            WHERE si.sale_id = %s
        """, (sale_id,))
        
        items = self.cursor.fetchall()
        
        # Add items to receipt
        for item in items:
            receipt.append(f"{item['name']} x{item['quantity']}")
            receipt.append(f"  ${item['price']:.2f} each = ${item['subtotal']:.2f}")
        
        # Calculate total
        total = sum(item['subtotal'] for item in items)
        
        receipt.extend([
            "-----------------------------------",
            f"Total: ${total:.2f}",
            f"Payment Method: {payment_method}",
            "===================================",
            "          Thank You!              ",
            "===================================",
        ])
        
        return "\n".join(receipt)
    
    def update_product(self, product_id, name=None, price=None, stock=None, category=None):
        """Update product information"""
        updates = []
        params = []
        
        if name:
            updates.append("name = %s")
            params.append(name)
        if price is not None:
            updates.append("price = %s")
            params.append(price)
        if stock is not None:
            updates.append("stock = %s")
            params.append(stock)
        if category:
            updates.append("category = %s")
            params.append(category)
        
        if not updates:
            return False, "No updates provided"
        
        params.append(product_id)
        query = f"UPDATE products SET {', '.join(updates)} WHERE id = %s"
        
        self.cursor.execute(query, params)
        self.connection.commit()
        
        if self.cursor.rowcount > 0:
            return True, "Product updated successfully"
        else:
            return False, "Product not found or no changes made"
    
    def add_product(self, name, price, stock, barcode, category):
        """Add a new product to the database"""
        try:
            self.cursor.execute(
                "INSERT INTO products (name, price, stock, barcode, category) VALUES (%s, %s, %s, %s, %s)",
                (name, price, stock, barcode, category)
            )
            self.connection.commit()
            return True, f"Product '{name}' added successfully"
        except mysql.connector.Error as err:
            if err.errno == 1062:  # Duplicate entry error
                return False, "A product with this barcode already exists"
            return False, f"Error adding product: {err}"
    
    def delete_product(self, product_id):
        """Delete a product from the database"""
        try:
            self.cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                return True, "Product deleted successfully"
            else:
                return False, "Product not found"
        except mysql.connector.Error as err:
            return False, f"Error deleting product: {err}"
    
    def get_sales_report(self, start_date=None, end_date=None):
        """Generate a sales report for a given date range"""
        query = """
            SELECT s.id, s.date, s.total, s.payment_method,
                   COUNT(si.id) as item_count
            FROM sales s
            JOIN sale_items si ON s.id = si.sale_id
        """
        
        params = []
        where_clauses = []
        
        if start_date:
            where_clauses.append("s.date >= %s")
            params.append(start_date)
        
        if end_date:
            where_clauses.append("s.date <= %s")
            params.append(end_date)
        
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        
        query += " GROUP BY s.id ORDER BY s.date DESC"
        
        self.cursor.execute(query, params)
        sales = self.cursor.fetchall()
        
        if not sales:
            return "No sales found for the specified period"
        
        # Calculate totals
        total_sales = len(sales)
        total_revenue = sum(sale['total'] for sale in sales)
        
        # Format sales for display
        sales_data = [[
            sale['id'],
            sale['date'].strftime('%Y-%m-%d %H:%M'),
            sale['item_count'],
            f"${sale['total']:.2f}",
            sale['payment_method']
        ] for sale in sales]
        
        table = tabulate(
            sales_data,
            headers=["Sale ID", "Date", "Items", "Total", "Payment"],
            tablefmt="grid"
        )
        
        summary = f"\nSummary:\n"
        summary += f"Total Sales: {total_sales}\n"
        summary += f"Total Revenue: ${total_revenue:.2f}"
        
        return table + summary
    
    def close(self):
        """Close the database connection"""
        self.cursor.close()
        self.connection.close()


# CLI interface for the Supermarket System
def main():
    # Database configuration - adjust these settings
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'password',  # Change this to your MySQL password
        'database': 'supermarket'
    }
    
    # Initialize the system
    try:
        system = SupermarketSystem(**config)
        print("Connected to the database successfully!")
    except mysql.connector.Error as err:
        if err.errno == 1049:  # Database doesn't exist
            # Connect without specifying a database
            connection = mysql.connector.connect(
                host=config['host'],
                user=config['user'],
                password=config['password']
            )
            cursor = connection.cursor()
            
            # Create the database
            cursor.execute(f"CREATE DATABASE {config['database']}")
            connection.commit()
            cursor.close()
            connection.close()
            
            # Try connecting again
            system = SupermarketSystem(**config)
            print(f"Database '{config['database']}' created and connected successfully!")
        else:
            print(f"Error connecting to MySQL: {err}")
            return
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n==== SUPERMARKET MANAGEMENT SYSTEM ====")
        print("1. Cashier Mode")
        print("2. Inventory Management")
        print("3. Reports")
        print("0. Exit")
        
        choice = input("\nSelect an option: ")
        
        if choice == '1':
            cashier_mode(system)
        elif choice == '2':
            inventory_management(system)
        elif choice == '3':
            reports_menu(system)
        elif choice == '0':
            system.close()
            print("Thank you for using the Supermarket System!")
            break
        else:
            input("Invalid option. Press Enter to continue...")


def cashier_mode(system):
    """Handle cashier operations"""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n==== CASHIER MODE ====")
        print("1. Scan/Add Product")
        print("2. View Cart")
        print("3. Remove Item from Cart")
        print("4. Checkout")
        print("0. Back to Main Menu")
        
        choice = input("\nSelect an option: ")
        
        if choice == '1':
            # Add product to cart
            search = input("Enter product barcode or name: ")
            
            if search.isdigit() or (search.startswith('8') and len(search) > 8):
                # Assume it's a barcode
                product = system.get_product_by_barcode(search)
                if product:
                    quantity = int(input(f"Found: {product['name']} (${product['price']:.2f}). Quantity: ") or "1")
                    success, message = system.add_to_cart(product['id'], quantity)
                    print(message)
                else:
                    print("Product not found with that barcode.")
            else:
                # Search by name
                products = system.search_products(search)
                if products:
                    print("\nSearch Results:")
                    for i, product in enumerate(products):
                        print(f"{i+1}. {product['name']} - ${product['price']:.2f} ({product['stock']} in stock)")
                    
                    selection = input("\nSelect a product number (or 0 to cancel): ")
                    if selection.isdigit() and 0 < int(selection) <= len(products):
                        product = products[int(selection)-1]
                        quantity = int(input(f"Quantity for {product['name']}: ") or "1")
                        success, message = system.add_to_cart(product['id'], quantity)
                        print(message)
                else:
                    print("No products found matching that name.")
            
            input("Press Enter to continue...")
            
        elif choice == '2':
            # View cart
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n==== CURRENT CART ====")
            print(system.view_cart())
            input("\nPress Enter to continue...")
            
        elif choice == '3':
            # Remove item from cart
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n==== REMOVE FROM CART ====")
            print(system.view_cart())
            
            if system.cart:
                item_index = input("\nEnter item number to remove (or 0 to cancel): ")
                if item_index.isdigit() and 0 < int(item_index) <= len(system.cart):
                    success, message = system.remove_from_cart(int(item_index)-1)
                    print(message)
            
            input("\nPress Enter to continue...")
            
        elif choice == '4':
            # Checkout
            if not system.cart:
                print("Cart is empty. Cannot checkout.")
                input("Press Enter to continue...")
                continue
                
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n==== CHECKOUT ====")
            print(system.view_cart())
            
            payment_methods = ["Cash", "Credit Card", "Debit Card", "Mobile Payment"]
            print("\nPayment Methods:")
            for i, method in enumerate(payment_methods):
                print(f"{i+1}. {method}")
            
            payment_choice = input("\nSelect payment method (1-4): ")
            if payment_choice.isdigit() and 0 < int(payment_choice) <= len(payment_methods):
                payment_method = payment_methods[int(payment_choice)-1]
                success, receipt = system.checkout(payment_method)
                
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\n==== RECEIPT ====")
                print(receipt)
                
                print("\nSale completed successfully!")
            else:
                print("Invalid payment method. Checkout cancelled.")
                
            input("\nPress Enter to continue...")
            
        elif choice == '0':
            break
        else:
            input("Invalid option. Press Enter to continue...")


def inventory_management(system):
    """Handle inventory operations"""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n==== INVENTORY MANAGEMENT ====")
        print("1. View All Products")
        print("2. Search Products")
        print("3. Add New Product")
        print("4. Update Product")
        print("5. Delete Product")
        print("0. Back to Main Menu")
        
        choice = input("\nSelect an option: ")
        
        if choice == '1':
            # View all products
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n==== ALL PRODUCTS ====")
            products = system.get_all_products()
            
            if products:
                # Group by category
                categories = {}
                for product in products:
                    category = product['category']
                    if category not in categories:
                        categories[category] = []
                    categories[category].append(product)
                
                for category, category_products in categories.items():
                    print(f"\n--- {category} ---")
                    product_data = [[
                        p['id'],
                        p['name'],
                        f"${p['price']:.2f}",
                        p['stock'],
                        p['barcode']
                    ] for p in category_products]
                    
                    print(tabulate(
                        product_data,
                        headers=["ID", "Name", "Price", "Stock", "Barcode"],
                        tablefmt="grid"
                    ))
            else:
                print("No products found.")
                
            input("\nPress Enter to continue...")
            
        elif choice == '2':
            # Search products
            search_term = input("Enter search term: ")
            products = system.search_products(search_term)
            
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n==== SEARCH RESULTS FOR '{search_term}' ====")
            
            if products:
                product_data = [[
                    p['id'],
                    p['name'],
                    f"${p['price']:.2f}",
                    p['stock'],
                    p['barcode'],
                    p['category']
                ] for p in products]
                
                print(tabulate(
                    product_data,
                    headers=["ID", "Name", "Price", "Stock", "Barcode", "Category"],
                    tablefmt="grid"
                ))
            else:
                print("No products found matching your search.")
                
            input("\nPress Enter to continue...")
            
        elif choice == '3':
            # Add new product
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n==== ADD NEW PRODUCT ====")
            
            name = input("Product Name: ")
            
            price = input("Price: $")
            while not price or not price.replace('.', '').isdigit():
                print("Please enter a valid price.")
                price = input("Price: $")
            price = float(price)
            
            stock = input("Initial Stock: ")
            while not stock.isdigit():
                print("Please enter a valid stock quantity.")
                stock = input("Initial Stock: ")
            stock = int(stock)
            
            barcode = input("Barcode (leave empty to skip): ")
            
            category = input("Category: ")
            
            success, message = system.add_product(name, price, stock, barcode or None, category)
            print(message)
            
            input("\nPress Enter to continue...")
            
        elif choice == '4':
            # Update product
            product_id = input("Enter Product ID to update: ")
            if not product_id.isdigit():
                print("Invalid product ID.")
                input("Press Enter to continue...")
                continue
                
            # Get current product info
            system.cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            product = system.cursor.fetchone()
            
            if not product:
                print(f"Product with ID {product_id} not found.")
                input("Press Enter to continue...")
                continue
            
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n==== UPDATE PRODUCT: {product['name']} ====")
            print(f"Current Details:")
            print(f"  Name: {product['name']}")
            print(f"  Price: ${product['price']:.2f}")
            print(f"  Stock: {product['stock']}")
            print(f"  Category: {product['category']}")
            print(f"  Barcode: {product['barcode'] or 'N/A'}")
            print("\nLeave field empty to keep current value.")
            
            name = input("\nNew Name: ") or None
            
            price_input = input("New Price: $")
            price = float(price_input) if price_input else None
            
            stock_input = input("New Stock: ")
            stock = int(stock_input) if stock_input and stock_input.isdigit() else None
            
            category = input("New Category: ") or None
            
            success, message = system.update_product(product_id, name, price, stock, category)
            print(message)
            
            input("\nPress Enter to continue...")
            
        elif choice == '5':
            # Delete product
            product_id = input("Enter Product ID to delete: ")
            if not product_id.isdigit():
                print("Invalid product ID.")
                input("Press Enter to continue...")
                continue
            
            confirm = input(f"Are you sure you want to delete product ID {product_id}? (y/n): ")
            if confirm.lower() == 'y':
                success, message = system.delete_product(product_id)
                print(message)
            else:
                print("Deletion cancelled.")
                
            input("\nPress Enter to continue...")
            
        elif choice == '0':
            break
        else:
            input("Invalid option. Press Enter to continue...")


def reports_menu(system):
    """Handle reports operations"""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n==== REPORTS ====")
        print("1. Sales Report")
        print("2. Low Stock Report")
        print("3. Category Sales Report")
        print("0. Back to Main Menu")
        
        choice = input("\nSelect an option: ")
        
        if choice == '1':
            # Sales report
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n==== SALES REPORT ====")
            
            print("Date Range (leave empty for all time):")
            start_date = input("Start Date (YYYY-MM-DD): ")
            end_date = input("End Date (YYYY-MM-DD): ")
            
            # Convert to datetime objects if provided
            start = datetime.datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
            end = datetime.datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
            if end:
                # Set end date to end of day
                end = end.replace(hour=23, minute=59, second=59)
            
            report = system.get_sales_report(start, end)
            print(report)
            
            input("\nPress Enter to continue...")
            
        elif choice == '2':
            # Low stock report
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n==== LOW STOCK REPORT ====")
            
            threshold = input("Stock threshold (default 10): ")
            threshold = int(threshold) if threshold and threshold.isdigit() else 10
            
            system.cursor.execute("SELECT * FROM products WHERE stock <= %s ORDER BY stock", (threshold,))
            low_stock = system.cursor.fetchall()
            
            if low_stock:
                product_data = [[
                    p['id'],
                    p['name'],
                    p['stock'],
                    p['category']
                ] for p in low_stock]
                
                print(tabulate(
                    product_data,
                    headers=["ID", "Name", "Stock", "Category"],
                    tablefmt="grid"
                ))
                print(f"\nTotal {len(low_stock)} products with stock <= {threshold}")
            else:
                print(f"No products with stock <= {threshold}")
                
            input("\nPress Enter to continue...")
            
        elif choice == '3':
            # Category sales report
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n==== CATEGORY SALES REPORT ====")
            
            # Get date range
            print("Date Range (leave empty for all time):")
            start_date = input("Start Date (YYYY-MM-DD): ")
            end_date = input("End Date (YYYY-MM-DD): ")
            
            # Convert to datetime objects if provided
            date_conditions = []
            params = []
            
            if start_date:
                date_conditions.append("s.date >= %s")
                params.append(datetime.datetime.strptime(start_date, "%Y-%m-%d"))
            
            if end_date:
                date_conditions.append("s.date <= %s")
                end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
                end = end.replace(hour=23, minute=59, second=59)
                params.append(end)
            
            # Build the query
            query = """
                SELECT 
                    p.category,
                    COUNT(si.id) as items_sold,
                    SUM(si.quantity) as units_sold,
                    SUM(si.quantity * si.price) as total_sales
                FROM sale_items si
                JOIN products p ON si.product_id = p.id
                JOIN sales s ON si.sale_id = s.id
            """
            
            if date_conditions:
                query += " WHERE " + " AND ".join(date_conditions)
            
            query += " GROUP BY p.category ORDER BY total_sales DESC"
            
            system.cursor.execute(query, params)
            category_sales = system.cursor.fetchall()
            
            if category_sales:
                category_data = [[
                    c['category'],
                    c['items_sold'],
                    c['units_sold'],
                    f"${c['total_sales']:.2f}"
                ] for c in category_sales]
                
                print(tabulate(
                    category_data,
                    headers=["Category", "Items Sold", "Units Sold", "Total Sales"],
                    tablefmt="grid"
                ))
                
                # Calculate totals
                total_sales = sum(c['total_sales'] for c in category_sales)
                total_units = sum(c['units_sold'] for c in category_sales)
                
                print(f"\nTotal Sales: ${total_sales:.2f}")
                print(f"Total Units Sold: {total_units}")
            else:
                print("No sales data found for the specified period")
                
            input("\nPress Enter to continue...")
            
        elif choice == '0':
            break
        else:
            input("Invalid option. Press Enter to continue...")


if __name__ == "__main__":
    main()