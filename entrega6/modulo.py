import Aulas.ia2020.dados as dado # Nao esta no git, pois tem dados sensiveis
from googlesearch import search
from goose3 import Goose
import datetime #https://www.w3schools.com/python/python_datetime.aspentrega3entrega3
import urllib.request #pacote para trabalhar com mewb
import json #pacote para manipular JSON
import pymysql
import schedule
import time

modo = "dev"

def getUrlGoogle(buscar):
    urls = []
    print("Buscar google")
    print(buscar)
    try :
        for i in (search(buscar,tld="com.br",num=15,stop=3,pause=2)):
            urls.append(i)
    except ValueError:
        print("Não achou nada no Google")
    return urls

def getHtml(urls,gravarBD,id):
    noticias = []
    for i in urls:
        g=Goose()
        noticia=g.extract(url=i)
        hoje = datetime.datetime.now()

        if (noticia.cleaned_text == "" ):
            print("vazio")
            continue

        val = [id]
        url_noticias = executaDB("SELECT url_noticia FROM noticias WHERE acao_id =%s", val)
        #print(url_noticias)
        #print(i)
        if i in str(url_noticias):
            print("Ja ta no BD")
            continue


        noticias.append(noticia.cleaned_text)
        #print(i)
        #print(noticia.cleaned_text)

        if gravarBD is not None:
            val = [5, noticia.cleaned_text, i,id]
            query = executaDB("INSERT INTO noticias(equipe_id,noticia_descricao,url_noticia,acao_id) values(%s,%s,%s,%s)", val)

    return noticias

def setArquivo(arquivo,noticia):
    for i in noticia:
        hoje = datetime.datetime.now();
        hoje = hoje.strftime("%d/%m/%Y %H:%M:%S")
        f = open(arquivo, 'a')
        f.write(str(hoje)+"\n" + i+"\n")
        f.close()

#def fnYFinJSON(stock):
def getAcaoJson(acao):
      urlData = "https://query2.finance.yahoo.com/v7/finance/quote?symbols="+acao
      print(urlData)
      webUrl = urllib.request.urlopen(urlData)
      if (webUrl.getcode() == 200):
        data = webUrl.read()
      else:
          print ("problema ao ler os resultado " + str(webUrl.getcode()))
      yFinJSON = json.loads(data)
      return yFinJSON["quoteResponse"]["result"][0]

def getDados(id, acao, gravaBD):
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
    ticker = acao
    #for ticker in ticker:
    tickerData = getAcaoJson(ticker)  # le o site
    singleResult = {}
    for key in fields.keys():
        if key in tickerData:
            singleResult[fields[key]] = tickerData[key]
        else:
            singleResult[fields[key]] = "N/A"
    #results[ticker] = singleResult
    try:
        results[ticker] = singleResult
    except ValueError:
        print("Valor incorreto da variavel")

    precoAtual = results[ticker]['regularMarketPrice']

    if gravaBD is not None:
        #val = [id]
        #url_noticias = executaDB("SELECT url_noticia FROM noticias WHERE acao_id =%s", val)
        #print(url_noticias)
        #print(i)
        #if valor != valor_banco:
        #    print("Valor igual")
        #    continue
        val = [5, precoAtual, id]
        query = executaDB("INSERT INTO cotacao(equipe_id,preco,acao_id) values(%s,%s,%s)",val)

    # print(results[ticker]['Company']);
    # print(results[ticker]['regularMarketPrice']);

    #precoAtual = results[ticker]['regularMarketPrice']
    #precoAbertura = results[ticker]['regularMarketOpen']
    #precoBaixa = results[ticker]['regularMarketDayLow']
    #fechamento = results[ticker]['close']
    #precoAlta = results[ticker]['regularMarketDayHigh']
    #marketState = results[ticker]['marketState']
    #media3Meses = results[ticker]['averageDailyVolume3Month']
    #media50Dias = results[ticker]['fiftyDayAverage']
    #baixa52Semanas = results[ticker]['fiftyTwoWeekLow']
    #alta52Semanas = results[ticker]['fiftyTwoWeekHigh']
    #media200Dias = results[ticker]['twoHundredDayAverage']
    #MudancaMercadoRegular = results[ticker]['regularMarketChange']
    #PercentualRegularMudancaMercado = results[ticker]['regularMarketChangePercent']
    #nomeCompleto = results[ticker]['longName'];

def getConnect():
    global modo
    if modo == "prod":
        host = dado.hostDB
        user = dado.userDB
        passwd = dado.senhaDB
        db = dado.baseDB
        print("BD PROD")
    else:
        host = dado.hostDBdev
        user = dado.userDBdev
        passwd = dado.senhaDBdev
        db = dado.baseDBdev
        print("BD DEV")
    conexao = pymysql.connect(host=host, user=user, passwd=passwd, db=db)
    return conexao

def executaDB(sql,val):
    if "select" in sql.lower():
        print("eh select")
        lista = []
        try :
            conexao = getConnect().cursor()
            if val is not None:
                conexao.execute(sql,val)
            else:
                conexao.execute(sql)
        except pymysql.DatabaseError as err:
            print("Erro fatal no banco:")
            exit()

        for linha in conexao.fetchall():
            lista.append(linha)
        conexao.close()
        return lista
    else:
        print("nao eh select")
        resultado = altera(sql,val)
        return resultado

def getDadosAcao(equipe,gravarDB):
    query = executaDB(equipe,0)
    print(query)
    i = 0
    while i < len(query):
        acao = str(query[i][1])
        id = str(query[i][0])
        getDados(id,acao,gravarDB)
        i += 1

def loop(qtime,qfuncao):
    schedule.every(.1).minutes.do(getDadosAcao)
    while True:
        schedule.run_pending()
        time.sleep(1)

def select(sql):
    lista = []
    conexao = getConnect().cursor()
    conexao.execute(sql)
    for linha in conexao.fetchall():
        lista.append(linha)
    conexao.close()
    return lista

def altera(sql,val):
    try :
        conexao = getConnect()
        insert = conexao.cursor()
    except pymysql.DatabaseError as err:
        print("Erro fatal no banco:")

    if val is not None:
        print("altera tem val")
        resultado = insert.execute(sql,val)
    else:
        print("altera não tem val")
        resultado = insert.execute(sql)
    conexao.commit()
    insert.close()
    conexao.close()
    return resultado




####################################################


##exemplos, sem uso, funções acima atendem o estado atual
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









