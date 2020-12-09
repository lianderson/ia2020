import numpy as np
import matplotlib.pyplot as plt
import certifi
import schedule
import requests
import time
import math
from googlesearch import search
from goose3 import Goose
from collections import Counter
import urllib.request #pacote para trabalhar com mewb
import json #pacote para manipular JSON
import pymysql
import sys
from datetime import date
import pandas as pd
import seaborn as sns
from scipy import stats

conexao = pymysql.connect(
    host = 'viajuntos.com.br',
    user = 'admin_ia',
    password = 'admin_ia',
    db = 'admin_ia',
    charset = 'utf8mb4',
    cursorclass = pymysql.cursors.DictCursor
)



def calcula_raiz(valor): ### Funcao que calcula raiz quadrada
    raiz = math.sqrt(float(valor))
    return(raiz)

def contarPalavras(): ### Funcao que conta as palavras das noticias
    try:
        with conexao.cursor() as cursor: ### inicia cursor banco
            cursor.execute('select * from noticias where equipe_id = 4') ### select para pegar os campos do bd

            for row in cursor.fetchall(): ### linha da tabela do banco
                buscaId = (row['id']) ### pega o id da noticia da tabela noticias
                descricao = (Counter(row['noticia_descricao'].split())) ### Separa cada palavra e conta quantas vezes aparece naquela notica


                for busca in descricao: ### for para percorrer a lista do counter
                    palavras = busca[0:].replace('"','').replace('.','').replace(')','').replace('(','').replace('!','').replace('?','').replace(',','').replace('-','').replace(" ",'').replace('--', '') ### pega cada palavra dentro da lista, replace retira a pontuação e espaços
                    quantidade = str(descricao[busca]) ### pegando a quantidade da palavra

                    verifica = cursor.execute('select palavra from equipe4_palavra where noticia_id= "{}" and palavra= "{}"'.format((buscaId),palavras))

                    if verifica:
                        print(">>>PALAVRA JA CADASTRADA NO BANCO<<<")
                        continue

                    sql = 'INSERT INTO equipe4_palavra (palavra, quantidade, noticia_id) values ("{}", "{}", "{}");'.format(palavras, quantidade, buscaId)
                    cursor.execute(sql)
                    print(">>>PALAVRA SALVA NO BANCO<<<")
                    conexao.commit()
        cursor.close() ### fecha cursor
        conexao.close()
    except ValueError:
            print(">>>ATENÇÂO<<< Não foi possivel realizar a contagem das palavras!")
    finally:
        cursor.close() ### fecha



def pesquisa(): ### Funçao que pesquisa as noticias das acoes
    try:
        consulta = ["HGTX3.SA", "DTEX3.SA", "LOGN3.SA"]

        for j in range(0,len(consulta)):
            for i in  (search(consulta[j], tld="com.br", num=5, stop=5, pause=2)):
                print(i)
                url = i
                g = Goose()
                noticia = g.extract(url)
                noticia.cleaned_text

                if(noticia.cleaned_text == ""): ### verifica se o conteudo da noticia esta vazio ou é alguma imagem sem ter texto
                    print(">>>NOTICIA VAZIA SEM TEXTO<<<")
                    continue

                with conexao.cursor() as cursor:
                    cursor.execute('select id from acao where nome= "{}"'.format(consulta[j])) ### Select para buscar o id da ação
                    buscar = cursor.fetchall()

                    verifica = cursor.execute('select noticia_descricao from noticias where acao_id= "{}" and noticia_descricao= "{}"'.format((buscar[0]['id']),noticia.cleaned_text))

                    if verifica:
                        print(">>>NOTICIA JA CADASTRADA NO BANCO<<<")
                        continue


                    sql = 'INSERT INTO noticias (equipe_id,noticia_descricao,url_noticia,acao_id) values ("4","{}","{}","{}");'.format(noticia.cleaned_text, i,(buscar[0]['id']))
                    cursor.execute(sql)
                    print(">>>NOTICIAS Salva no banco<<<")
                    conexao.commit()
                    cursor.close() ### fecha cursor
                    conexao.close()

    except ValueError:
        print(">>>ATENCAO<<< Não foi possivel realizar a pesquisa de noticias!")
    finally:
                cursor.close() ### fecha cursor


