import csv
import math

def retornaValores():
    data = csv.reader(open('C:\\Users\\Gabriel Soares\\Documents\\Faculdade\\IntArtificial\\cotacao.csv', newline=''), delimiter=',', quotechar=',')
    vetor = []

    for row in data:
        try:
            vetor.append(float(row[2]))
        except Exception as e:
            print(e)

    return vetor

def calculaRaiz():
    valores = retornaValores()
    vetor = []
    for row in valores:
        try:
            vetor.append(math.sqrt(row))
        except Exception as e:
            print(e)

    print(vetor)

