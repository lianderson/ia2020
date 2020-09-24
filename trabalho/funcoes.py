import csv
import math

def retornaValores():
    data = csv.reader(open('trabalho/cotacao.csv', newline=''), delimiter=',', quotechar=',')
    vetor = []

    for row in data:
        try:
            vetor.append(float(row[2]))
        except Exception as e:
            print(e)

    return vetor

def printaRaiz():
    data = csv.reader(open('trabalho/cotacao.csv', newline=''), delimiter=',', quotechar=',')
    retorno = ""
    for row in data:
        try:
            retorno += "\n" + row[0] + " - " + row[1] + " - " + row[2] + " - sqrt = " + str(math.sqrt(float(row[2])))
        except Exception as e:
            print(e)

    print(retorno)

def calculaRaiz():
    valores = retornaValores()
    vetor = []
    for row in valores:
        try:
            vetor.append(math.sqrt(row))
        except Exception as e:
            print(e)

    print(vetor)

