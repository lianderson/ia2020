import Aulas.ia2020.entrega3.modulo as mod

acoes = ['ITUB3','PNVL4','ABEV3']
#acoes = ['ITUB3']
for i in acoes:
    fonte=mod.getFontes(i)
    noticia = mod.getHtml(fonte)
    mod.gravaArquivo("noticia"+str(i)+".txt",noticia)
