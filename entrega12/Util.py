import pymysql
import urllib
import urllib.request
import json
from googlesearch import search
from goose3 import Goose
import pandas as pd
import requests
from scipy import stats


 #conexao_certa = pymysql.connect(host='viajuntos.com.br', user='admin_ia', password='admin_ia', db='admin_ia')
 #conexao_teste = pymysql.connect(host = '127.0.0.1', user = 'root', password = '', db = 'admin_ia')
def PesquisaNoticiasGoogle(resultado):
    conexao = pymysql.connect(host='viajuntos.com.br', user='admin_ia', password='admin_ia', db='admin_ia')
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
                    titulo   = noticias.title()
                    print(url)
                    #with conexao.cursor() as cursor:
                    #    sql = "SELECT * FROM noticias  WHERE  url_noticia ="+str(noticia)
                    #    print(sql)
                    #    cursor.execute(sql)
                    #    if cursor.fetchall():
                    #        print(True)
                    #        print(InserirNoticia(conteudo, noticia))
                    #        cursor.close()
                    #    else:
                    #        print(False)
                    #        pass
                    #        cursor.close()
                g.close()
        except Exception as ex:
            print("Não foi possível salvar a notícia", ex)
    conexao.close()

def ValidarNoticia():
    return


def InserirNoticia(conteudo, noticia):
    conexao = pymysql.connect(host='viajuntos.com.br', user='admin_ia', password='admin_ia', db='admin_ia')
    while True:
        try:

            with conexao.cursor() as cursor:
                retornos = BuscarDadosYahoo()
                for retorno in retornos:
                    acao_id = FuncaoSelect(retorno["empresa"])
                    sql= 'INSERT INTO noticias(equipe_id,noticia_descricao,url_noticia,acao_id)values(1,"{}","{}","{}")'.format(conteudo, noticia, acao_id)
                    cursor.execute(sql)
                    print(sql)
                    conexao.commit()
        except ValueError:
            print("Não foi possível salvar a notícia")
        finally:
            cursor.close()
            conexao.close()

def contadorDePalavras():

    conexao = pymysql.connect(host='viajuntos.com.br', user='admin_ia', password='admin_ia', db='admin_ia')
    acao_id = FuncaoSelect(retorno["empresa"])
    try:
        with conexao.cursor() as cursor:
                sql ='SELECT noticia_descricao FROM admin_ia.noticias WHERE equipe_id=1 and id={}'.format(acao_id)
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
                            sqlInser = "INSERT INTO equipe1_palavra(palavra,quantidade, noticia_id)values('{}',{},{})".format(str(palavras), qtdPalavras,acao_id)
                            cursor.execute(sqlInser)
                            print(sqlInser)
                            conexao.commit()
    except ValueError:
            print("Não foi possível contar as palavras da notícia")
            pass
    finally:
            cursor.close()
            conexao.close()


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
            sql= 'INSERT INTO cotacao(equipe_id,preco,acao_id)values(1,"{}",{})'.format(retorno["preco_atual"],FuncaoSelect(retorno["empresa"]))
            cursor.execute(sql)
            conexao.commit()
            cursor.close()
    conexao.close()



def graficoCotacoes(data, acao_id):
    #conexao = pymysql.connect(host='viajuntos.com.br', user='admin_ia', password='admin_ia', db='admin_ia')
    #with conexao.cursor() as cursor:
    #    sql='SELECT preco,data_importacao FROM cotacao where equipe_id = 1 and data_importacao like "'+str(data)+'%" and acao_id={}'.format(acao_id)
    #    cursor.execute(sql)
    #   #Acao = ['Data, Ação']
    #    #Data = []
    #    #plt.bar(Acao,Data)
    #    #plt.show()
    #    for i in cursor.fetchall():
    #        preco = i[0]
    #        data = i[1]
    #        Acao = ['Data, Ação']
    #        Data = [data, preco]
    #        plt.bar(Acao,Data)
    #    cursor.close()
    #conexao.close()
    #return plt.show()

    Preco = []
    Datas = []

    conexao = pymysql.connect(host='viajuntos.com.br', user='admin_ia', password='admin_ia', db='admin_ia')

    with conexao.cursor() as cursor:
        sql = "select * from cotacao where acao_id = '33' order by data_importacao"
        cursor.execute(sql)
        conexao.close()

    for linhas in (cursor.fetchall()):
        Preco.append(linhas[2])
        data = linhas[3]
        Datas.append(data.strftime('%d/%m'))
    cursor.close()


    #fig, ax = plt.subplots()
    #ax.bar(Datas, Preco, label='Aula Grafico')
    #plt.xlabel("Valor")
    #plt.ylabel("Data")
    #plt.show()

def analitycs():

    preco = list()
    acao_id = list()
    Data = list()

    #Identifica qual açao:

    identifica_acao = input(
        "Acoes:\n Digite 1 para ITSA4.SA\n Digite 2 para MWET4.SA\n Digite 3 para LREN3.SA\n Digite aqui:")
    if identifica_acao == '1':
        identifica_acao = 'ITSA4.SA'
    elif identifica_acao == '2':
        identifica_acao = 'MWET4.SA'
    elif identifica_acao == '3':
        identifica_acao = 'LREN3.SA'
    else:
        print("NUMERO ERRADO")

    #Pega os dados da acao, das tabelas acao e cotacao:

    conexao = pymysql.connect(host='viajuntos.com.br', user='admin_ia', password='admin_ia', db='admin_ia')
    with conexao.cursor() as cursor:
        sql = "SELECT c.preco, c.data_importacao, a.nome, c.acao_id FROM cotacao c" \
              " JOIN acao a ON a.id = c.acao_id " \
              "WHERE equipe_id = 1 AND a.nome = '%s' " \
              "ORDER BY data_importacao" % (identifica_acao)
        cursor.execute(sql)
        #Prenche as listas com os valores do cursor:

        for linhas in (cursor.fetchall()):
            preco.append(linhas[0])
            acao_id.append(linhas[3])
            data = str(linhas[1])
            Data.append(data)

        data = {'preco': preco}
        df = pd.DataFrame(data)

        quantidade = df['preco'].count()
        min = df['preco'].min()
        max = df['preco'].max()
        soma = df['preco'].sum()
        desvio = df['preco'].std()
        media = df['preco'].mean()
        acaoid = acao_id[0]
        print(acaoid)
        mediana = df['preco'].median()
        moda = (float(df['preco'].mode()))
        amplitude = df['preco'].max() - df['preco'].min()
        variacao = df['preco'].var()
        media_geome = stats.gmean(df['preco'], axis=0)
        media_harmoni = stats.hmean(df['preco'], axis=0)


        print(quantidade)
        print(min)
        print(max)
        print(soma)
        print(desvio)
        print(media)
        print(acaoid)
        print(mediana)
        print(moda)
        print(amplitude)
        print(variacao)
        print(media_geome)
        print(media_harmoni)
    #inseri no banco de dados os valores:

        sql = 'INSERT INTO equipe1_analise (equipe_id, acao_id,soma, quantidade, minimo, maximo, desvio_padra, media, mediana, moda, amplitude, variacao, media_harmonica, media_geometrica)values(1,{},{},{},{},{},{},{},{},{},{},{},{},{})'.format(acaoid, quantidade,float(soma),float(min), float(max), float(desvio), float(media), float(mediana), float(moda), float(amplitude), float(variacao), float(media_harmoni), float(media_geome))
        print(sql)
        cursor.execute(sql)
        conexao.commit()

        cursor.close()
    conexao.close()
