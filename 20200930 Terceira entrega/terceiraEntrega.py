# ===============================================================================
# inteligencia artificial
# data: 2020 09 30
# script: desenvolver script parar pesquisar as acoes no google search e com o goose analisar cada url
# autores: mauricio zaquia, lindice lopes, gustavo berté
# ===============================================================================

import moduloTerceiraEntrega

# ===============================================================================
# criação das variaveis
# ===============================================================================

caminho = 'D:\\Projetos\\python\\InteligenciaArtificial\\#github\\ia2020\\20200930 Terceira entrega\\info.csv'

acao = ''
data = ''
titulo = ''
noticia = ''

# ===============================================================================
# lista de acoes
# ===============================================================================

acoes = ["BBSE3", "CCRO3", "UNIP3"]

# ===============================================================================
# lendo os sites
# ===============================================================================

for a in (acoes):
    # retorna lista de urls
    listaUrls = moduloTerceiraEntrega.retornaURL(a)

    for i in (listaUrls):
        # retorna noticias de acordo com cada url
        arrayNoticia = moduloTerceiraEntrega.retornaInformacoesSite(i)

        print("===============================================================================")
        print("TITULO")
        print("===============================================================================")
        print(arrayNoticia[0])
        print("===============================================================================")
        print("DATA")
        print("===============================================================================")
        print(arrayNoticia[2])
        print("===============================================================================")
        print("NOTICIA")
        print("===============================================================================")
        print(arrayNoticia[1])

        acao = a
        data = arrayNoticia[2]
        titulo = arrayNoticia[0]
        noticia = arrayNoticia[1]

        # escrever arquivo
        f = open(caminho, 'a')
        f.write(acao + ';' + str(data) + ';' + titulo + ';' + noticia + '\n')
        f.close()
