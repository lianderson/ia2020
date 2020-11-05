# ===============================================================================
# inteligencia artificial
# data: 2020 10 07
# script: desenvolver script parar pesquisar as informacoes das empresas utiolizando api do yahoo
# autores: mauricio zaquia, lindice lopes, gustavo berté
# ===============================================================================

# ===============================================================================
# importando as bibliotecas
# ===============================================================================
import moduloOitavaEntrega as mqe
#import schedule
#import time
import pymysql
from datetime import datetime

# ===============================================================================
# criacao de variaveis
# ===============================================================================
arrayPreco = []
arrayData = []

# ===============================================================================
# criando a funcao para rodar a busca
# ===============================================================================
arrayAcoes = [] #limpando o arrayacoes (lista) para nao duplicar as cotacoes
# ===============================================================================
# conexao com o banco
# ===============================================================================
conexao = pymysql.connect(host='viajuntos.com.br',user='admin_ia', password='admin_ia', db='admin_ia')
# ===============================================================================
# fazendo o select das acoes
# ===============================================================================    
cursor_banco = conexao.cursor()
sql = "SELECT c.preco, c.data_importacao FROM cotacao c WHERE equipe_id = 2"
cursor_banco.execute(sql)
for linhas in (cursor_banco.fetchall()):
    arrayPreco.append(linhas[0])
    arrayData.append(linhas[1])
cursor_banco.close()

plt.plot(arrayData,arrayPreco)
plt.xlabel("Data")
plt.ylabel("Preço")
lt.show()    