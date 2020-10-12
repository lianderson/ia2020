import Aulas.ia2020.dados as dado # Nao esta no git, pois tem dados sensiveis
from googlesearch import search
from goose3 import Goose
import datetime #https://www.w3schools.com/python/python_datetime.aspentrega3entrega3
import urllib.request #pacote para trabalhar com mewb
import json #pacote para manipular JSON
import pymysql

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

        precoAtual = results[ticker]['regularMarketPrice']
        precoAbertura = results[ticker]['regularMarketOpen']
        precoBaixa = results[ticker]['regularMarketDayLow']
        fechamento = results[ticker]['close']
        precoAlta = results[ticker]['regularMarketDayHigh']
        marketState = results[ticker]['marketState']
        media3Meses = results[ticker]['averageDailyVolume3Month']
        media50Dias = results[ticker]['fiftyDayAverage']
        baixa52Semanas = results[ticker]['fiftyTwoWeekLow']
        alta52Semanas = results[ticker]['fiftyTwoWeekHigh']
        media200Dias = results[ticker]['twoHundredDayAverage']
        MudancaMercadoRegular = results[ticker]['regularMarketChange']
        PercentualRegularMudancaMercado = results[ticker]['regularMarketChangePercent']
        nomeCompleto = results[ticker]['longName'];

def getConnect():
    modo = "dev"
    if modo == "prod":
        host = dado.hostDB
        user = dado.userDB
        passwd = dado.senhaDB
        db = dado.baseDB
        print("if")
    else:
        host = dado.hostDBdev
        user = dado.userDBdev
        passwd = dado.senhaDBdev
        db = dado.baseDBdev
        print("else")
    conexao = pymysql.connect(host=host, user=user, passwd=passwd, db=db)
    return conexao

def Select(sql):
    lista = []
    conexao = getConnect().cursor()
    conexao.execute(sql)
    #return conexao.execute(sql) returna 3, You can't call fetchall() on the result of a cursor.execute(), in fact, according to MySQLdb documentation, cursor.execute() return the number of affected rows by the query executed. To retrieve data you have to access to cursor results directly:
    for linha in conexao.fetchall():
        lista.append(linha)
    conexao.close()
    return lista


def altera(sql):
    conexao = getConnect()
    insert = conexao.cursor()
    resultado = insert.execute(sql)
    conexao.commit()
    insert.close()
    conexao.close()
    return resultado

##exemplos, sem uso, fnções acima atendem o estado atual
def insertNovo():
    conexao = pymysql.connect(host='viajuntos.com.br', user='admin_ia', passwd='admin_ia', db='admin_ia')
    cursor_banco = conexao.cursor()

    sql = "INSERT INTO acao(nome,id_equipe)  values('%s',%s) " % ('Li', 1)
    cursor_banco.execute(sql)
    conexao.commit()

    cursor_banco.close()
    conexao.close()

def update():
    conexao = pymysql.connect(host='viajuntos.com.br', user='admin_ia', passwd='admin_ia', db='admin_ia')
    cursor_banco = conexao.cursor()

    sql = " update acao set nome ='%s',id_equipe ='%s' where id ='%s'  " % ('Li', 1, 9)
    cursor_banco.execute(sql)
    conexao.commit()
    cursor_banco.close()
    conexao.close()
def delete():
    import pymysql
    # abrir conexao
    # o que precisar para abrir a conexao com banco
    # 1 Host
    # 2 usuario do banco
    # 3 password
    # 4 db banco de dados
    conexao = pymysql.connect(host='viajuntos.com.br', user='admin_ia', passwd='admin_ia', db='admin_ia')
    cursor_banco = conexao.cursor()
    sql = " delete from acao  where  nome ='%s'  " % ('Ola')
    cursor_banco.execute(sql)
    conexao.commit()
    cursor_banco.close()
    conexao.close()









