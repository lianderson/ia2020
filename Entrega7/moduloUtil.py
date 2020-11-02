import tweepy ### bliblioteca para importar dados do twitter
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

conexao = pymysql.connect(
    host = '127.0.0.1',
    user = 'root',
    password = '2n84rc28y@',
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
            cursor.execute('select * from noticias WHERE equipe_id = 4') ### select para pegar os campos do bd

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
    except ValueError:
            print(">>>ATENÇÂO<<< Não foi possivel realizar a contagem das palavras!")
    finally:
        cursor.close() ### fecha cursor



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
            #print(nome_completo)

            with conexao.cursor() as cursor:
                cursor.execute('select id from acao where nome= "{}"'.format(acoes[i]))
                buscar = cursor.fetchall()
                sql = 'INSERT INTO cotacao (equipe_id,preco, acao_id ) values ("4","{}","{}");'.format(preco_atual,(buscar[0]['id']))
                cursor.execute(sql)
                print(">>>Cotação Cadastrada<<<")
                conexao.commit()
    except ValueError:
        print(">>>ATENCAO<<< Não foi possivel realizae a cotação das ações!")
    finally:
            cursor.close() ### fecha cursor





