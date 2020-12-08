import numpy as np
import matplotlib . pyplot as plt
import pandas as pd
import seaborn as sns
import pymysql
import time
from scipy import stats

def busca_cotacoes(equipe):
    conexao = pymysql.connect(host='viajuntos.com.br',
                              user='admin_ia', passwd='admin_ia', db='admin_ia')
    cursor_banco = conexao.cursor()
    sql = "SELECT * FROM acao WHERE id_equipe = " + str(equipe)
    cursor_banco.execute(sql)
    conexao.close()
    return cursor_banco

acoes = busca_cotacoes(3)

def get_valor_atual(acao_id):
    conexao = pymysql.connect(host='viajuntos.com.br',user='admin_ia', passwd='admin_ia', db='admin_ia')
    cursor_banco = conexao.cursor()
    sql = "SELECT * FROM cotacao WHERE preco > 0 AND acao_id = " + str(acao_id) + " order by data_importacao desc limit 1"
    cursor_banco.execute(sql)
    #conexao.close()
    for row in cursor_banco:
        return row[2]

"""

"""
def grava_robo(valor_compra, valor_venda, acao_id, equipe_id, data_consulta):
    return ""



for acao in acoes.fetchall():
    valores = list()
    datas = list()
    valor_atual = get_valor_atual(str(acao[0]))
    conexao = pymysql.connect(host='viajuntos.com.br',user='admin_ia', passwd='admin_ia', db='admin_ia')
    cursor_banco = conexao.cursor()
    sql = "SELECT * FROM equipe3_analise where acao_id = " + str(acao[0]) + " order by data_importacao limit 1"
    cursor_banco.execute(sql)
    for row in cursor_banco:
        desvio_p = float(row[8])
        media = float(row[9])
        valor_compra =  float(valor_atual - desvio_p)
        valor_venda = float(valor_atual + desvio_p)
        if (valor_atual < float(media)):
            print(str(acao[1]) + " Valor " + str(valor_atual) + " abaixo da media " + str(media) + " Compra")
        elif (valor_atual > float(media)):
            print(str(acao[1]) + " Valor " + str(valor_atual) + " acima da media " + str(media) + " Vende")
        else:                
            print(str(acao[1]) + " Valor " + str(valor_atual) + " mesmo da media " + str(media) + " Espera")

           



