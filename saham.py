def typedepack(choix):
    packs = {
        1: {"nom": "Responsabilite civile", "prix": 2500.00},
        2: {"nom": "Dommage collision", "prix": 2500.00 + 2500.00 * 0.4258},  
        3: {"nom": "Tous risques", "prix": 2500.00 + 2500.00 * 0.8351}      
    }
    return packs.get(choix, {"nom": "", "prix": 0})

def ancienneteDuPermis(annees):
    a = 2025-annees
    if a >= 17:
        return 0.18
    elif 11 <= a <= 16:
        return 0.10
    elif 5 <= a <= 10:
        return 0.05
    else:
        return 0
    
def ancienneteVoiture(t):
    r = 2025-t
    if r > 0:
        return r/100
    else:
        return 0

def calcul(pack_choix, annee_circul, annee_permis):
    pack = typedepack(pack_choix)
    montant = pack["prix"]
    
    reduction_circulation = ancienneteVoiture(annee_circul) * montant
    reduction_permis = ancienneteDuPermis(annee_permis) * montant
    
    total = montant - reduction_circulation - reduction_permis
    
    return {
        "pack_info": pack,
        "montant": montant,
        "reduction_circulation": reduction_circulation,
        "reduction_permis": reduction_permis,
        "total": total,
        "annees_circulation": 2025 - annee_circul,
        "annees_permis": 2025 - annee_permis
    }

# Entrées utilisateur
marque = input("La marque du voiture: ")
modele = input("Model du voiture: ")
annee_circul = int(input("Annee de la 1er mise en circulation: "))
annee_permis = int(input("Annee d'obtention du permis: "))
pack = int(input("""
########choisir les pack:########
1. Responsabilité civile
2. Dommage collision
3. Tous risques
Votre choix (1-3): """))

resultat = calcul(pack, annee_circul, annee_permis)



output_text = f"""===== FACTURE =====
Voiture : {marque}
Model : {modele}
Pack choisi : {resultat['pack_info']['nom']}
Voiture mise en circulation: {annee_circul}
Réduction années de circulation ({resultat['annees_circulation']} ans) : -{resultat['reduction_circulation']:.2f} MAD
Réduction ancienneté permis ({resultat['annees_permis']} ans) : -{resultat['reduction_permis']:.2f} MAD
Total TTC : {resultat['total']:.2f} MAD
"""
with open("facture_Saham.txt", "w") as file:
    file.write(output_text)
    print("Facture enregistrée dans 'facture_Saham.txt'")



