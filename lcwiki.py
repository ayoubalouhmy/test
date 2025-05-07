def calcul(n):
    data = []
    for i in range(nombre):
        article = float(input(f"Articles{i+1}:"))
        data.append(article)
        data.sort()
    r = n//4
    for i in range (r):
        data.remove(i)
    return data

    



nombre = int(input("Enter le nombre d´articles:"))


print(calcul(nombre))


def calcul(n):
    data = []
    for i in range(n):
        article = float(input(f"Article {i+1}: "))
        data.append(article)
    data.sort()
    r = n // 4
    for j in range(r):
        data.pop(0)
    for l in data:
        result = sum(data)
    return result

nombre = int(input("Enter le nombre d'articles: "))
print(calcul(nombre))

