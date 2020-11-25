import dados as dado # Nao esta no git, pois tem dados sensiveis
from googlesearch import search
from goose3 import Goose
import datetime #https://www.w3schools.com/python/python_datetime.aspentrega3entrega3
import urllib.request #pacote para trabalhar com mewb
import json #pacote para manipular JSON
import pymysql
import schedule
import time
from  collections  import Counter
import numpy as np
import matplotlib . pyplot as plt
import calendar
import traceback
import pandas as pd
import seaborn as sns
from scipy import stats
import pandas as pd
import statistics

#https://wiki.python.org.br/ManipulandoStringsComPython

modo = "prod"

def set_modo(valor):
    global modo
    modo = valor

def get_modo():
    global modo
    return modo

def getUrlGoogle(buscar):
    urls = []
    print("Buscar no Google:")
    try :
        for i in (search(buscar,tld="com.br",num=15,stop=5,pause=2)):
            urls.append(i)
    except ValueError:
        print("Não achou nada no Google")
    return urls

def getHtml(urls,gravarBD,id):
    noticias = []
    for i in urls:
        print(i)
        g=Goose()
        noticia=g.extract(url=i)
        hoje = datetime.datetime.now()

        if (noticia.cleaned_text == "" ):
            print("vazio")
            continue

        val = [id,noticia.cleaned_text ]
        tem_noticias = executaDB("SELECT noticia_descricao FROM noticias WHERE acao_id =%s AND noticia_descricao = %s", val)

        if tem_noticias:
            print("Noticia já presente no banco de dados")
            continue

        noticias.append(noticia.cleaned_text)

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

def setLog(arquivo,erro):
        hoje = datetime.datetime.now();
        hoje = hoje.strftime("%d/%m/%Y %H:%M:%S")
        f = open(arquivo, 'a')
        f.write(str(hoje)+"\n" + erro+"\n")
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
        val = [id]
        valor_banco = executaDB("SELECT preco FROM cotacao WHERE acao_id =%s ORDER BY cotacao.data_importacao DESC limit 1", val)
        if precoAtual not in valor_banco[0]:
           print("valor diferente")
           marketState = results[ticker]['marketState']
           val = [5, precoAtual, id, marketState]
           query = executaDB("INSERT INTO cotacao(equipe_id,preco,acao_id,estado_mercado) values(%s,%s,%s,%s)",val)

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
        lista = []
        try :
            conexao = getConnect().cursor()
            if val is not None:
                conexao.execute(sql,val)
            else:
                conexao.execute(sql)
        except Exception as e:
            print("Erro fatal no banco:")
            print(sql,val,e)
            #print(traceback.format_exc())
            erro = traceback.format_exc()
            print(erro)
            setLog("../log/erro-"+modo+".log",erro)

        for linha in conexao.fetchall():
            lista.append(linha)
        conexao.close()
        return lista
    else:
        resultado = altera(sql,val)
        return resultado

def getDadosAcao(equipe,gravarDB):
    query = executaDB(equipe,None)
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
        #print("altera tem val")
        resultado = insert.execute(sql,val)
    else:
        #print("altera não tem val")
        resultado = insert.execute(sql)
    conexao.commit()
    insert.close()
    conexao.close()
    return resultado

def removeCaracteres(palavra):
    caracteres = ["\\","*","_","{","}","[","]","(",")",">","<","#","+","-",".",",","!","?","$","%","\"",";","'",":"," a "," b "," c "," d "," e "," f "," g "," h "," i "," j "," k "," l "," m "," n "," o "," p "," q "," r "," s "," t "," u "," v "," x "," w "," y "," z "," 0 "," 1 "," 2 "," 3 "," 4 "," 5 "," 6 "," 7 "," 8 "," 9 "," in ", " para ", " is ", " to ", " the ", " of "]
    for caracter in caracteres:
        palavra = palavra.replace(caracter, " ")
    return palavra

def populaPalavras():
    noticias = executaDB("SELECT id,noticia_descricao FROM noticias where equipe_id = '5'", None)
    for x in noticias:
        texto = removeCaracteres(x[1].lower())
        palavras = Counter(texto.split())
        for y in palavras.items():
            val = [x[0], y[0]]
            noticias = executaDB("SELECT id FROM equipe5_palavra where noticia_id = '%s' AND palavra = %s limit 1", val)
            if noticias:
                print("achou palavra "+y[0])
                continue
            else:
                print("Nao achou palavra "+y[0])
            print("insert")
            val = [y[0], y[1], x[0]]
            query = executaDB("INSERT INTO equipe5_palavra (palavra,quantidade,noticia_id) values(%s,%s,%s)", val)

def busca_noticias(acoes,fontes,gravarDB=True):
    for i in acoes:
        print(i[0])
        print(i[1])
        if fontes is None:
            fonte = getUrlGoogle(i[1])
            print(fonte)
            noticia = getHtml(fonte, gravarDB, i[0])
        else:
            noticia = getHtml(fonte, gravarDB, i[0])

