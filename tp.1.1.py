from math import pi

def cube(c):
    a = 6 * c**2
    v = c**3
    return f"L'aire de ce cube est: {a} \nLe volume de ce cube est: {v}"

def sphere(r):
    a = 4 * pi * r**2
    v = (4 * pi * r**3) / 3
    return f"L'aire de cette sphère est: {a} \nLe volume de cette sphère est: {v}"

def cylindre(r, h):
    a = 2 * pi * r * h + 2 * pi * r**2
    v = pi * r**2 * h
    return f"L'aire de ce cylindre est: {a} \nLe volume de ce cylindre est: {v}"

def cone(r, h, a):
    surface_area = pi * r * a + pi * r**2
    v = (pi * r**2 * h) / 3
    return f"L'aire de ce cône est: {surface_area} \nLe volume de ce cône est: {v}"

def pyramide(pb, ab, h, a):
    surface_area = (pb * a) / 2 + ab
    v = (ab * h) / 3
    return f"L'aire de cette pyramide est: {surface_area} \nLe volume de cette pyramide est: {v}"

def choice(s):
    try:
        if s == 1:
            c = int(input("Entrez le côté du cube : "))
            return cube(c)
        elif s == 2:
            r = int(input("Entrez le rayon de la sphère : "))
            return sphere(r)
        elif s == 3:
            r = int(input("Entrez le rayon du cylindre : "))
            h = int(input("Entrez la hauteur du cylindre : "))
            return cylindre(r, h)
        elif s == 4:
            r = int(input("Entrez le rayon du cône : "))
            h = int(input("Entrez la hauteur du cône : "))
            a = int(input("Entrez l'apothème du cône : "))
            return cone(r, h, a)
        elif s == 5:
            pb = int(input("Entrez le périmètre de la base de la pyramide : "))
            ab = int(input("Entrez l'aire de la base de la pyramide : "))
            h = int(input("Entrez la hauteur de la pyramide : "))
            a = int(input("Entrez l'apothème de la pyramide : "))
            return pyramide(pb, ab, h, a)
        else:
            return "Erreur: Choix invalide"
    except ValueError:
        return "Erreur: Veuillez entrer un nombre valider."

try:
    solides = int(input("""Choisir un solide:
1 - Cube
2 - Sphère
3 - Cylindre
4 - Cône
5 - Pyramide : """))
    
    print(choice(solides))
except ValueError:
    print("Erreur: Veuillez entrer un nombre valide pour choisir un solide.")