import mysql.connector

def mydb():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=""
    )

    # Create database and tables:
    cr = db.cursor()
    cr.execute("CREATE DATABASE IF NOT EXISTS BIM_Products")
    cr.execute("USE BIM_Products")

    # Create table:
    cr.execute("""CREATE TABLE IF NOT EXISTS products(
        reference_prd INT AUTO_INCREMENT PRIMARY KEY,
        name_prd VARCHAR(100) NOT NULL,
        price_prd DECIMAL(10, 2) NOT NULL,
        stock INT NOT NULL)"""
    )

    # Insert products:
    products = [
        ("Milk", 2.50, 50),
        ("Bread", 1.25, 50),
        ("Eggs", 3.00, 50),
        ("Rice", 5.75, 50),
        ("Chicken", 8.99, 50)
    ]

    insert_query = "INSERT INTO products (name_prd, price_prd, stock) VALUES (%s, %s, %s)"
    cr.executemany(insert_query, products)
    db.commit()  

    # Display:
    cr.execute("SELECT * FROM products")
    data = cr.fetchall()

    # Close cursor and connection
    cr.close()
    db.close()

    return data  

