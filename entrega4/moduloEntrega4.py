
import urllib.request  # pacote para trabalhar com mewb
import json  # pacote para manipular JSON

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


def retornarDados(enterprise):

    empresa = enterprise

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
              'regularMarketChangePercent':'regularMarketChangePercent','longName':'longName'      }

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



    return results