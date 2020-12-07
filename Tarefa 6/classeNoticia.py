import time
import pymysql
import urllib.request  # pacote para trabalhar com mewb
import json  # pacote para manipular JSON
from datetime import datetime
from decimal import Decimal
from goose3 import Goose
from googlesearch import search


def fnYFinJSON(symbol):
    urlData = "https://query2.finance.yahoo.com/v7/finance/quote?symbols=" + symbol
    # print(urlData)
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
    conexao = pymysql.connect(host='viajuntos.com.br',
                              user='admin_ia', passwd='admin_ia', db='admin_ia')
    cursor_banco = conexao.cursor()
    sql = "SELECT * FROM acao WHERE id_equipe = " + str(equipe)
    cursor_banco.execute(sql)
    conexao.close()
    return cursor_banco


def consulta(termo, qnt):
    return search(termo, num_results=qnt, lang="pt-br")


class Noticia:
    url = ""
    titulo = ""
    acao = 0
    texto = ""
    data = ""


def get_noticia_url(url, id_acao):
    g = Goose()
    noticia = g.extract(url=url)
    objnoticia = Noticia()
    objnoticia.url = url
    objnoticia.titulo = noticia.title
    objnoticia.data = str(noticia.publish_date)
    objnoticia.acao = id_acao
    objnoticia.texto = noticia.cleaned_text
    g.close()
    return objnoticia


def busca_noticias(acao, id_acao):
    tmpbusca = consulta(str(acao), 9)
    if(len(tmpbusca) > 0):
        for item in tmpbusca:
            #busca = tmpbusca[0]
            resultado = get_noticia_url(item, id_acao)

            if(len(resultado.texto) > 0):
                conexao = pymysql.connect(host='viajuntos.com.br', user='admin_ia', passwd='admin_ia', db='admin_ia')
                cursor_banco = conexao.cursor()
                sql = "SELECT * FROM noticias WHERE url_noticia = '%s'" % (resultado.url)
                cursor_banco.execute(sql)
                conexao.close()
                cont = 0
                for rows in (cursor_banco.fetchall()):
                    cont = cont + 1
                if(cont == 0):
                    #nao tem repetido, cadastrar
                    inserir_noticia(resultado)

def inserir_noticia(noticia):
    data = time.strftime('%Y-%m-%d %H:%M:%S')
    conexao = pymysql.connect(host='viajuntos.com.br', user='admin_ia', passwd='admin_ia',db='admin_ia')
    cursor_banco = conexao.cursor()
    cursor_banco.execute('insert into noticias(equipe_id,noticia_descricao,data_importacao,url_noticia,acao_id) values(%s, %s, %s, %s, %s)', (3, (noticia.titulo + " - " + noticia.texto), str(data), noticia.url, noticia.acao))
    conexao.commit()
    conexao.close()
    print(noticia.url + " - " + str(data) + '\n')
    print(noticia.texto + '\n')
    print("---------------------------------")

def busca_noticias_equipe3():
    cotacoes = busca_cotacoes(3)  # busca cotacoes da equipe com id 3
    for row in cotacoes:
        busca_noticias(str(row[1]), str(row[0]))


busca_noticias_equipe3()
