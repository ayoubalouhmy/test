def pair(number):
    liste = []
    for i in range(len(number)) :
        liste.append(int(number[i]))
    print(liste)
    s=0
    for j in range(len(liste)):
        if liste[j]%2==0:
            s+=liste[j]
    print(s)
    
    
x = input("Enter les number:")
pair(x)