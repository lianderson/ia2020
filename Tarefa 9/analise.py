import numpy as np
import matplotlib . pyplot as plt
import pandas as pd
import seaborn as sns
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

indexacao = 0
for acao in acoes.fetchall():
    valores = list()
    datas = list()
    conexao = pymysql.connect(host='viajuntos.com.br',user='admin_ia', passwd='admin_ia', db='admin_ia')
    cursor_banco = conexao.cursor()
    sql = "SELECT * FROM cotacao WHERE acao_id = " + str(acao[0]) + " order by data_importacao"
    cursor_banco.execute(sql)
    #conexao.close()
    for row in cursor_banco:
        valores.append(row[2])
        data = row[3]
        datas.append(data.strftime('%d/%m/%y'))

    data = {'valor':valores, 'data': datas}
    df = pd.DataFrame(data)

    print("-----------"+str(acao[1])+"-----------")
    print("soma:" + str(df['valor'].sum()))
    print("minimo:" + str(df['valor'].min()))
    print("maximo:" + str(df['valor'].max()))
    print("desvio padrao:" + str(df['valor'].std()))
    print("media:" + str(df['valor'].mean()))

    cursor_banco.execute('insert into equipe3_analise(equipe_id,acao_id,soma,quantidade,minimo,maximo,desvio_padra,media) values(%s, %s, %s, %s, %s, %s, %s, %s)', (str(3), str(acao[0]), str(df['valor'].sum()), str(df['valor'].count()), str(df['valor'].min()), str(df['valor'].max()), str(df['valor'].std()), str(df['valor'].mean())))
    conexao.commit()
    conexao.close()

# rodando = 0
# acao = -1

# while rodando == 1:
#     print("Digite o que quer mostrar:")
#     print("1-grafico1.")
#     print("2-grafico2.")
#     print("0-sair.")
#     acao = int(input(">"))

#     if acao == 0:
#         rodando = 0

#     if acao == 1:
#         print("1")

#     if acao == 2:
#         print("1")


