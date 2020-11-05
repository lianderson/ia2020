import numpy as np
import matplotlib . pyplot as plt
import pymysql
import time

def busca_cotacoes(equipe):
    conexao = pymysql.connect(host='viajuntos.com.br',
                              user='admin_ia', passwd='admin_ia', db='admin_ia')
    cursor_banco = conexao.cursor()
    sql = "SELECT * FROM acao WHERE id_equipe = " + str(equipe)
    cursor_banco.execute(sql)
    conexao.close()
    return cursor_banco

acoes = busca_cotacoes(3)
valores = list()
datas = list()
indexacao = 0
acao = acoes.fetchall()[indexacao]
conexao = pymysql.connect(host='viajuntos.com.br',user='admin_ia', passwd='admin_ia', db='admin_ia')
cursor_banco = conexao.cursor()
sql = "SELECT * FROM cotacao WHERE acao_id = " + str(acao[0]) + " order by data_importacao"
cursor_banco.execute(sql)
conexao.close()
for row in cursor_banco:
    valores.append(row[2])
    data = row[3]
    datas.append(data.strftime('%d/%m'))
    
fig,ax = plt.subplots()
ax.bar(datas, valores, label=("$ " + acao[1]))
ax.set_title("Valores " + acao[1])
ax.legend(loc='upper center')
plt.xlabel("Data") ####
plt.ylabel("Valor")
plt.show()
