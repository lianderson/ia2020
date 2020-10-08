# -*- coding: utf-8 -*-

# ===============================================================================
# importando as bibliotecas
# ===============================================================================
import urllib.request  # pacote para trabalhar com mewb
import json  # pacote para manipular JSON

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
              'longName': 'Nome Completo'}

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
