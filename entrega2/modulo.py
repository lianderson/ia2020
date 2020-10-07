import math
from googlesearch import search
from goose3 import Goose
import datetime #https://www.w3schools.com/python/python_datetime.asp

def soma(valor,total):
    valor = float(valor.replace(',', '.'))
    total = total + valor
    return total

def media(total,count):
    total = total/count
    return total


def raiz(val,nomentrega2/crv.pye):
    val = float(val.replace(',', '.'))
    print("Nome "+nome+" raiz: R$ " + str(math.sqrt(val)))


def getFontes(buscar):
    urls = []
    for i in (search(buscar,tld="com.br",num=15,stop=3,pause=2)):
        urls.append(i)
    print(urls)
    return urls

def getHtml(urls):
    noticias = []
    for i in urls:
        g  =  Goose()
        noticia  =  g.extract(url=i)
        print("\nNoticia: "+i)
        #print(noticia.title)
        #print(noticia.cleaned_text)
        noticias.append(noticia.cleaned_text)
    return noticias

def gravaArquivo(arquivo,noticia):
    for i in noticia:
        today = datetime.datetime.now();
        today = today.strftime("%d/%m/%Y %H:%M:%S")
        f = open(arquivo, 'a')
        f.write(str(today)+"\n" + i+"\n")
        f.close()