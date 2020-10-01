import math
from googlesearch import search
from goose3 import Goose

def calcula_raiz(valor):
    raiz = math.sqrt(float(valor))
    return(raiz)

def pesquisa(consulta):



    for i in (search(consulta, tld="co.in", num=5, stop=4, pause=2)):
        url = i

        print(i)
        g = Goose()


        noticia = g.extract(url)

        return noticia.cleaned_text