from datetime import datetime
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
    g.close()
    return retorno

def check_url(url):
    retorno = 0
    g = Goose()
    noticia = g.extract(url=url)
    if(noticia._publish_datetime_utc):
        agora_unf = datetime.now()
        data_unf = noticia.publish_datetime_utc
        agora = datetime.strptime(str(agora_unf.day)+"-"+str(agora_unf.month)+"-"+str(agora_unf.year), "%d-%m-%y")
        data = datetime.strptime(str(data_unf.day)+"-"+str(data_unf.month)+"-"+str(data_unf.year), "%d-%m-%y")
        tempoEntre = agora - data
        if(tempoEntre.days <= 7):
            retorno = 1
    
    return retorno

"""
ate_time_str = '2018-06-29 08:15:27.243860'
date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')

print('Date:', date_time_obj.date())
print('Time:', date_time_obj.time())
print('Date-time:', date_time_obj)
"""
arr = ["lwsa3 noticia","slce3 noticia", "klbn4 noticia"]
resultado = ""
for url in arr:
    for result in consulta(url, 10):
        if(check_url(result) == 1):
            resultado += get_simple_page(result)

file = open("Noticias.txt", "w") 
file.write(resultado) 
file.close()

print(resultado)




