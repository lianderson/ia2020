import Aulas.ia2020.entrega5.modulo as mod


acoes = mod.executaDB("SELECT id,nome FROM acao where id_equipe = '5'",None)


gravarDB = "SIM"
fonte = ["https://br.financas.yahoo.com/quote/ITUB3.SA/", "https://br.financas.yahoo.com/quote/PNVL4.SA/"]
fonte = None

for i in acoes:
    #Retorna uma lista com as fontes
    if fonte is None:
        fonte=mod.getUrlGoogle(i[1])
    noticia = mod.getHtml(fonte,gravarDB,i[0])
    #print(noticia)
    #mod.gravaArquivo("noticia"+str(i)+".txt",noticia)