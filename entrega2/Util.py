import csv
import math
data = csv.reader(open('C:\\Users\\jonat\\\Downloads\\cotacoes1.txt', newline=''), delimiter='|', quotechar='|')

def ler_csv():
    cotacoes = []
    for row in data:
        try:
            cotacoes.append(row)
        except Exception as e:
            print(e)
    return cotacoes


def raiz_quadrada():
    dados = ler_csv()
    for valor in dados:
        try:
            dados_cotacao = valor[2].split(':')[1]
            raiz = math.sqrt(float(dados_cotacao))
            print(raiz)
        except Exception as e:
            print(e)









