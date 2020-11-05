import numpy as np
import matplotlib . pyplot as plt
import Aulas.ia2020.dados as dado # Nao esta no git, pois tem dados sensiveis
from googlesearch import search
from goose3 import Goose
import datetime #https://www.w3schools.com/python/python_datetime.aspentrega3entrega3
import urllib.request #pacote para trabalhar com mewb
import json #pacote para manipular JSON
import pymysql
import schedule
import time
from  collections  import Counter
import Aulas.ia2020.entrega8.modulo as mod


def busca_cotacoes(equipe):
    conexao = pymysql.connect(host='viajuntos.com.br',
                              user='admin_ia', passwd='admin_ia', db='admin_ia')
    cursor_banco = conexao.cursor()
    sql = "SELECT * FROM acao WHERE id_equipe = " + str(equipe)
    cursor_banco.execute(sql)
    conexao.close()
    return cursor_banco


acoes = busca_cotacoes(5)
valores = list()
datas = list()
indexacao = 0
acao = acoes.fetchall()[indexacao]
conexao = pymysql.connect(host='viajuntos.com.br', user='admin_ia', passwd='admin_ia', db='admin_ia')
cursor_banco = conexao.cursor()
sql = "SELECT * FROM cotacao WHERE acao_id = " + str(acao[0]) + " order by data_importacao"
cursor_banco.execute(sql)
conexao.close()
valor = mod.executaDB("SELECT valorAcao,dataHora FROM `cotacao2` where `dataHora` LIKE '%18:00:01%' AND empresa = 'PNVL4.SA' ORDER BY `cotacao2`.`id` DESC limit 10", None)

for x in valor:
    valores.append(x[0])
    data = x[1].replace('18:00:01','')
    datas.append(data)

fig, ax = plt.subplots()
ax.bar(datas, valores, label=("$ " + acao[1]))
ax.set_title("Valores " + acao[1])
ax.legend(loc='upper center')
plt.xlabel("Data")  ####
plt.ylabel("Valor")
plt.show()