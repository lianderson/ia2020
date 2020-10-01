# COMANDOS DE DATA
#
#curr_datetime = datetime.now()
#curr_date = curr_datetime.date()
#curr_time = curr_datetime.time()
#curr_hour = curr_datetime.hour
#curr_min = curr_datetime.minute
#curr_sec = curr_datetime.second
#

# ===============================================================================
# importando as bibliotecas
# ===============================================================================

from goose3 import Goose
from googlesearch import search
from datetime import datetime

# ===============================================================================
# criando a funcao para pesquisar no google search
# ===============================================================================

def retornaURL(consulta):
    lista = search(consulta, num_results=1, lang="pt-br")
    return lista

# ===============================================================================
# criando a funcao para separar URL
# ===============================================================================

def retornaInformacoesSite(site_url):
    g = Goose()
    noticia = g.extract(url=site_url)

    arrayNoticia = [noticia.title, noticia.cleaned_text, noticia.publish_date]

    return(arrayNoticia)
