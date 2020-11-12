# ===============================================================================
# inteligencia artificial
# data: 2020 11 11
# script: desenvolver um codigo para trazer as informacoes de acoes do banco e preencher um array para utilizar com datafrae
# autores: mauricio zaquia, lindice lopes, gustavo berté
# ===============================================================================

# ===============================================================================
# importando as bibliotecas
# ===============================================================================
import moduloNonaEntrega as mqe
#import schedule
#import time
import pymysql
import numpy as np
import pandas as pd
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
#tipo = input("Digite 0 para barra 1 para linha: ")

# ===============================================================================
# conexao com o banco
# ===============================================================================
conexao = pymysql.connect(host='viajuntos.com.br',user='admin_ia', password='admin_ia', db='admin_ia')
# ===============================================================================
# gerando o grafico
# ===============================================================================
arrayPreco = []
arrayId = []
cursor_banco = conexao.cursor()
sql = "SELECT c.preco, c.data_importacao, a.nome, c.acao_id FROM cotacao c  JOIN acao a ON a.id = c.acao_id WHERE equipe_id = 2 AND a.nome = '%s' ORDER BY data_importacao" % (acao)
cursor_banco.execute(sql)
for linhas in (cursor_banco.fetchall()):
    arrayPreco.append(linhas[0])
    arrayId.append(linhas[3])
    data = str(linhas[1])
    data = data[0:19]
    arrayData.append(data)
cursor_banco.close()

#data = {'nome': ['lianderson', 'Paulo', 'Joao'], 'idade': [43, 22, 19]}
#print(arrayPreco)

data = {'0': arrayPreco, 'acao_id' : arrayId}
df = pd.DataFrame(data)
inf = mqe.retornaInfoMat(df)

id_equipe = 2
acao_id = arrayId[0]
soma = inf[0]
quantidade = inf[1]
minimo = inf[2]
maximo = inf[3]
desvio_padrao = inf[4]
media = inf[5]

# ===============================================================================
# inserindo as palavras na tabela equipe2_palavra no banco
# ===============================================================================
cursor_banco = conexao.cursor()
sql = 'INSERT INTO equipe2_analise(equipe_id, acao_id, soma,quantidade,minimo,maximo,desvio_padra,media)  values(%s,%s,%s,%s,%s,%s,%s,%s) ' % (id_equipe, acao_id, soma, quantidade, minimo, maximo, desvio_padrao, media)
print(sql)
cursor_banco.execute(sql)
conexao.commit()
cursor_banco.close()

conexao.close()