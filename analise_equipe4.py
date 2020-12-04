import pymysql
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

conexao = pymysql.connect(
    host = '152.67.55.61',
    user = 'admin_ia',
    password = 'admin_ia',
    db = 'admin_ia',
    charset = 'utf8mb4',
    cursorclass = pymysql.cursors.DictCursor
)

cod_acao = ["28", "29", "30"]

for j in range(0,len(cod_acao)):#lenda as ações da lista e realizando um dataframa para cada ação. com o objetivo de dividir cada ação e pegar somente os valores respectivos

    with conexao.cursor() as cursor: ### inicia cursor banco
        cursor.execute('select preco, acao_id, data_importacao from cotacao where equipe_id= "4" and acao_id = {};'.format(cod_acao[j]))

        data = {'acao_id':[], 'preco':[],'data_importacao':[]}#criando dataframe do preco e da acao

        df = pd.DataFrame(data)

    for row in cursor.fetchall(): ### linha da tabela do banco
        busca_Preco = (row['preco']) ###
        busca_acao= (row['acao_id'])
        data_in = (row['data_importacao'])

        entrada = [busca_acao, busca_Preco,data_in]#adicionando informações no dataframe
        df.loc[len(df)] = entrada

    #execuntando calculos estatiscos e guardando em variaveis

    soma = df['preco'].sum()
    quantidade = df['preco'].count()#quantidade de itens
    minimo = df['preco'].min()#valor minimo
    media_harmonica = stats.hmean(df['preco'], axis = 0) #media harmonica
    maximo = df['preco'].max()#imprime a idade maior
    desvio_padra = df['preco'].std()#desvio padrao
    media = df['preco'].mean()#media
    mediana = df['preco'].median()#mediana
    moda = df['preco'].mode()# nao consegui fazer no grupo a moda. somente com todos os itens
    amplitude = df['preco'].min() - df['preco'].max()#amplitude de cada ação
    variacao = df['preco'].var()#variança = media dos quadrados
    media_geometrica = stats.gmean(df['preco'], axis = 0)

    with conexao.cursor() as cursor: #adicionando calculos esdtatisticos ao banco de dados
        sql = 'INSERT INTO equipe4_analise (equipe_id,acao_id,soma,quantidade,minimo,media_harmonica,maximo, desvio_padra,media,mediana,moda, amplitude,variacao, media_geometrica ) values ("4","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}");'.format(cod_acao[j],soma,quantidade,minimo,media_harmonica,maximo, desvio_padra,media,mediana,moda, amplitude,variacao, media_geometrica)
        cursor.execute(sql)
        print(">>>Cadastrada no Banco <<<")
        conexao.commit()


    #print(df)#imprimindo df completo
    #print(soma,quantidade,minimo,media_harmonica,maximo, desvio_padra,media,mediana,moda, amplitude,variacao, media_geometrica)

    cursor.close() ### fecha cursor
