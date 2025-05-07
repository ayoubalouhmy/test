import string
from score import evaluer_force_mdp

alphabet_lower = string.ascii_lowercase
alphabet_upper = string.ascii_uppercase


def user_verf(user):
    if user[0] in alphabet_lower or user[0] in alphabet_upper:
        for lettre in user:
            if lettre != " ":
                continue
            else:
                return "essayez encore"
        return user
    else:
        return "essayez encore"
    
def mdp_verf(mdp):
    force = evaluer_force_mdp(mdp)
    print(f"Force du mot de passe: {force}")
    if force == "Très Faible":
        print("Votre mot de passe est trop faible. Veuillez en choisir un plus sécurisé.")
        return "Mot de passe trop faible"
    if len(mdp) > 8:
        contient_majuscule = False
        for lettre in mdp:
            if lettre in alphabet_upper:
                contient_majuscule = True
                break
        if contient_majuscule:
            mdp_re = input("verf ton mode passe: ")
            if mdp == mdp_re:
                return "Mot de passe accepté"
            else:
                return "Vérification du mot de passe échouée"
        else:
            return "Le mot de passe doit contenir au moins une lettre majuscule"
    else:
        return "Le mot de passe doit contenir plus de 8 caractères"
while True:
    user_name = input("Entrez le nom : ")
    user_result = user_verf(user_name)
    
    if user_result != "essayez encore":
        print(f"Nom d'utilisateur '{user_result}' est valide")
        while True:
            mdp = input("Entrez le mot de passe : ")
            mdp_result = mdp_verf(mdp)
            print(mdp_result)
            if mdp_result == "Mot de passe accepté":
                exit()
            else:
                print("Veuillez réessayer avec un mot de passe valide.")
    else:
        print("Nom d'utilisateur invalide, veuillez commencer par une lettre et éviter les espaces")