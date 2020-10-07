from googlesearch import search
from goose3 import Goose
import datetime #https://www.w3schools.com/python/python_datetime.aspentrega3entrega3
import urllib.request #pacote para trabalhar com mewb
import json #pacote para manipular JSON

def getFontes(buscar):
    urls = []
    for i in (search(buscar,tld="com.br",num=15,stop=3,pause=2)):
        urls.append(i)
    print(urls)
    return urls

def getHtml(urls):
    noticias = []
    for i in urls:
        g=Goose()
        noticia=g.extract(url=i)
        hoje = datetime.datetime.now()
        if(noticia.publish_date != None):
            artigoData = noticia.publish_date.split('T')
            dataHoje = hoje.strftime("%Y-%m-%d")
            print(artigoData[0])
            print(dataHoje)
            if str(dataHoje) != str(artigoData[0]):
               print("\nNoticia Antiga : "+i +" Data "+ artigoData[0])
        noticias.append(noticia.cleaned_text)
    return noticias

def gravaArquivo(arquivo,noticia):
    for i in noticia:
        hoje = datetime.datetime.now();
        data = hoje.strftime("%d/%m/%Y")
        hoje = hoje.strftime("%d/%m/%Y %H:%M:%S")
        f = open(arquivo, 'a')
        f.write(str(hoje)+"\n" + i+"\n")
        f.close()

def fnYFinJSON(stock):
      urlData = "https://query2.finance.yahoo.com/v7/finance/quote?symbols="+stock
      print(urlData)
      webUrl = urllib.request.urlopen(urlData)
      if (webUrl.getcode() == 200):
        data = webUrl.read()
      else:
          print ("problema ao ler os resultado " + str(webUrl.getcode()))
      yFinJSON = json.loads(data)
      return yFinJSON["quoteResponse"]["result"][0]

def getDados(tickers):
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

        print(results[ticker]);
        # print(results[ticker]['Company']);
        # print(results[ticker]['regularMarketPrice']);

        preco_atual = results[ticker]['regularMarketPrice'];
        preco_abertura = results[ticker]['regularMarketOpen'];
        preco_baixa = results[ticker]['regularMarketDayLow'];
        close = results[ticker]['close'];
        preco_alta = results[ticker]['regularMarketDayHigh'];
        marketState = results[ticker]['marketState'];
        averageDailyVolume3Month = results[ticker]['averageDailyVolume3Month'];
        fiftyDayAverage = results[ticker]['fiftyDayAverage'];
        fiftyTwoWeekLow = results[ticker]['fiftyTwoWeekLow'];
        fiftyTwoWeekHigh = results[ticker]['fiftyTwoWeekHigh'];
        twoHundredDayAverage = results[ticker]['twoHundredDayAverage'];
        regularMarketChange = results[ticker]['regularMarketChange'];
        regularMarketChangePercent = results[ticker]['regularMarketChangePercent'];
        longName = results[ticker]['longName'];

