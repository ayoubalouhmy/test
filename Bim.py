import mysql.connector
from bimdb import mydb

def get_products(num):
    product_dict = {}  # Renamed to avoid confusion with function name
    for i in range(1, num + 1):
        print(f"\nProduit {i}:")
        reference = int(input("Enter le reference de produit: "))
        quan = int(input("Enter la quantite: "))
        product_dict[reference] = quan
    return product_dict

def check_condition():
    num = int(input("Enter le nombre des produits: "))
    user_products = get_products(num)  # Get user input products
    
    db_products = mydb()  # Get products from database
    
    print("\nChecking products against database:")
    for ref, quantity in user_products.items():
        found = False
        for db_product in db_products:
            if db_product[0] == ref:  # Compare reference numbers
                print(f"Reference {ref}: True (Available quantity: {db_product[3]})")
                found = True
                break
        if not found:
            print(f"Reference {ref}: False (Not found in database)")

# Main execution
if __name__ == "__main__":
    check_condition()









