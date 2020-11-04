import csv
import math
import requests
import pymysql
import urllib.request
import json
from googlesearch import search
from goose3 import Goose

 #conexao_certa = pymysql.connect(host='viajuntos.com.br', user='admin_ia', password='admin_ia', db='admin_ia')
 #conexao_teste = pymysql.connect(host = '127.0.0.1', user = 'root', password = '', db = 'admin_ia')
def PesquisaNoticiasGoogle(resultado):
    url = []
    if not resultado is None:
        try:
            consulta = resultado
            for i in (search(consulta, tld="co.in", num=5, stop=10, pause=2, country="brazil")):
                url.append(i)
                for noticia in url:
                    g = Goose()
                    noticias = g.extract(url=noticia)
                    conteudo = noticias.cleaned_text.upper()
                    print(InserirNoticia(conteudo, noticia))
                g.close()

        except Exception as ex:
            print("Não foi possível salvar a notícia", ex)



def InserirNoticia(conteudo, noticia):
    conexao = pymysql.connect(host='viajuntos.com.br', user='admin_ia', password='admin_ia', db='admin_ia')
    while True:
        try:

            with conexao.cursor() as cursor:
                retornos = BuscarDadosYahoo()
                for retorno in retornos:
                    acao_id = FuncaoSelect(retorno["empresa"])
                    select = "SELECT * FROM noticias  WHERE  url_noticia ='"+str(noticia)+"' AND acao_id ="+str(acao_id)
                    print(select)
                    if select is None:
                        sql= 'INSERT INTO noticias(equipe_id,noticia_descricao,url_noticia,acao_id)values(1,"{}","{}","{}")'.format(conteudo, noticia, acao_id)
                        cursor.execute(sql)
                        print(sql)
                        conexao.commit()
                    else:
                        pass

        except ValueError:
            print("Não foi possível salvar a notícia")
        finally:
            cursor.close()

def contadorDePalavras():
    conexao = pymysql.connect(host='viajuntos.com.br', user='admin_ia', password='admin_ia', db='admin_ia')
    try:
        with conexao.cursor() as cursor:
                sql ='SELECT noticia_descricao FROM admin_ia.noticias WHERE equipe_id=1 and id=26'
                cursor.execute(sql)
                for i in cursor.fetchall():
                    for j in i:
                        chaves_unicas = set(j.split())
                        palavra = [(item, j.split().count(item)) for item in chaves_unicas]
                        for rows in palavra:
                            palavras = rows[0].replace('"','').replace('.','').replace(')','').replace('(','').replace('!','').replace('?','').replace(',','').replace('-','').upper()
                            qtdPalavras = rows[1]
                            print('Palavra: '+palavras)
                            print('quantidade: '+str(qtdPalavras))
                            sqlInser = "INSERT INTO equipe1_palavra(palavra,quantidade, noticia_id)values('{}',{},26)".format(str(palavras), qtdPalavras)
                            cursor.execute(sqlInser)
                            print(sqlInser)
                            conexao.commit()
    except ValueError:
            print("Não foi possível contar as palavras da notícia")
            pass
    finally:
            cursor.close()