def ler_acao (): ### Funçao que busca a cotaçao dos ativos no Yahoo
    try:
        acoes = ["HGTX3.SA","DTEX3.SA","LOGN3.SA"]

        for i in range(0,len(acoes)):
            def fnYFinJSON(stock):
              urlData = "https://query2.finance.yahoo.com/v7/finance/quote?symbols=" + acoes[i]
              print(urlData)
              webUrl = urllib.request.urlopen(urlData)
              if (webUrl.getcode() == 200):
                data = webUrl.read()
              else:
                  print ("problema ao ler os resultado " + str(webUrl.getcode()))
              yFinJSON = json.loads(data)
              return yFinJSON["quoteResponse"]["result"][0]



            empresa    = acoes[i]

            tickers = [empresa]
            fields = {'shortName':'Company', 'bookValue':'Book Value', 'currency':'Curr',
                  'fiftyTwoWeekLow':'52W L', 'fiftyTwoWeekHigh':'52W H',
                  'regularMarketPrice':'Price',
                  'regularMarketDayHigh':'High', 'regularMarketDayLow':'Low',
                  'priceToBook':'P/B', 'trailingPE':'LTM P/E'  , 'regularMarketDayLow':'DayLow',
                  'regularMarketPrice':'regularMarketPrice' ,'regularMarketOpen': 'regularMarketOpen',
                  'ask':'close','regularMarketDayHigh' : 'regularMarketDayHigh',
                  'marketState':'marketState','averageDailyVolume3Month':'averageDailyVolume3Month',
                  'regularMarketDayLow':'regularMarketDayLow','fiftyDayAverage':'fiftyDayAverage',
                  'fiftyTwoWeekLow':'fiftyTwoWeekLow','twoHundredDayAverage':'twoHundredDayAverage',
                  'fiftyTwoWeekHigh':'fiftyTwoWeekHigh','regularMarketChange':'regularMarketChange',
                  'regularMarketChangePercent':'regularMarketChangePercent','longName':'longName'             }
            results = {}
            for ticker in tickers:
              tickerData = fnYFinJSON(ticker) #le o site
              singleResult = {}
              for key in fields.keys():
                if key in tickerData:
                  singleResult[fields[key]] = tickerData[key]
                else:
                  singleResult[fields[key]] = "N/A"
              results[ticker] = singleResult

            # print(results);
            #print(results[empresa]['Company']);
            #print(results[empresa]['regularMarketPrice']);

            preco_atual                = results[empresa]['regularMarketPrice'];
            # preco_abertura             = results[empresa]['regularMarketOpen'];
            #preco_baixa                = results[empresa]['regularMarketDayLow'];
            # close                      = results[empresa]['close'];
            #preco_alta                 = results[empresa]['regularMarketDayHigh'];
            #estadomercado              = results[empresa]['marketState'];
            #volume_medio_diario_3meses = results[empresa]['averageDailyVolume3Month'];
            #media_50dias               = results[empresa]['fiftyDayAverage'];
            #media_2semanas_em_baixa    = results[empresa]['fiftyTwoWeekLow'];
            #media_2semanas_em_alta     = results[empresa]['fiftyTwoWeekHigh'];
            #media_200dias              = results[empresa]['twoHundredDayAverage'];
            #mudanca_mercado            = results[empresa]['regularMarketChange'];
            #mudanca_mercado_percent    = results[empresa]['regularMarketChangePercent'];
            nome_completo              = results[empresa]['longName'];
            estadoMercado = results[empresa]['marketState'];
            #print(nome_completo)

            with conexao.cursor() as cursor:
                cursor.execute('select id from acao where nome= "{}"'.format(acoes[i]))
                buscar = cursor.fetchall()

                sql = 'INSERT INTO cotacao (equipe_id,preco, acao_id, estado_mercado ) values ("4","{}","{}","{}");'.format(preco_atual,(buscar[0]['id']),estadoMercado)
                cursor.execute(sql)
                print(">>>Cotação Cadastrada<<<")
                conexao.commit()
                cursor.close()

    except ValueError:
        print(">>>ATENCAO<<< Não foi possivel realizae a cotação das ações!")
    finally:
            cursor.close() ### fecha cursor

def graficoBarCotacao(a):
    fig,ax = plt.subplots()
    with conexao.cursor() as cursor: ### inicia cursor banco
            cursor.execute('select * from acao as a inner join cotacao as c on a.id = c.acao_id where a.nome = "{}";'.format(a)) ### select para pegar os campos do bd

            vetorPreco = []
            vetorData = []

            for row in cursor.fetchall(): ### linha da tabela do banco
                buscaPreco = (row['preco']) ###
                buscaData = (row['data_importacao'])


                vetorPreco.append(buscaPreco)


                data = str(buscaData.strftime('%d/%m/%Y'))
                vetorData.append(data.replace(',','-'))


                print(vetorData)
                print(vetorPreco)
    cursor.close() ### fecha cursor
    plt.xlabel("DATA")
    plt.ylabel("VALOR")
    ax.set_title('COTAÇÃO X DATA')
    plt.bar(vetorData, vetorPreco)
    plt.show()

def decisaoAcao():

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

        valor_compra = media - (media *0.1)
        valor_venda = media + (media *0.1)

        if busca_Preco > valor_venda:
            decisao = "vender"

        elif busca_Preco < valor_compra:
            decisao = "comprar"

        else:
            decisao = "Sem operações no momento"

        with conexao.cursor() as cursor: #adicionando calculos esdtatisticos ao banco de dados
            sql = 'INSERT INTO equipe4_robo (valor_compra,valor_venda,acao_id,equipe_id,valor_atual,decisao,quantidade_compra,media) values ("{}","{}","{}","{}","{}","{}","{}","{}");'.format(valor_compra,valor_venda, cod_acao[j],"4", busca_Preco,decisao,"3",media)
            cursor.execute(sql)
            print(">>>Cadastrada no Banco <<<")
            conexao.commit()



            df = pd.DataFrame(data)


        cursor.close() ### fecha cursor




