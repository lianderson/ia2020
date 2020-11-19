# -*- coding: utf-8 -*-
# ===============================================================================
# importando as bibliotecas
# ===============================================================================
import urllib.request  # pacote para trabalhar com mewb
import json  # pacote para manipular JSON
from goose3 import Goose
#======
from scipy import  stats
import pandas as pd
#from googlesearch import search
from datetime import datetime


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

    fields = {
        'shortName': 'Empresa',
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
        'symbol': 'Simbolo'
    }

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


#def retornaURL(consulta):
#    lista = search(consulta, num_results=1, lang="pt-br")
#    return lista


# ===============================================================================
# criando a funcao para separar URL
# ===============================================================================


def retornaInformacoesSite(site_url):
    g = Goose()
    noticia = g.extract(url=site_url)

    arrayNoticia = [noticia.title, noticia.cleaned_text, noticia.publish_date]

    return (arrayNoticia)


def retornaInfoMat(df):
    print(df)
    print('Soma:')
    print(df['0'].sum())
    print('Quantidade:')
    print(df['0'].count())
    print('Minimo:')
    print(df['0'].min())
    print('Maximo:')
    print(df['0'].max())
    print('Desvio Padrão:')
    print(df['0'].std())  # desvio padrao
    print('Média:')
    print(df['0'].mean())  # media
    print('Describe:')    
    print(df.describe())    
    print('Mediana:')    
    print(df['0'].median()) #mediana
    print('Moda:')    
    print(float(df['0'].mode())) #moda
    print('Amplitude:')    
    amplitude =df['0'].max() - df['0'].min()    
    print(amplitude) #amplitude
    print('Variancia:')    
    print(df['0'].var())#variacia
    print('Media Geometrica:')    
    media_geo  =  stats.gmean(df['0'],axis=0)
    print(media_geo) #edia Geometrica
    print('Media Harmonica:')    
    media_harm  =  stats.hmean(df['0'],axis=0)
    print(media_harm) #media harmonica

    soma = df['0'].sum()
    quantidade = df['0'].count()
    minimo = df['0'].min()
    maximo = df['0'].max()
    desvio_padrao = df['0'].std()
    media = df['0'].mean()
    mediana = df['0'].median()
    moda = float(df['0'].mode())
    amplitude = amplitude
    variancia = df['0'].var()
    media_geo = media_geo
    media_harm = media_harm

    return (soma,quantidade,minimo,maximo,desvio_padrao,media,mediana,moda,amplitude,variancia, media_geo, media_harm)