import schedule
import time
import math
from googlesearch import search
from goose3 import Goose
# -*- coding: utf-8 -*-
import urllib.request #pacote para trabalhar com mewb
import json #pacote para manipular JSON
import pymysql
conexao = pymysql.connect(
    host = '127.0.0.1',
    user = 'root',
    password = '',
    db = 'admin_ia',
    charset = 'utf8mb4',
    cursorclass = pymysql.cursors.DictCursor
)


def calcula_raiz(valor):
    raiz = math.sqrt(float(valor))
    return(raiz)

def pesquisa(consulta):



    for i in (search(consulta, tld="co.in", num=5, stop=4, pause=2)):
        url = i

        print(i)
        g = Goose()
        noticia = g.extract(url)
        return noticia.cleaned_text



def ler_acao ():
    acoes = ["HGTX3.SA","DTEX3.SA","LOGN3.SA"]

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

       # print(results);
        #print(results[empresa]['Company']);
        #print(results[empresa]['regularMarketPrice']);

        preco_atual                = results[empresa]['regularMarketPrice'];
        preco_abertura             = results[empresa]['regularMarketOpen'];
        preco_baixa                = results[empresa]['regularMarketDayLow'];
        close                      = results[empresa]['close'];
        preco_alta                 = results[empresa]['regularMarketDayHigh'];
        estadomercado              = results[empresa]['marketState'];
        volume_medio_diario_3meses = results[empresa]['averageDailyVolume3Month'];
        media_50dias               = results[empresa]['fiftyDayAverage'];
        media_2semanas_em_baixa    = results[empresa]['fiftyTwoWeekLow'];
        media_2semanas_em_alta     = results[empresa]['fiftyTwoWeekHigh'];
        media_200dias              = results[empresa]['twoHundredDayAverage'];
        mudanca_mercado            = results[empresa]['regularMarketChange'];
        mudanca_mercado_percent    = results[empresa]['regularMarketChangePercent'];
        nome_completo              = results[empresa]['longName'];
        #print(nome_completo)

        with conexao.cursor() as cursor:
            sql = 'INSERT INTO cotacao2 (equipe_id,preco, acao_id ) values ("4","{}","{}");'.format(preco_atual, acoes[i])
            cursor.execute(sql)
            print(sql)
            conexao.commit()



schedule.every(10).seconds.do(ler_acao)

while 1:
    schedule.run_pending()
    time.sleep(1)


