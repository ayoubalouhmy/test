def ville():
    return {
        "casa-tanger": 132,
        "Rabat-tanger": 101,
        "casa-fes": 127,
        "rabat-fes": 94,
        "casa-marrakech": 146,
        "rabat-marrakech": 183,
        "casa-oujda": 215,
        "rabat-oujda": 189,
        "casa-rabat": 40
    }

def jours_ouvres():
    return ["lundi", "mardi", "mercredi", "jeudi", "vendredi"]

def condition_trajet(trajet):
    v = ville()
    trajets = [
        "casa-tanger",
        "Rabat-tanger",
        "casa-fes",
        "rabat-fes",
        "casa-marrakech",
        "rabat-marrakech",
        "casa-oujda",
        "rabat-oujda",
        "casa-rabat"
    ]
    if 1 <= trajet <= 9:
        return v.get(trajets[trajet-1])
    return None

def calcul_prix(a, e, j, h, trajet):
    prix_base = condition_trajet(trajet)
    if prix_base is None:
        return None
    
    if j.lower() not in jours_ouvres() or not (6 <= h <= 9 or 15 <= h <= 19):
        prix_adult = prix_base * 0.7  
        prix_enfant = prix_base * 0.5  
    else:
        prix_adult = prix_base
        prix_enfant = prix_base * 0.8  
    
    prixt = (prix_adult * a) + (prix_enfant * e)
    return round(prixt, 2)

def affichage():
    print("""PROGRAMME N° 4 - Promos des trajets ONCF
Trajets disponibles:
1- Casa-Tanger: 132 MAD
2- Rabat-Tanger: 101 MAD
3- Casa-Fès: 127 MAD
4- Rabat-Fès: 94 MAD
5- Casa-Marrakech: 146 MAD
6- Rabat-Marrakech: 183 MAD
7- Casa-Oujda: 215 MAD
8- Rabat-Oujda: 189 MAD
9- Casa-Rabat: 40 MAD
""")

def main():
    affichage()
    
    try:
        trajet = int(input("Entrez le numéro du trajet (1-9): "))
        if trajet < 1 or trajet > 9:
            print("Numéro de trajet invalide. Veuillez choisir entre 1 et 9.")
            return
            
        adulte = int(input("Entrez le nombre d'adultes: "))
        enfant = int(input("Entrez le nombre d'enfants: "))
        jour = input("Entrez le jour du voyage: ").strip()
        heure = int(input("Entrez l'heure du voyage (en format 24h): "))
        
        if heure < 0 or heure > 23:
            print("Heure invalide. Veuillez entrer une heure entre 0 et 23.")
            return
            
        prix_total = calcul_prix(adulte, enfant, jour, heure, trajet)
        
        if prix_total is not None:
            print(f"\nLe prix total est de: {prix_total} MAD")
        else:
            print("Erreur dans le calcul du prix. Veuillez vérifier vos informations.")
            
    except ValueError:
        print("Erreur: Veuillez entrer des valeurs numériques valides.")

main()

