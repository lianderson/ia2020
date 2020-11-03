import schedule
import time
import pymysql
import urllib.request  # pacote para trabalhar com mewb
import json  # pacote para manipular JSON
from datetime import datetime
from decimal import Decimal

def fnYFinJSON(symbol):
    urlData = "https://query2.finance.yahoo.com/v7/finance/quote?symbols=" + symbol
    #print(urlData)
    webUrl = urllib.request.urlopen(urlData)
    if (webUrl.getcode() == 200):
        data = webUrl.read()
    else:
        print("problema ao ler os resultado " + str(webUrl.getcode()))
    yFinJSON = json.loads(data)
    try:
        return yFinJSON["quoteResponse"]["result"][0]
    except:
        return []


def buscaAcao(tickers):

    fields = {'shortName': 'Company', 'bookValue': 'Book Value', 'currency': 'Curr',
                      'fiftyTwoWeekLow': '52W L', 'fiftyTwoWeekHigh': '52W H',
                      'regularMarketPrice': 'Price',
                      'regularMarketDayHigh': 'High', 'regularMarketDayLow': 'Low',
                      'priceToBook': 'P/B', 'trailingPE': 'LTM P/E', 'regularMarketDayLow': 'DayLow',
                      'regularMarketPrice': 'regularMarketPrice', 'regularMarketOpen': 'regularMarketOpen',
                      'ask': 'close', 'regularMarketDayHigh': 'regularMarketDayHigh',
                      'marketState': 'marketState', 'averageDailyVolume3Month': 'averageDailyVolume3Month',
                      'regularMarketDayLow': 'regularMarketDayLow', 'fiftyDayAverage': 'fiftyDayAverage',
                      'fiftyTwoWeekLow': 'fiftyTwoWeekLow', 'twoHundredDayAverage': 'twoHundredDayAverage',
                      'fiftyTwoWeekHigh': 'fiftyTwoWeekHigh', 'regularMarketChange': 'regularMarketChange',
                      'regularMarketChangePercent': 'regularMarketChangePercent', 'longName': 'longName'}
    results = {}
    for ticker in tickers:
        tickerData = fnYFinJSON(ticker)  # le o site
        singleResult = {}
        for key in fields.keys():
            if key in tickerData:
                singleResult[fields[key]] = tickerData[key]
            else:
                singleResult[fields[key]] = "N/A"
        results[ticker] = singleResult
        return str(results[ticker]["close"])
        
    

def busca_cotacoes(equipe):
    conexao = pymysql.connect(host='viajuntos.com.br', user='admin_ia', passwd='admin_ia',db='admin_ia')
    cursor_banco = conexao.cursor()
    sql = "SELECT * FROM acao WHERE id_equipe = " + str(equipe)
    cursor_banco.execute(sql)
    conexao.close()
    return cursor_banco

def salva_cotacoes_atuais(sigla, id):
    now = datetime.now()
    acao = [sigla]
    preco = Decimal(buscaAcao(acao))
    data_formatada = now.strftime('%Y-%m-%d %H:%M:%S')
    conexao = pymysql.connect(host='viajuntos.com.br', user='admin_ia', passwd='admin_ia',db='admin_ia')
    cursor_banco = conexao.cursor()
    cursor_banco.execute('insert into cotacao(equipe_id,preco,data_importacao,acao_id) values(%s, %s, %s, %s)', (3, preco, data_formatada,id))
    conexao.commit()
    conexao.close()


def atualiza_cotacoes_equipe3():
    cotacoes = busca_cotacoes(3)#busca cotacoes da equipe com id 3
    for row in cotacoes:
        salva_cotacoes_atuais(str(row[1]), str(row[0]))

    #loop pelas cotacoes

#schedule.every(.1).minutes.do(rodar)


