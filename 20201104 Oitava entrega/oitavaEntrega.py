# ===============================================================================
# inteligencia artificial
# data: 2020 11 04
# script: desenvolver script parar gerar grafico de data e preco
# autores: mauricio zaquia, lindice lopes, gustavo berté
# ===============================================================================

# ===============================================================================
# importando as bibliotecas
# ===============================================================================
import moduloOitavaEntrega as mqe
#import schedule
#import time
import pymysql
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# ===============================================================================
# criacao de variaveis
# ===============================================================================
arrayPreco = []
arrayData = []

acao = ''
tipo = ''

# ===============================================================================
# perguntando a acao e o tipo de grafico
# ===============================================================================
acao = input("Digite o nome da acao: ")
tipo = input("Digite 0 para barra 1 para linha: ")

# ===============================================================================
# conexao com o banco
# ===============================================================================
conexao = pymysql.connect(host='viajuntos.com.br',user='admin_ia', password='admin_ia', db='admin_ia')
# ===============================================================================
# gerando o grafico
# ===============================================================================
arrayPreco = []
arrayData = []
cursor_banco = conexao.cursor()
sql = "SELECT c.preco, c.data_importacao, a.nome FROM cotacao c  JOIN acao a ON a.id = c.acao_id WHERE equipe_id = 2 AND a.nome = '%s' ORDER BY data_importacao" % (acao)
cursor_banco.execute(sql)
for linhas in (cursor_banco.fetchall()):
    arrayPreco.append(linhas[0])
    data = str(linhas[1])
    data = data[0:19]
    arrayData.append(data)
cursor_banco.close()

if (str(tipo) == "0"):
    plt.bar(arrayData, arrayPreco)
    plt.xlabel("Data")
    plt.ylabel("Preço")
    plt.show()
if (str(tipo) == "1"):
    plt.plot(arrayData,arrayPreco)
    plt.xlabel("Data")
    plt.ylabel("Preço")
    plt.show()