import numpy as np
import matplotlib . pyplot as plt
import pandas as pd
import seaborn as sns
import pymysql
import time
from datetime import datetime
from scipy import stats

def buscarCotacoes(equipe):
    conexao = pymysql.connect(host='viajuntos.com.br',
                              user='admin_ia', passwd='admin_ia', db='admin_ia')
    cursor_banco = conexao.cursor()
    sql = "SELECT * FROM acao WHERE id_equipe = " + str(equipe)
    cursor_banco.execute(sql)
    conexao.close()
    return cursor_banco

acoes = buscarCotacoes(1)

def buscarValorAtual(acao_id):
    conexao = pymysql.connect(host='viajuntos.com.br',user='admin_ia', passwd='admin_ia', db='admin_ia')
    cursor_banco = conexao.cursor()
    sql = "SELECT * FROM cotacao WHERE preco > 0 AND acao_id = " + str(acao_id) + " order by data_importacao desc limit 1"
    cursor_banco.execute(sql)
    #conexao.close()
    for row in cursor_banco:
        return row[2]


def inserirValoresnoRobo(valor_atual, valor_compra, valor_venda, acao_id, equipe_id, decisao):
    conexao = pymysql.connect(host='viajuntos.com.br',user='admin_ia', passwd='admin_ia', db='admin_ia')
    cursor_banco = conexao.cursor()
    cursor_banco.execute('insert into equipe1_robo (valor_atual, valor_compra, valor_venda, acao_id, equipe_id, decisao) VALUES (%s, %s, %s, %s, %s, %s);', (str(valor_atual), str(valor_compra), str(valor_venda), str(acao_id), str(equipe_id), str(decisao)))
    conexao.commit()
    conexao.close()

#Logica implementada para o robo:
    #Pegamos o valor do desvio padrão de cada ação para saber se o valor dessa ação está variando para mais ou para menos em relação aos valores
    #dos períodos anteriores, ou seja, se o valor da minha cotação atual está menor que o valor da cotação - o desvio padrão eu compro, pois essa ação
    #não está variando tanto (pra mais ou pra menos)
    #Agora, se o valor da cotação for maior que o valor dela atual + desvio padrão eu vendo, pois ele está apresentando uma variação maior
    #Sendo assim, podemos dizer que nosso algorítmo é mais "conservador" em termos de compra e venda pois prefere adquirir ações que não estejam ocilando
    #muito em termos de valores (pra mais ou pra menos)



for acao in acoes.fetchall():
    valores = list()
    datas = list()
    valor_atual = buscarValorAtual(str(acao[0]))
    conexao = pymysql.connect(host='viajuntos.com.br',user='admin_ia', passwd='admin_ia', db='admin_ia')
    cursor_banco = conexao.cursor()
    sql = "SELECT * FROM equipe1_analise where acao_id = " + str(acao[0]) + " order by data_importacao limit 1"
    cursor_banco.execute(sql)
    for row in cursor_banco:
        desvio_p = float(row[8])
        media = (row[9])
        valor_compra =  float(valor_atual - (desvio_p / 4))
        valor_venda = float(valor_atual + (desvio_p / 4))
        if (valor_atual <= float(valor_compra)):
            print(str(acao[1]) + " Valor " + str(valor_atual) + " abaixo do desvio padrao " + str(media) + " Comprar")
            inserirValoresnoRobo(valor_atual, valor_compra, valor_venda, str(acao[0]), 1, "Comprar")
        elif (valor_atual > float(valor_venda)):
            print(str(acao[1]) + " Valor " + str(valor_atual) + " acima do desvio padrao " + str(media) + " Vender")
            inserirValoresnoRobo(valor_atual, valor_compra, valor_venda, str(acao[0]), 1, "Vender")
        else:
            print(str(acao[1]) + " Valor " + str(valor_atual) + " Manter")
            inserirValoresnoRobo(valor_atual, valor_compra, valor_venda, str(acao[0]), 1, "Manter")