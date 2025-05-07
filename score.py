import string

alphabet_lower = string.ascii_lowercase
alphabet_upper = string.ascii_uppercase

def pwd_force(pwd):
    nb = 0
    for k in pwd:
        if k == alphabet_lower:
            nb += 1
    return nb

def NbCMaj(pwd):
    nb = 0
    for k in pwd:
        if k == alphabet_upper:
            nb += 1
    return nb

def NbCAlpha(pwd):
    nb = 0
    for k in pwd:
        if not (alphabet_upper or alphabet_lower):
            nb += 1
    return nb



def Score(pwd):
    nbcar = len(pwd)
    nbcarmaj = NbCMaj(pwd)
    nbcaraplha = NbCAlpha(pwd)
    Score = nbcar * 4 + (nbcar-nbcarmaj) * 2 + nbcaraplha * 5
    return Score

def evaluer_force_mdp(mdp):
    S = Score(mdp)
    print(f"Score du mot de passe: {S}")
    
    if S < 20:
        return "Très Faible"
    elif S < 40:
        return "Faible"
    elif S < 80:
        return "Fort"
    else:
        return "Très Fort"