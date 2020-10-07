from googlesearch import search
from goose3 import Goose
import datetime #https://www.w3schools.com/python/python_datetime.aspentrega3entrega3


def getFontes(buscar):
    urls = []
    for i in (search(buscar,tld="com.br",num=15,stop=3,pause=2)):
        urls.append(i)
    print(urls)
    return urls

def getHtml(urls):
    noticias = []
    for i in urls:
        g=Goose()
        noticia=g.extract(url=i)
        hoje = datetime.datetime.now()
        if(noticia.publish_date != None):
            artigoData = noticia.publish_date.split('T')
            dataHoje = hoje.strftime("%Y-%m-%d")
            print(artigoData[0])
            print(dataHoje)
            if str(dataHoje) != str(artigoData[0]):
               print("\nNoticia Antiga : "+i +" Data "+ artigoData[0])
        noticias.append(noticia.cleaned_text)
    return noticias

def gravaArquivo(arquivo,noticia):
    for i in noticia:
        hoje = datetime.datetime.now();
        data = hoje.strftime("%d/%m/%Y")
        hoje = hoje.strftime("%d/%m/%Y %H:%M:%S")
        f = open(arquivo, 'a')
        f.write(str(hoje)+"\n" + i+"\n")
        f.close()