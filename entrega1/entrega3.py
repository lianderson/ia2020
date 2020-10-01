import Aulas.ia2020.entrega1.modulo as mod

acoes = ['ITUB3','PNVL4','ABEV3']

for i in acoes:
    fonte=mod.getFontes('ABEV3')
    noticia = mod.getHtml(fonte)
    mod.gravaArquivo("noticia"+str(i)+".txt",noticia)