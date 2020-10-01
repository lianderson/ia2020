import csv
import math
import requests
from googlesearch import search
from goose3 import Goose
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


def pesquisa(resultado):
    url = []
    print(resultado)
    consulta = resultado
    for i in (search(consulta, tld="co.in", num=5, stop=10, pause=2)):
        url.append(i)
        print(url)

    for noticia in url:
        g = Goose()
        noticias = g.extract(url=noticia)
        print(noticias.title)
        print(noticias.cleaned_text)
        print(noticias.publish_datetime_utc)
    g.close()