def BuscarDadosYahoo():
    acoes = ["ITSA4.SA","MWET4.SA","LREN3.SA"]
    lista= []
    for i in range(0,3):
        def fnYFinJSON(stock):
          urlData = "https://query2.finance.yahoo.com/v7/finance/quote?symbols=" + acoes[i]
          print(urlData)
          webUrl = urllib.request.urlopen(urlData)
          if (webUrl.getcode() == 200):
            data = webUrl.read()
            print("Conectado a URL")
          else:
              print ("problema ao ler os resultado " + str(webUrl.getcode()))
          yFinJSON = json.loads(data)
          return yFinJSON["quoteResponse"]["result"][0]

        empresa = acoes[i]

        tickers = [empresa]
        fields = {'shortName':'Company',
                  'bookValue':'Book Value',
                  'currency':'Curr',
                  'fiftyTwoWeekLow':'52W L',
                  'fiftyTwoWeekHigh':'52W H',
                  'regularMarketPrice':'Price',
                  'regularMarketDayHigh':'High',
                  'regularMarketDayLow':'Low',
                  'priceToBook':'P/B',
                  'trailingPE':'LTM P/E',
                  'regularMarketDayLow':'DayLow',
                  'regularMarketPrice':'regularMarketPrice',
                  'regularMarketOpen': 'regularMarketOpen',
                  'ask':'close',
                  'regularMarketDayHigh' : 'regularMarketDayHigh',
                  'marketState':'marketState',
                  'averageDailyVolume3Month':'averageDailyVolume3Month',
                  'regularMarketDayLow':'regularMarketDayLow',
                  'fiftyDayAverage':'fiftyDayAverage',
                  'fiftyTwoWeekLow':'fiftyTwoWeekLow',
                  'twoHundredDayAverage':'twoHundredDayAverage',
                  'fiftyTwoWeekHigh':'fiftyTwoWeekHigh',
                  'regularMarketChange':'regularMarketChange',
                  'regularMarketChangePercent':'regularMarketChangePercent',
                  'longName':'longName'             }

        results={}
        for ticker in tickers:
           tickerData = fnYFinJSON(ticker) #le o site
           singleResult = {}
           for key in fields.keys():
             if key in tickerData:
               singleResult[fields[key]] = tickerData[key]
             else:
               singleResult[fields[key]] = "N/A"
           results[ticker] = singleResult

        var_x = {}
        var_x["empresa"]                              = empresa
        var_x["preco_atual"]                          = results[empresa]['regularMarketPrice'];
        var_x["preco_abertura"]                       = results[empresa]['regularMarketOpen'];
        var_x["preco_baixa"]                          = results[empresa]['regularMarketDayLow'];
        var_x["close"]                                = results[empresa]['close'];
        var_x["preco_alta"]                           = results[empresa]['regularMarketDayHigh'];
        var_x["estado_de_mercado"]                    = results[empresa]['marketState'];
        var_x["media_de_volume_diario_nos_3_meses"]   = results[empresa]['averageDailyVolume3Month'];
        var_x["media_de_50_dias"]                     = results[empresa]['fiftyDayAverage'];
        var_x["baixa_de_52_semanas"]                  = results[empresa]['fiftyTwoWeekLow'];
        var_x["alta_de_52_semanas"]                   = results[empresa]['fiftyTwoWeekHigh'];
        var_x["media_de_200_dias"]                    = results[empresa]['twoHundredDayAverage'];
        var_x["variaçao_do_mercado"]                  = results[empresa]['regularMarketChange'];
        var_x["porcentagem_de_variaçao_do_mercado"]   = results[empresa]['regularMarketChangePercent'];
        var_x["nome_completo"]                        = results[empresa]['longName'];


        lista.append(var_x)
    return lista


def FuncaoSelect(acoes):
    leitura = 0
    conexao = pymysql.connect(host='viajuntos.com.br', user='admin_ia', password='admin_ia', db='admin_ia')
    with conexao.cursor() as cursor:
        sql="Select id from acao where nome = '" +acoes+ "' "
        cursor.execute(sql)
        for i in cursor.fetchall():
            leitura = i[0]
        cursor.close()
    conexao.close()
    return leitura

def InserirCotacao():
    conexao = pymysql.connect(host='viajuntos.com.br', user='admin_ia', password='admin_ia', db='admin_ia')
    retornos = BuscarDadosYahoo()
    for retorno in retornos:
        with conexao.cursor() as cursor:
            sql= 'INSERT INTO cotacao(equipe_id,preco,acao_id)values(1,"{}","{}")'.format(retorno["preco_atual"],FuncaoSelect(retorno["empresa"]))
            cursor.execute(sql)
            conexao.commit()
            cursor.close()
    conexao.close()









