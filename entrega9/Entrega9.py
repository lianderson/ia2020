import seaborn as sns
import pymysql
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

Preco = []
Data = []

identifica_acao = ''


identifica_acao = input("Digite o nome da acao: ")

conexao = pymysql.connect(host='viajuntos.com.br',user='admin_ia', password='admin_ia', db='admin_ia')

Preco = []
idd = []
cursor_banco = conexao.cursor()
sql = "SELECT c.preco, c.data_importacao, a.nome, c.acao_id FROM cotacao c  JOIN acao a ON a.id = c.acao_id WHERE equipe_id = 1 AND a.nome = '%s' ORDER BY data_importacao" % (identifica_acao)
cursor_banco.execute(sql)
for linhas in (cursor_banco.fetchall()):
    Preco.append(linhas[0])
    idd.append(linhas[3])
    data = str(linhas[1])
    Data.append(data)
cursor_banco.close()

def Informacoes_Analise(df):
    print('Soma:')
    print(df['valor_acao'].sum())

    print('Contagem:')
    print(df['valor_acao'].count())

    print('Minimo:')
    print(df['valor_acao'].min())

    print('Maximo:')
    print(df['valor_acao'].max())

    print('STD:')
    print(df['valor_acao'].std())#desvio padrao

    print('Mean:')
    print(df['valor_acao'].mean())#desvio padrao

    print(df.describe())

    soma = df['valor_acao'].sum()
    contagem = df['valor_acao'].count()
    minimo = df['valor_acao'].min()
    maximo = df['valor_acao'].max()
    desvio_padrao = df['valor_acao'].std()
    media = df['valor_acao'].mean()

    return (soma,contagem,minimo,maximo,desvio_padrao,media)

data = {'valor_acao': Preco, 'acao_id' : idd}
df = pd.DataFrame(data)
dados = Informacoes_Analise(df)

id_equipe = 1
acao_id = idd[0]
soma = dados[0]
contagem = dados[1]
minimo = dados[2]
maximo = dados[3]
desvio_padrao = dados[4]
media = dados[5]

cursor_banco = conexao.cursor()
sql = 'INSERT INTO equipe1_analise(equipe_id, acao_id, soma,quantidade,minimo,maximo,desvio_padra,media)  values(%s,%s,%s,%s,%s,%s,%s,%s) ' % (id_equipe, acao_id, soma, contagem, minimo, maximo, desvio_padrao, media)
print(sql)
cursor_banco.execute(sql)
conexao.commit()
cursor_banco.close()

conexao.close()