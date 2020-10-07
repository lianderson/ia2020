# ===============================================================================
# inteligencia artificial
# data: 2020 10 07
# script: desenvolver script parar pesquisar as informacoes das empresas utiolizando api do yahoo
# autores: mauricio zaquia, lindice lopes, gustavo berté
# ===============================================================================

import moduloQuartaEntrega

# ===============================================================================
# criacao de variaveis
# ===============================================================================
informacoes = ''

# ===============================================================================
# lista de acoes
# ===============================================================================
acoes = ["BBSE3.SA", "CCRO3.SA", "UNIP3.SA"]

# ===============================================================================
# lendo os dados
# ===============================================================================
for a in (acoes):
    arrayInformacoes = moduloQuartaEntrega.retornaCamposFormatados(a)
    print('============================')
    print(arrayInformacoes) 