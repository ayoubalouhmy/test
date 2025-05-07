def calcul_salaire(s, a):
    if a <= 2:
        taux = 0
    elif 2 < a <= 5:
        taux = 5/100
    elif 5 < a <= 12:
        taux = 10/100
    elif 12 < a <= 20:
        taux = 15/100
    elif 20 < a <= 25:
        taux = 20/100
    else:
        taux = 25/100
    
    prime_anc = s * taux
    salaire_brut = s + prime_anc
    return salaire_brut


def Calcul_Tax(salaire_brut):
    CNSS = 4.48/100
    AMO = 2.26/100
    Retirement = 6/100
    Prof_expenses = 20/100

    cnss_amount = salaire_brut * CNSS
    amo_amount = salaire_brut * AMO
    retirement_amount = salaire_brut * Retirement
    prof_expenses_amount = salaire_brut * Prof_expenses

    salaire_net_imp = salaire_brut - (cnss_amount + amo_amount + retirement_amount + prof_expenses_amount)
    
    return {
        'salaire_net_imp': salaire_net_imp,
        'CNSS': cnss_amount,
        'AMO': amo_amount,
        'Retirement': retirement_amount,
        'Prof_expenses': prof_expenses_amount,
    }


def IR(salaire_net_imposable):
    if salaire_net_imposable <= 2500:
        ir = 0
    elif salaire_net_imposable <= 4164:
        ir = (salaire_net_imposable - 2501) * 0.10
    elif salaire_net_imposable <= 5000:
        ir = (4164 - 2501) * 0.10 + (salaire_net_imposable - 4167) * 0.20
    elif salaire_net_imposable <= 6666:
        ir = (4164 - 2501) * 0.10 + (5000 - 4167) * 0.20 + (salaire_net_imposable - 5001) * 0.30
    elif salaire_net_imposable <= 15000:
        ir = (4164 - 2501) * 0.10 + (5000 - 4167) * 0.20 + (6666 - 5001) * 0.30 + (salaire_net_imposable - 6667) * 0.34
    else:
        ir = (4164 - 2501) * 0.10 + (5000 - 4167) * 0.20 + (6666 - 5001) * 0.30 + (15000 - 6667) * 0.34 + (salaire_net_imposable - 15001) * 0.38
    return ir


def net_salaire(salaire_brut):
    taxes = Calcul_Tax(salaire_brut)
    ir= IR(taxes['salaire_net_imp'])
    
    salaire_net = salaire_brut - taxes['CNSS'] - taxes['AMO'] - taxes['Retirement'] - ir
    return salaire_net

def affichage(salaire_base,anc):
    salaire_brut = calcul_salaire(salaire_base, anc)
    taxes = Calcul_Tax(salaire_brut)
    ir_amount = IR(taxes['salaire_net_imp'])
    salaire_net = net_salaire(salaire_brut)

    print("\nRésultats de calcul:")
    print(f"Salaire brut: {salaire_brut:.2f} MAD")
    print(f"Salaire net imposable: {taxes['salaire_net_imp']:.2f} MAD")
    print(f"CNSS: {taxes['CNSS']:.2f} MAD")
    print(f"AMO: {taxes['AMO']:.2f} MAD")
    print(f"Retraite: {taxes['Retirement']:.2f} MAD")
    print(f"IR: {ir_amount:.2f} MAD")
    print(f"Salaire net: {salaire_net:.2f} MAD")



salaire_base = float(input("Entrez le salaire de base: "))
anc = int(input("Saisir l'ancienneté: "))

affichage(salaire_base,anc)

