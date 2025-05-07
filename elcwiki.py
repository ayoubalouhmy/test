def calculer_reduction(taille, prix):
    if taille in ['XXXL', 'XXL']:
        return 0.60
    elif taille in ['XL', 'L'] and prix > 400:
        return 0.45
    elif prix > 500:
        return 0.40
    elif 300 <= prix <= 500:
        return 0.30
    elif taille in ['S', 'M'] and prix < 300:
        return 0.15
    elif prix < 300:
        return 0.25
    else:
        return 0.0

def calculer_prix_article(taille, prix):
    reduction = calculer_reduction(taille, prix)
    prix_reduit = prix * (1 - reduction)
    return round(prix_reduit, 2)

def affichage():
    nombre_articles = int(input("Nombre d'articles choisi : "))
    total = 0.0
    
    for i in range(nombre_articles):
        print(f"\nArticle {i+1}:")
        taille = input("Taille (S, M, L, XL, XXL, XXXL) : ").upper()
        prix = float(input("Prix (MAD) : "))
        prix_reduit = calculer_prix_article(taille, prix)
        print(f"→ Prix après réduction : {prix_reduit} MAD")
        total += prix_reduit
    
    livraison = 0.0 if total >= 350 else 35.0
    total_ttc = total + livraison
    
    print("\n--- RÉSUMÉ DE L'ACHAT ---")
    print(f"Total avant livraison : {total:.2f} MAD")
    if livraison > 0:
        print(f"Frais de livraison : {livraison:.2f} MAD")
    else:
        print("Livraison gratuite !")
    print(f"Prix TTC : {total_ttc:.2f} MAD")

affichage()