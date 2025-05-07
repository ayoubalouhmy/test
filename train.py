
def ville():
    v={"casa-tanger":132,"Rabat-tanger":101,
    "casa-fes":127,"rabat-fes":94,"casa-marrakech":146,
    "rabat-marrakech":183,"casa-oujda":215,"rabat-oujda":189,"casa-rabat":40}
    return v
def jours():
    js=["lundi","mardi","Mercredi","jeudi","Vendredi"]
    return js

def condition_trajet(trajet):
    v = ville()
    if trajet == 1:
        return v.get("casa-tanger")
    if trajet == 2:
        return v.get("Rabat-tanger")
    if trajet == 3:
        return v.get("casa-fes")
    if trajet == 4:
        return v.get("rabat-fes")
    if trajet == 5:
        return v.get("casa-marrakech")
    if trajet == 6:
        return v.get("rabat-marrakech")
    if trajet == 7:
        return v.get("casa-oujda")
    if trajet == 8:
        return v.get("rabat-oujda")
    if trajet == 9:
        return v.get("casa-rabat")
    
def condition(a,e,j,h):
    if jour in jours() and not(6<=h<=9 or 15<=h<=19):
         prixt = (condition_trajet(trajet)*0.7)*a+(condition_trajet(trajet)*0.5)*e
         return round(prixt,2)
    elif jour not in jours():
        prixt = (condition_trajet(trajet)*0.7)*a+(condition_trajet(trajet)*0.5)*e
        return round(prixt,2)

def affichage():
    print("""1-casa-tanger":132 MAD
          2-"Rabat-tanger":101 MAD
          3-"casa-fes":127 MAD
          4-"rabat-fes":94 MAD
          5-"casa-marrakech":146 MAD
          6-"rabat-marrakech":183 MAD
          7-"casa-oujda":40 MAD
          8-"rabat-oujda":189 MAD
          9-"casa-rabat":40 MAD
""")

affichage()

trajet = int(input("Enter le numero du trajet:"))
adulte = int(input("Enter nombre d´adultes:"))
enfant = int(input("Enter nombre d´enfants:"))
jour = input("Enter jour du voyages :").lower
heure = int(input("Enter heure du voyages en(24h):"))


print(condition(adulte,enfant,jour,heure))

