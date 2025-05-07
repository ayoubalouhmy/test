from bimdb import mydb

def get_products(num):
    product = {}
    for i in range(1, num + 1):

        print(f"\nProduit {i}:")
        reference = int(input("Enter le reference de produit: "))
        quan = int(input("Enter la quantite: "))
        product[reference] = quan
    return product

def check_condition(num):
    user_products = get_products(num)
    db_products = mydb()
    print("\n chearcher pour les produits:")
    for ref, quantity in user_products.items():
        for product in db_products:
            if product[0] == ref:
                print(f"Reference {ref}: True (Available quantity: {product[3]})")
                














num = int(input("Enter le nombre des produits: "))

print(check_condition(num))