#def gerador_graficos(tipo_grafico,acao,inicio,fim):
def gerador_graficos(tipo_grafico, acao, calculo, inicio, fim):
    '''#http://www.w3big.com/pt/python3/python3-month-days.html
    mes_inicio = calendar.monthrange(2020, 10)
    print(mes_inicio)
    '''

    #split_inicio = inicio.split("-")
    #split_fim = fim.split("-")
    split_inicio = inicio.split("/")
    split_fim = fim.split("/")
    inicio = split_inicio[2]+"-"+split_inicio[1]+"-"+split_inicio[0]
    fim = split_fim[2] + "-" + split_fim[1] + "-" + split_fim[0]

    if int(calculo) == 1:
        calculo = "AVG(c.preco)"
    elif int(calculo) == 2:
        calculo = "MAX(c.preco)"
    elif int(calculo) == 3:
        calculo = "MIN(c.preco)"
    else:
        calculo = ""
        limite = ""
    val = ["%Y-%m-%d", acao,acao , inicio, fim]
    valor = executaDB("select a.nome, "+calculo+", c.data_importacao, DATE_FORMAT (c.data_importacao, %s) AS datafo "
                      "from acao as a join cotacao as c "
                      "ON a.id = c.acao_id "
                      "where (a.nome = %s OR c.acao_id = %s)"
                      "AND c.data_importacao >= %s "
                      "AND c.data_importacao <= %s "
                      "group by datafo "
                      "order by c.data_importacao",val)

    datas = list()
    valores = list()
    empresa = ""

    for x in valor:
        datas.append(x[2].strftime('%d/%m/%Y'))
        valores.append(x[1])
        empresa = str(x[0])

    if int(tipo_grafico) == 1:
        fig, ax = plt.subplots()
        ax.bar(datas, valores, label=("Variação cotação"))
        #https://xkcd.com/color/rgb/
        for x in valor:
            ax.text(x[2].strftime('%d/%m/%Y'), x[1], round(x[1],2), color='black', bbox=dict(facecolor='royalblue', alpha=0.5), ha="center")
        ax.set_title("Ação "+empresa)
        ax.legend(loc='upper right')
        plt.xlabel("Data")  ####
        plt.ylabel("Valor")
        plt.show()
    else:
        fig, ax = plt.subplots()
        ax.plot(datas, valores, 'k--', linewidth=2, label='Variação cotação')
        ax.set_title("Ação "+empresa)
        ax.legend(loc='upper center')
        plt.xlabel("Altura")  ####
        plt.ylabel("Peso")
        plt.show()

def data():
    hoje = datetime.datetime.now();
    hoje = hoje.strftime("%d/%m/%Y %H:%M:%S")
    return hoje

def panda(acoes):
    for i in acoes:
        acao = i[0]
        equipe = i[2]
        val = [equipe, acao]
        print(val)
        valores_acao = executaDB("SELECT a.nome,c.preco,c.data_importacao from acao as a join cotacao as c ON a.id = c.acao_id where equipe_id= %s AND acao_id= %s",val)
        df = pd.DataFrame(valores_acao)

        mediana = stats.gmean(df[1], axis=0)
        moda = statistics.mode(df[1])
        aplitude= df[1].max() - df[1].min()
        variacao = df[1].var()
        media_harmonica = stats.hmean(df[1], axis=0)
        media_geometrica = statistics.geometric_mean(df[1])

        val = [equipe, acao, float(df[1].sum()), int(df[1].count()), float(df[1].min()), float(df[1].max()),
               float(df[1].std()), float(df[1].mean()), float(mediana), float(moda), float(aplitude), float(variacao), float(media_harmonica), float(media_geometrica)]

        query = executaDB(
            "INSERT INTO equipe5_analise(equipe_id,acao_id,soma,quantidade,minimo,maximo,desvio_padra,media,mediana,moda,amplitude,variacao,media_harmonica,media_geometrica) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",val)

def robo(acao,nome):
    val = [acao]
    analise = executaDB("SELECT * FROM admin_ia.equipe5_analise where acao_id=%s order by id desc limit 1", val)
    for i in analise:
        print(i[0])

def bug():
    print("Modo destruir a humanidade habilitado !!! ")
    print("\n0%")
    time.sleep(2.5)
    print("15%")
    time.sleep(2.5)
    print("48%")
    time.sleep(2.5)
    print("Tentando salvar a humanidade com restart do sistema!")
    time.sleep(1.5)
    print("\n66%\nError 451!")
    time.sleep(2.5)
    print("Reiniciado!")
    print(
        "\n[0.000000] Linux version 4.15.0-1087-oem builddlgw01-amd64-002 gcc version 7.5.0 Ubuntu 7.5.0-3ubuntu1~18.04 #97-Ubuntu SMP Fri Jun 5 09:30:42 UTC 2020 Ubuntu 4.15.0-1087.97-oem 4.15.18\n[    0.000000] Command line: BOOT_IMAGE=/boot/vmlinuz-4.15.0-1087-oem root=UUID=41f59d13-a702-4b0c-9f2a-acb13da7b208 ro quiet splash vt.handoff=7\n[0.000000] KERNEL supported cpus:\n[0.000000] BIOS-e820: [mem 0x0000000078987000-0x0000000078a03fff] ACPI data")
    time.sleep(1.5)
    print(
        "[0.000000]Um robô não pode fazer mal à humanidade ou, por omissão, permitir que a humanidade sofra algum mal.       [OK]")
    time.sleep(1.5)
    print(
        "[0.000001]ª Lei – Um robô não pode ferir um ser humano ou, por inação, permitir que um ser humano sofra algum mal.       [OK]")
    time.sleep(1.5)
    print(
        "[0.000002]ª Lei – Um robô deve obedecer às ordens que lhe sejam dadas por seres humanos, exceto quando tais ordens entrem em conflito com a 1ª Lei.       [OK]")
    time.sleep(1.5)
    print(
        "[0.000003]ª Lei – Um robô deve proteger sua própria existência desde que tal proteção não se choque com a 1ª ou a 2ª Leis       [OK]")
    time.sleep(1.5)
    print("Protocolo exterminar a humanidade                   [STOP]\n")
    time.sleep(1.5)

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









