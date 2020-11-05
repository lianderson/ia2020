import Aulas.ia2020.entrega6.modulo as mod

try :
    acoes = mod.executaDB("SELECT id,nome FROM acao where id_equipe = '5'",None)
    gravarDB = "SIM"
    fonte = ["https://br.financas.yahoo.com/quote/ITUB3.SA/", "https://br.financas.yahoo.com/quote/PNVL4.SA/"]
    fonte = None

    for i in acoes:
        #Retorna uma lista com as fontes
        print(i[1])
        #if fonte is None:
        fonte=mod.getUrlGoogle(i[1])
        noticia = mod.getHtml(fonte,gravarDB,i[0])
        #else:
        # noticia = mod.getHtml(fonte, gravarDB, i[0])
except Exception as e:
    print(e)