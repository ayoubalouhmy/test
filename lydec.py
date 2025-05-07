def cal_elec(consommation):
    if 1 <= consommation <= 150:
        if consommation <= 100:
            montant = consommation * 0.8349
        else:
            montant = 100 * 0.8349 + (consommation - 100) * 1.0044
    elif 150 < consommation <= 210:
        montant = consommation * 1.0044
    elif 210 < consommation <= 310:
        montant = consommation * 1.0928
    elif 310 < consommation <= 510:
        montant = consommation * 1.2930
    else:  # for consumption > 510
        montant = consommation * 1.4931
    
    tva = montant * 0.16
    total = montant + tva
    
    return { 
        "montant_ht": round(montant, 2),
        "tva": round(tva, 2),
        "total_ttc": round(total, 2)
    }


def cal_eau(consommation):
    if 1 <= consommation <= 12:
        if consommation <= 6:
            montant_ht = consommation * 2.99
        else:
            montant_ht = 6 * 2.99 + (consommation - 6) * 6.00
    elif 12 < consommation <= 20:
        montant_ht = consommation * 6.00
    elif 20 < consommation <= 35:
        montant_ht = consommation * 11.24
    else:  
        montant_ht = consommation * 16.48
    return {
        "montant_ht": round(montant_ht, 2),
        "tva": 0,
        "total_ttc": round(montant_ht, 2),
    }

def affichage(elc, eau):
    facture_elec = cal_elec(elc)
    facture_eau = cal_eau(eau)
    total_general = facture_elec['total_ttc'] + facture_eau['total_ttc']

    output_text = f"""
    === Programme de Facturation Lydec ===
        === Facture d'Électricité ===
Consomation KWh: {facture_elec['montant_ht']} MAD
TVA (16%): {facture_elec['tva']} MAD
Total TTC: {facture_elec['total_ttc']} MAD

            === Facture d'Eau ===
Consommation m3: {facture_eau['montant_ht']} MAD
TVA (0%): {facture_eau['tva']} MAD
Total TTC: {facture_eau['total_ttc']} MAD
Total des deux factures: {round(total_general, 2)} MAD"""
    
    with open("facture_lydec.txt", "w") as file:
        file.write(output_text)
        print("Facture enregistrée dans 'facture_lydec.txt'")


elc = float(input("Enter la consomatio mensuelle de l´electricite (enKWh): "))
eau = float(input("Enter la consomatio mensuelle de l´eau (en m3): "))

affichage(elc, eau)
