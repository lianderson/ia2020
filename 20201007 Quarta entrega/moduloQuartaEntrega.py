# -*- coding: utf-8 -*-

# ===============================================================================
# importando as bibliotecas
# ===============================================================================
import urllib.request  # pacote para trabalhar com mewb
import json  # pacote para manipular JSON

# ===============================================================================
# criando a funcao para retornar json valores passando o codigo da acao por parametro
# ===============================================================================
def fnYFinJSON(stock):
    urlData = "https://query2.finance.yahoo.com/v7/finance/quote?symbols=" + stock
    #print(urlData)
    webUrl = urllib.request.urlopen(urlData)
    if (webUrl.getcode() == 200):
        data = webUrl.read()
    else:
        print("problema ao ler os resultado " + str(webUrl.getcode()))
    yFinJSON = json.loads(data)
    return yFinJSON["quoteResponse"]["result"][0]


# ===============================================================================
# criando a funcao para separar os campos
# ===============================================================================
def retornaCamposFormatados(pEmpresa):

    empresa = pEmpresa

    tickers = [empresa]

    fields = {'shortName': 'Company', 
            'bookValue': 'Book Value',
            'currency': 'Curr',
            'fiftyTwoWeekLow': '52W L', 
            'fiftyTwoWeekHigh': '52W H',
            'regularMarketPrice': 'Price',
            'regularMarketDayHigh': 'High', 
            'regularMarketDayLow': 'Low',
            'priceToBook': 'P/B', 
            'trailingPE': 'LTM P/E', 
            'regularMarketDayLow': 'DayLow',
            'regularMarketPrice': 'regularMarketPrice', 
            'regularMarketOpen': 'regularMarketOpen',
            'ask': 'close', 
            'regularMarketDayHigh': 'regularMarketDayHigh',
            'marketState': 'marketState', 
            'averageDailyVolume3Month': 'averageDailyVolume3Month',
            'regularMarketDayLow': 'regularMarketDayLow', 
            'fiftyDayAverage': 'fiftyDayAverage',
            'fiftyTwoWeekLow': 'fiftyTwoWeekLow', 
            'twoHundredDayAverage': 'twoHundredDayAverage',
            'fiftyTwoWeekHigh': 'fiftyTwoWeekHigh', 
            'regularMarketChange': 'regularMarketChange',
            'regularMarketChangePercent': 'regularMarketChangePercent', 
            'longName': 'longName'}

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

    # print(results)
    # print(results[empresa]['Company'])
    # print(results[empresa]['regularMarketPrice'])

    #preco_atual = results[empresa]['regularMarketPrice']
    #preco_abertura = results[empresa]['regularMarketOpen']
    #preco_baixa = results[empresa]['regularMarketDayLow']
    #close = results[empresa]['close']
    #preco_alta = results[empresa]['regularMarketDayHigh']
    #marketState = results[empresa]['marketState']
    #averageDailyVolume3Month = results[empresa]['averageDailyVolume3Month']
    #fiftyDayAverage = results[empresa]['fiftyDayAverage']
    #fiftyTwoWeekLow = results[empresa]['fiftyTwoWeekLow']
    #fiftyTwoWeekHigh = results[empresa]['fiftyTwoWeekHigh']
    #twoHundredDayAverage = results[empresa]['twoHundredDayAverage']
    #regularMarketChange = results[empresa]['regularMarketChange']
    #regularMarketChangePercent = results[empresa]['regularMarketChangePercent']    
    #longName = results[empresa]['longName']    
    #print(longName)

    return results
