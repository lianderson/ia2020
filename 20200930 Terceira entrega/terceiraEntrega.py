# ===============================================================================
# inteligencia artificial
# data: 2020 09 30
# script: desenvolver script parar pesquisar as acoes no google search e com o goose analisar cada url
# autores: mauricio zaquia, lindice lopes, gustavo berté
# ===============================================================================

import moduloTerceiraEntrega

# ===============================================================================
# lista de acoes
# ===============================================================================

acao = ["BBSE3", "CCRO3", "UNIP3"]

# ===============================================================================
# lendo os sites
# ===============================================================================

for a in (acao):
    # retorna lista de urls
    lista = moduloTerceiraEntrega.retornaURL(a)

    for i in (lista):
        # retorna noticias de acordo com cada url
        noticia = moduloTerceiraEntrega.retornaInformacoesSite(i)

        print("===============================================================================")
        print("TITULO")
        print("===============================================================================")
        print(noticia[0])
        print("===============================================================================")
        print("DATA")
        print("===============================================================================")
        print(noticia[2])        
        print("===============================================================================")
        print("NOTICIA")
        print("===============================================================================")
        print(noticia[1])