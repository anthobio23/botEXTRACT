l = []
with open("COD.txt", "r") as file:
    lista = [linea.rstrip() for linea in file]
print(lista)
