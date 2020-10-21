import schedule
import time
import math
from googlesearch import search
from goose3 import Goose


import urllib.request
import json
import pymysql

conexao = pymysql.connect(host = '127.0.0.1', user = 'root', password = '', db = 'admin_ia', charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)


def pesquisa(consulta):



    for i in (search(consulta, tld="co.in", num=5, stop=4, pause=2)):
        url = i

        print(i)
        g = Goose()
        noticia = g.extract(url)
        return noticia.cleaned_text



def buscar_dados ():
    acoes = ["ITSA4.SA","MWET4.SA","LREN3.SA"]

    for i in range(0,3):
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



        preco_atual                          = results[empresa]['regularMarketPrice'];
        preco_abertura                       = results[empresa]['regularMarketOpen'];
        preco_baixa                          = results[empresa]['regularMarketDayLow'];
        close                                = results[empresa]['close'];
        preco_alta                           = results[empresa]['regularMarketDayHigh'];
        estado_de_mercado                    = results[empresa]['marketState'];
        media_de_volume_diario_nos_3_meses   = results[empresa]['averageDailyVolume3Month'];
        media_de_50_dias                     = results[empresa]['fiftyDayAverage'];
        baixa_de_52_semanas                  = results[empresa]['fiftyTwoWeekLow'];
        alta_de_52_semanas                   = results[empresa]['fiftyTwoWeekHigh'];
        media_de_200_dias                    = results[empresa]['twoHundredDayAverage'];
        variaçao_do_mercado                  = results[empresa]['regularMarketChange'];
        porcentagem_de_variaçao_do_mercado   = results[empresa]['regularMarketChangePercent'];
        nome_completo                        = results[empresa]['longName'];
        #print(Nomecompleto))

        with conexao.cursor() as cursor:
            sql = 'INSERT INTO cotacao (equipe_id,preco, acao_id ) values ("1","{}","{}");'.format(preco_atual, acoes[i])
            cursor.execute(sql)
            print(sql)
            conexao.commit()



schedule.every(10).seconds.do(buscar_dados)

while 1:
    schedule.run_pending()
    time.sleep(1)