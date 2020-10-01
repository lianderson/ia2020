from googlesearch import search
from goose3 import Goose


def consulta(termo, qnt):
    return search(termo, num_results=qnt, lang="br")

def get_simple_page(url):
    g = Goose()
    noticia = g.extract(url=url)
    retorno = "noticia"
    retorno += "\n" + noticia.title + " - " + str(noticia.publish_date)
    retorno += "\n---------------------"
    retorno += "\n" + noticia.cleaned_text
    retorno += "\nfim noticia\n\n\n"
    return retorno

arr = ["lwsa3 noticia","slce3 noticia", "klbn4 noticia"]
resultado = ""
for url in arr:
    for result in consulta(url, 5):
        resultado += get_simple_page(result)

file = open("Noticias.txt", "w") 
file.write(resultado) 
file.close()

print(resultado)




