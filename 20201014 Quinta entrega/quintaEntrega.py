# ===============================================================================
# inteligencia artificial
# data: 2020 10 07
# script: desenvolver script parar pesquisar as informacoes das empresas utiolizando api do yahoo
# autores: mauricio zaquia, lindice lopes, gustavo berté
# ===============================================================================

# ===============================================================================
# importando as bibliotecas
# ===============================================================================
import moduloQuintaEntrega as mqe
import schedule
import time

# ===============================================================================
# criacao de variaveis
# ===============================================================================
informacoes = ''

# ===============================================================================
# lista de acoes
# ===============================================================================
acoes = ["BBSE3.SA", "CCRO3.SA", "UNIP3.SA"]

# ===============================================================================
# criando a funcao para disparar
# ===============================================================================
def rodarBusca():
    # ===============================================================================
    # lendo os dados
    # ===============================================================================
    for a in (acoes):
        arrayInformacoes = mqe.retornaCamposFormatados(a)
        print(arrayInformacoes[a]['Simbolo'])
        print(arrayInformacoes[a]['Preço Atual'])

schedule.every(.1).minutes.do(rodarBusca)

while True:
    schedule.run_pending()
    time.sleep(1)
