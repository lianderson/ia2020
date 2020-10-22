# -*- coding: utf-8 -*-
# ===============================================================================
# importando as bibliotecas
# ===============================================================================
import urllib.request  # pacote para trabalhar com mewb
import json  # pacote para manipular JSON
from goose3 import Goose
from googlesearch import search
from datetime import datetime
import pymysql

# ===============================================================================
# criando a funcao para retornar json valores passando o codigo da acao por parametro
# ===============================================================================


def fnYFinJSON(stock):
    urlData = "https://query2.finance.yahoo.com/v7/finance/quote?symbols=" + stock
    # print(urlData)
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

    fields = {'shortName': 'Empresa',
              'bookValue': 'Válor Contábil',
              'currency': 'Moeda',
              'fiftyTwoWeekLow': '52W L',
              'fiftyTwoWeekHigh': '52W H',
              'regularMarketPrice': 'Preço Atual',
              'regularMarketDayHigh': 'Alta do Dia',
              'regularMarketDayLow': 'Baixa do Dia',
              'priceToBook': 'P/L Proporção',
              'trailingPE': 'Índice P/L',
              'regularMarketDayLow': 'DayLow',
              'regularMarketPrice': 'Preço Atual',
              'regularMarketOpen': 'Preço na Abertura',
              'ask': 'Preço de Venda',
              'regularMarketDayHigh': 'Alta do Dia',
              'marketState': 'Estado do Mercado',
              'averageDailyVolume3Month': 'Estimativa Volume',
              'regularMarketDayLow': 'Baixa do Dia',
              'fiftyDayAverage': 'Média da V52',
              'fiftyTwoWeekLow': 'V52 Baixa',
              'twoHundredDayAverage': 'Média da Variação de 200 Dias',
              'fiftyTwoWeekHigh': 'V52 Alta',
              'regularMarketChange': 'Diferença',
              'regularMarketChangePercent': 'Diferença Porcentagem',
              'longName': 'Nome Completo',
              'symbol': 'Simbolo'}

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
    # print(results[empresa]['Empresa']);
    #print(results[empresa]['Preço Atual']);

    #preco_atual                = results[empresa]['Preço Atual'];
    #preco_abertura             = results[empresa]['Preço na Abertura'];
    #preco_baixa                = results[empresa]['Baixa do Dia'];
    #preco_venda                      = results[empresa]['Preço de Venda'];
    #preco_alta                 = results[empresa]['Alta do Dia'];
    #estado_mercado                = results[empresa]['Estado do Mercado'];
    #estimativa_volume   = results[empresa]['Estimativa Volume'];
    #media_52            = results[empresa]['Média da V52'];
    #media_52B            = results[empresa]['V52 Baixa'];
    #media_52A           = results[empresa]['V52 Alta'];
    #media_200       = results[empresa]['Média da Variação de 200 Dias'];
    #diferenca        = results[empresa]['Diferença'];
    #diferenca_por100 = results[empresa]['Diferença Porcentagem'];
    #nome_completo                   = results[empresa]['Nome Completo'];
    # print(nome_completo)

    return results

# ===============================================================================
# criando a funcao para pesquisar no google search
# ===============================================================================


def retornaURL(consulta):
    lista = search(consulta, num_results=1, lang="pt-br")
    return lista

# ===============================================================================
# criando a funcao para separar URL
# ===============================================================================


def retornaInformacoesSite(site_url):
    g = Goose()
    noticia = g.extract(url=site_url)

    arrayNoticia = [noticia.title, noticia.cleaned_text, noticia.publish_date]

    return(arrayNoticia)


def noticiaDuplicada(pCursor, noticia):
    cont = 0

    #conexao2 = pymysql.connect(host='viajuntos.com.br', user='admin_ia', password='admin_ia', db='admin_ia')    
    #pCursor = conexao2.cursor()
    
    sql = "SELECT noticia_descricao FROM noticias WHERE equipe_id = 2 and noticia_descricao = '%s'" % (noticia)
    print(sql)
    pCursor.execute(sql)

    for linhas in (pCursor.fetchall()):
        # arrayAcoes.append(linhas)
        print(str(linhas))
        cont = cont + 1

    pCursor.close()

    return cont
