import math
from googlesearch import search
from goose3 import Goose

def soma(valor,total):
    valor = float(valor.replace(',', '.'))
    total = total + valor
    return total

def media(total,count):
    total = total/count
    return total


def raiz(val,nome):
    val = float(val.replace(',', '.'))
    print("Nome "+nome+" raiz: R$ " + str(math.sqrt(val)))


def pegaHTML(buscar):
    #consulta = "ABEV3"
    urls = []

    for i in (search(buscar,tld="com.br",num=15,stop=2,pause=2)):
        urls.append(i)

    print(urls)

    for i in urls:
        g  =  Goose()
        noticia  =  g.extract(url=i)
        print("\nNoticia:")
        print(noticia.title)
        print(noticia.cleaned_text)
