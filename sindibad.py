def nombre(n):
    people_info = {}  
    for i in range(n):
        person_id = i + 1
        print(f"personne n{person_id}")
        taille = float(input("Taille de la personne(en cm):"))
        choix_b = input("Voulez-vous un braclet (Y/N):").lower()
        type_b = None  
        
        if choix_b == "y":
            type_b = int(input("Quel le type de braclet \n1-braclet fun\n2-braclet Extra fun:"))

        #person_id as  key 
        people_info[person_id] = {
            "taille": taille,
            "choix_b": choix_b,
            "type_b": type_b
        }
    
    return people_info
    
def braclet():
    braclet = {
        "braclet fun": 65,
        "braclet Extra fun": 125
    }
    return braclet

def attraction():
    kids = {
        "ile oak oka": 80,
        "le troubilon": 80,
        "sindi express": 80,
        "ilot enchante": 105
    }
    famille = {
        "tapis": 90,
        "la tempete": 120,
        "ibn battuta": 90,
        "aventura": 80,
        "le vertige": 90,
        "caravane": 105,
        "le toubkal": 105
    }
    sensations = {
        "le serpent": 125,
        "air rokh": 105,
        "O´Temba": 120,
        "Sibabor": 110
    }
    return kids, famille, sensations

def ticket_ent(person_info):
    taille = person_info["taille"]
    if taille < 80:
        return 0
    else:
        return 20

def choix_braclet(person_info):
    bra = braclet()
    choix = person_info["choix_b"]
    
    if choix == "y":
        type_b = person_info["type_b"]
        if type_b == 1:
            return bra["braclet fun"]
        else:
            return bra["braclet Extra fun"]
    else:
        return 0

def affichage():
    num = int(input("Enter le nombre de personne:"))
    people = nombre(num)

    total_cost = 0
import csv
from datetime import datetime

def nombre(n):
    people_info = {}  # Dictionary to store people's information
    for i in range(n):
        person_id = i + 1
        print(f"personne n{person_id}")
        taille = float(input("Taille de la personne(en cm):"))
        choix_b = input("Voulez-vous un braclet (Y/N):").lower()
        type_b = None  # Default value if no bracelet is chosen
        
        if choix_b == "y":
            type_b = int(input("Quel le type de braclet \n1-braclet fun\n2-braclet Extra fun:"))

        # Using person_id as the key in the dictionary
        people_info[person_id] = {
            "taille": taille,
            "choix_b": choix_b,
            "type_b": type_b
        }
    
    return people_info
    
def braclet():
    braclet = {
        "braclet fun": 65,
        "braclet Extra fun": 125
    }
    return braclet

def attraction():
    kids = {
        "ile oak oka": 80,
        "le troubilon": 80,
        "sindi express": 80,
        "ilot enchante": 105
    }
    famille = {
        "tapis": 90,
        "la tempete": 120,
        "ibn battuta": 90,
        "aventura": 80,
        "le vertige": 90,
        "caravane": 105,
        "le toubkal": 105
    }
    sensations = {
        "le serpent": 125,
        "air rokh": 105,
        "O´Temba": 120,
        "Sibabor": 110
    }
    return [kids, famille, sensations]

def ticket_ent(person_info):
    taille = person_info["taille"]
    if taille < 80:
        return 0
    else:
        return 20

def choix_braclet(person_info):
    bra = braclet()
    choix = person_info["choix_b"]
    
    if choix == "y":
        type_b = person_info["type_b"]
        if type_b == 1:
            return bra["braclet fun"]
        else:
            return bra["braclet Extra fun"]
    else:
        return 0

def affichage():
    # Main program logic moved to this function
    num = int(input("Enter le nombre de personne:"))
    people = nombre(num)

    # Prepare data for CSV
    csv_data = []
    total_cost = 0
    
    # Iterate through the dictionary's items
    for person_id, person in people.items():
        ticket_price = ticket_ent(person)
        bracelet_price = choix_braclet(person)
        person_total = ticket_price + bracelet_price
        
        # Display information
        print(f"Prix pour personne {person_id}: {person_total} DHs")
        total_cost += person_total
        
        # Store data for CSV
        bracelet_type = None
        if person["choix_b"] == "y" and person["type_b"] is not None:
            bracelet_type = "Fun" if person["type_b"] == 1 else "Extra Fun"
            
        csv_data.append({
            "Personne ID": person_id,
            "Taille (cm)": person["taille"],
            "Bracelet": "Oui" if person["choix_b"] == "y" else "Non",
            "Type de Bracelet": bracelet_type,
            "Prix du Ticket": ticket_price,
            "Prix du Bracelet": bracelet_price,
            "Total": person_total
        })

    print(f"Prix total avant promotion: {total_cost} DHs")
    
    # Apply 10% promotion directly 
    discount_percent = 10
    discount_amount = total_cost * (discount_percent / 100)
    discounted_total = total_cost - discount_amount
    
    print(f"Promotion appliquée: -10%")
    print(f"Prix total après promotion: {discounted_total} DHs")
    
    # Generate CSV file
    generate_csv(csv_data, discounted_total)
    
    return discounted_total

def generate_csv(data, total_with_promo):
    # Generate a filename with current date and time
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"parc_tickets_{current_time}.csv"
    
    # Write data to CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Define field names
        fieldnames = ["Personne ID", "Taille (cm)", "Bracelet", "Type de Bracelet", 
                      "Prix du Ticket", "Prix du Bracelet", "Total"]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Write each person's data
        for row in data:
            writer.writerow(row)
        
        # Add empty row and totals
        writer.writerow({})
        writer.writerow({"Personne ID": "Sous-total", "Total": sum(item["Total"] for item in data)})
        writer.writerow({"Personne ID": "Promotion -10%", "Total": sum(item["Total"] for item in data) * 0.1})
        writer.writerow({"Personne ID": "TOTAL FINAL", "Total": total_with_promo})
    
    print(f"Données sauvegardées dans le fichier '{filename}'")

# Call the affichage function to run the program
affichage()