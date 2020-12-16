import dados as dado # Nao esta no git, pois tem dados sensiveis
from googlesearch import search
from goose3 import Goose
import datetime #https://www.w3schools.com/python/python_datetime.aspentrega3entrega3
from datetime import timedelta
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
import bot
import telegram
import re
bot2 = telegram.Bot(token='1464243153:AAEvApGons_u7ScnndVzBwF4yeswJ4Ua9DY')
#https://wiki.python.org.br/ManipulandoStringsComPython

modo = "prod"

'''
Para mudar como a aplicação irpa rodar, se em dev ou produção
'''
def set_modo(valor):
    global modo
    modo = valor

def get_modo():
    global modo
    return modo

'''
Buscar ações da equipe, se pasar o nome, retorna a ação especifica passada no nome.
'''

def busca_acoes(time,nome=None):
    if nome is not None:
        val = [time,nome]
        acoes = executaDB("SELECT * FROM acao where id_equipe = %s AND nome = %s", val)
    else:
        val = [time]
        acoes = executaDB("SELECT * FROM acao where id_equipe = %s", val)
    return acoes

'''
Buscar ações passadas no buscar no google
'''
def getUrlGoogle(buscar):
    urls = []
    print("Buscar no Google:")
    try :
        for i in (search(buscar,tld="com.br",num=15,stop=20,pause=2)):
            urls.append(i)
    except ValueError:
        print("Não achou nada no Google")
    return urls

'''
Buscar html dos sites que passar na lista urls
'''
def getHtml(urls,gravarBD,id):
    noticias = []
    for i in urls:
        print(i)
        g=Goose()
        noticia=g.extract(url=i)
        hoje = datetime.datetime.now()
        ##Se não conseguiu ler o html passa
        if (noticia.cleaned_text == "" ):
            print("vazio")
            continue
        #print(i)
        #print(noticia.cleaned_text[0:100])
        ##noticia.cleaned_text[0:100]+"%" -> forma um like com os 100 caracteres da noticia para bater se existe
        val = [id,noticia.cleaned_text[0:100]+"%"]
        tem_noticias = executaDB("SELECT noticia_descricao FROM noticias WHERE acao_id =%s AND noticia_descricao like %s", val)
        ##Se a noticia já existe não tem pq gravar de novo
        if tem_noticias:
            print("Noticia já presente no banco de dados")
            continue

        noticias.append(noticia.cleaned_text)

        if gravarBD is not None:
            val = [5, noticia.cleaned_text, i,id]
            query = executaDB("INSERT INTO noticias(equipe_id,noticia_descricao,url_noticia,acao_id) values(%s,%s,%s,%s)", val)

    return noticias

'''
Função para criar um arquivo em um local que for enviado no arquivo e o dados que for enviado na varival noticia
'''
def setArquivo(arquivo,noticia):
    for i in noticia:
        hoje = datetime.datetime.now();
        hoje = hoje.strftime("%d/%m/%Y %H:%M:%S")
        f = open(arquivo, 'a')
        f.write(str(hoje)+"\n" + i+"\n")
        f.close()
'''
Função para criar um arquivo de log de erros
'''

def setLog(arquivo,erro):
        hoje = datetime.datetime.now();
        hoje = hoje.strftime("%d/%m/%Y %H:%M:%S")
        f = open(arquivo, 'a')
        f.write(str(hoje)+"\n" + erro+"\n")
        f.close()

'''
Pega na API do yahoo, os dados da ação desejada
'''
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

'''
Filtra os dados da getAcaoJson desejado e grava no bd
'''
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

'''
Função para criar uma vez só a conexão com o BD
'''
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

'''
Função que valida se a execução é um select, se sim, faz o select e retonna uma lista com os dados, se for outro update,delete,insert...faz a iteração com o banco
'''

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

'''
Prefiro cron XD
'''

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

'''
Passe uma palavra ou lista para remover caracteres especiais
'''

def removeCaracteres(palavra):
    caracteres = ["\\","*","_","{","}","[","]","(",")",">","<","#","+","-",".",",","!","?","$","%","\"",";","'",":"," a "," b "," c "," d "," e "," f "," g "," h "," i "," j "," k "," l "," m "," n "," o "," p "," q "," r "," s "," t "," u "," v "," x "," w "," y "," z "," 0 "," 1 "," 2 "," 3 "," 4 "," 5 "," 6 "," 7 "," 8 "," 9 "," in ", " para ", " is ", " to ", " the ", " of "]
    for caracter in caracteres:
        palavra = palavra.replace(caracter, " ")
    return palavra

'''
Le noticias e popula as palavras e seus totais
'''
def populaPalavras():
    noticias = executaDB("SELECT id,noticia_descricao FROM noticias where equipe_id = '5'", None)
    for x in noticias:
        texto = removeCaracteres(x[1].lower())
        palavras = Counter(texto.split())
        for y in palavras.items():
            val = [x[0], y[0]]
            noticias = executaDB("SELECT id FROM equipe5_palavra where noticia_id = '%s' AND palavra = %s limit 1", val)
            ##Se a palavra já existe pra noticia especifica, não grava de novo
            if noticias:
                print("achou palavra "+y[0])
                continue
            else:
                print("Nao achou palavra "+y[0])
            print("insert")
            val = [y[0], y[1], x[0]]
            query = executaDB("INSERT INTO equipe5_palavra (palavra,quantidade,noticia_id) values(%s,%s,%s)", val)

'''
Função que faz a busca das noticias no google ou outro site se for passado no campo fontes

'''

def busca_noticias(acoes,fontes,gravarDB=True):
    for i in acoes:
        #print(i[0])
        #print(i[1])
        if fontes is None:
            fonte = getUrlGoogle(i[1])
            print(fonte)
            noticia = getHtml(fonte, gravarDB, i[0])
        else:
            noticia = getHtml(fonte, gravarDB, i[0])

'''
Gera graficos tipo linha ou 
'''
def gerador_graficos(tipo_grafico, acao, calculo, inicio, fim, img=None, img_complemento=None):
    '''#http://www.w3big.com/pt/python3/python3-month-days.html
    mes_inicio = calendar.monthrange(2020, 10)
    print(mes_inicio)
    '''

    ##inverter o padrão de data
    split_inicio = inicio.split("/")
    split_fim = fim.split("/")
    inicio = split_inicio[2]+"-"+split_inicio[1]+"-"+split_inicio[0]
    fim = split_fim[2] + "-" + split_fim[1] + "-" + split_fim[0]

    #Calculos possiveis, para se gerar o gráfico
    if int(calculo) == 1:
        calculo = "AVG(c.preco)"
    elif int(calculo) == 2:
        calculo = "MAX(c.preco)"
    elif int(calculo) == 3:
        calculo = "MIN(c.preco)"
    else:
        calculo = ""
        limite = ""
    val = ["%Y-%m-%d", acao,acao, inicio, fim]
    print(val)
    print(calculo)
    valor = executaDB("select a.nome, "+calculo+", c.data_importacao, DATE_FORMAT (c.data_importacao, %s) AS datafo "
                      "from acao as a join cotacao as c "
                      "ON a.id = c.acao_id "
                      "where (a.nome = %s OR c.acao_id = %s)"
                      #"AND c.data_importacao >= %s "
                      #"AND c.data_importacao <= %s "
                     "AND (c.data_importacao BETWEEN %s AND DATE_SUB(%s, INTERVAL -1 DAY))"
                      "group by datafo "
                      "order by c.data_importacao",val)
    #print(valor)
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
        if img is None:
            plt.show()
        else:
            plt.savefig("../img/grafico_"+img_complemento+".png")
            plt.close(fig)

    else:
        fig, ax = plt.subplots()
        ax.plot(datas, valores, 'k--', linewidth=2, label='Variação cotação')
        for x in valor:
            ax.text(x[2].strftime('%d/%m/%Y'), x[1], round(x[1],2), color='black', bbox=dict(facecolor='royalblue', alpha=0.5), ha="center")
        ax.set_title("Ação "+empresa)
        ax.legend(loc='upper center')
        plt.xlabel("Altura")  ####
        plt.ylabel("Peso")
        if img is None:
            plt.show()
        else:
            plt.savefig("../img/grafico_"+img_complemento+".png")
            plt.close(fig)
'''
Formatador de datas
'''

def data(arquivo=None,data_hoje=None,data_antes=None):
    hoje = datetime.datetime.now();
    if data_hoje is not None:
        hoje = hoje.strftime("%d/%m/%Y")
        return hoje
    elif arquivo is not None:
        hoje = hoje.strftime("%d_%m_%Y_%H_%M_%S")
        return hoje
    elif data_antes is not None:
        hoje = datetime.datetime.now() - timedelta(days=data_antes)
        hoje = hoje.strftime("%d/%m/%Y")
        return hoje
    else:
        hoje = hoje.strftime("%d/%m/%Y %H:%M:%S")
        return hoje
    return hoje


'''
Gera os dados da tabela analise, contendo mediana,moda,amplitude...dos ultimos 15 dias
'''

def analise(acoes,dias,exibir=None):
    for i in acoes:
        acao = i[0]
        equipe = i[2]
        inicio = data(data_antes=dias)
        #inicio = inicio.replace("/", "-")
        split_inicio = inicio.split("/")
        inicio = split_inicio[2] + "-" + split_inicio[1] + "-" + split_inicio[0]
        val = [equipe, acao, inicio+" 00:00:00"]
        valores_acao = executaDB("SELECT a.nome,c.preco,c.data_importacao from acao as a join cotacao as c ON a.id = c.acao_id where c.equipe_id= %s AND c.acao_id= %s AND c.data_importacao >= %s",val)
        df = pd.DataFrame(valores_acao)
        mediana = stats.gmean(df[1], axis=0)
        moda = statistics.mode(df[1])
        aplitude= df[1].max() - df[1].min()
        variacao = df[1].var()
        media_harmonica = stats.hmean(df[1], axis=0)
        media_geometrica = statistics.geometric_mean(df[1])
        if acao == 1:
            quantidade = 2
        elif acao == 2:
            quantidade = 1
        elif acao == 3:
            quantidade = 8
        val = [equipe, acao, float(df[1].sum()), int(df[1].count()), float(df[1].min()), float(df[1].max()),
               float(df[1].std()), float(df[1].mean()), float(mediana), float(moda), float(aplitude), float(variacao), float(media_harmonica), float(media_geometrica), int(dias), quantidade]
        if exibir is None:
            query = executaDB("INSERT INTO equipe5_analise(equipe_id,acao_id,soma,quantidade,minimo,maximo,desvio_padra,media,mediana,moda,amplitude,variacao,media_harmonica,media_geometrica,periodo_analise,quantidade_compra) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",val)
        else:
            return val

'''
Faz analise dos melhores valores de compra e venda das ações
Regra valor da media dos últimos 15 dias+%desvio
'''

def robo(acao,nome):
    val = [acao, 15 ]
    analise = executaDB("SELECT * FROM admin_ia.equipe5_analise where acao_id=%s and periodo_analise =%s order by id desc  limit 1", val)
    for i in analise:
        media = i[8]
        desvio = i[7]/10
        valor_compra = round(media-(media*desvio),2)
        valor_venda = round(media+(media*desvio),2)
        comprar = i[17]
        print(media)
        print(desvio)
        val = [valor_compra,valor_venda, acao,'5', comprar]
        executaDB("INSERT INTO equipe5_robo(valor_compra,valor_venda,acao_id,equipe_id,quantidade_compra) values(%s,%s,%s,%s,%s)",val)
'''
Menu para o bot.py, Quando for enciada palavras unicas ao bot caira neste menue
'''

def menuBot(text,chat):
    if (text.upper() == "STATUS"):
        print("status")
        acoes = busca_acoes(5, None)
        text = ""
        for acao in acoes:
            val = [acao[0]]
            ultimo_valor = executaDB(
                "SELECT preco,data_importacao FROM cotacao where acao_id = %s order by id desc limit 1", val)
            val = ["%Y-%m-%d_%H:%i", acao[0]]
            valor_robo = executaDB(
                "SELECT *,DATE_FORMAT (avisou, %s) AS datafo FROM admin_ia.equipe5_robo where acao_id = %s order by data_consulta desc limit 1",
                val)
            for valor in ultimo_valor:
                for robo in valor_robo:
                    valor = valor[0]
                    compra = robo[1]
                    venda = robo[2]
                    hoje = datetime.datetime.now();
                    hoje = hoje.strftime("%Y-%m-%d_%H:%M")
                    if "naoavisar" not in robo[8]:
                        if robo[9] not in hoje:
                            if valor <= compra:
                                if "comprado" not in robo[8]:
                                    text = "Aconselhada COMPRA da ACAO " + str(acao[1])
                                    text += "\nValor " + str(valor)
                                    text += "\nCompra sugerida " + str(compra)
                                    val = [robo[0]]
                                    executaDB(
                                        "UPDATE `admin_ia`.`equipe5_robo` SET `avisou` = now() WHERE `id` = %s", val)
                                    bot.send_message(text, chat)
                            elif valor >= venda:
                                if "vendido" not in robo[8]:
                                    text = "Aconselhada VENDA da ACAO " + str(acao[1])
                                    text += "\nValor " + str(valor)
                                    text += "\nVenda sugerida " + str(venda)
                                    val = [robo[0]]
                                    executaDB(
                                        "UPDATE `admin_ia`.`equipe5_robo` SET `avisou` = now() WHERE `id` = %s", val)
                                    bot.send_message(text, chat)
    elif (text.upper() == "GRAFICO"):
        acoes = busca_acoes(5)
        text = "Qual ação você gostaria de ver o gráfico de valores dos últimos 15 dias?\n"
        text += "Legenda:\n"
        text += "MIN: Valor minimo.\n"
        text += "AVG: Valor médio.\n"
        text += "MAX: Valor máximo.\n"
        text += "DIAS: Quantidades de dias.\n"
        text += "Comandos possiveis:\n"
        for i in acoes:
            text += "======== " + i[1] + " ===========\n"
            text += "GRAFICO MIN DIAS " + i[1] + "\n"
            text += "GRAFICO AVG DIAS " + i[1] + "\n"
            text += "GRAFICO MAX DIAS " + i[1] + "\n"

        bot.send_message(text, chat)
        text = ""
    elif (text.upper() == "COTACAO"):
        acoes = busca_acoes(5)
        text = "Qual ação você gostaria de ver o último valor? Veja o comando:\n"
        for i in acoes:
            text += "COTACAO " + i[1] + "\n"
        bot.send_message(text, chat)
        text = ""
    elif (text.upper() == "NOTICIA"):
        acoes = busca_acoes(5)
        text = "Qual ação você gostaria de ver as noticias existentes? Veja o comando:\n"
        for i in acoes:
            text += "NOTICIA " + i[1] + "\n"
        bot.send_message(text, chat)
        text = ""
    elif (text.upper() == "COMPRA"):
        acoes = busca_acoes(5)
        text = "Qual ação você gostaria de informa compra? Veja o comando:\n"
        for i in acoes:
            text += "COMPRA " + i[1] + "\n"
        bot.send_message(text, chat)
        text = ""
    elif (text.upper() == "VENDA"):
        acoes = busca_acoes(5)
        text = "Qual ação você gostaria de informa compra? Veja o comando:\n"
        for i in acoes:
            text += "VENDA " + i[1] + "\n"
        bot.send_message(text, chat)
        text = ""
    elif (text.upper() == "AVISO"):
        acoes = busca_acoes(5)
        text = "Qual ação você gostaria de informar venda ou compra/ativar aviso? Veja o comando:\n"
        for i in acoes:
            text += "AVISO NAO " + i[1] + "\n"
        for i in acoes:
            text += "AVISO SIM " + i[1] + "\n"
        bot.send_message(text, chat)
        text = ""
    else:
        bot2.send_photo(chat_id=chat, photo=open('../img/bot.jpg', 'rb'))
        text = "O que voce deseja?\n"
        text += "Escreva COTACAO para ver o valor de uma ação!\n"
        text += "Escreva NOTICIA para ver as noticias de uma ação!\n"
        text += "Escreva GRAFICO para ver as noticias de uma ação!\n"
        text += "Escreva AVISO para ver as opções de avisos!\n"
        bot.send_message(text, chat)

'''
Funções disponiveis nos menus do bot.py, Quando for enviada mais de uma palavra com espaço caira nessa função que fará a execução dos dados em si ao usuário
'''

def funcoesBot(text,chat):
    if re.search('GRAFICO ', text, re.IGNORECASE):
        split_text = text.split(" ")
        calculo = split_text[1].upper()
        calculos_possiveis = ['MIN', 'AVG', 'MAX']
        if calculo not in calculos_possiveis:
            text = "Opção inválida!\n"
            text += "Comandos possiveis:\n"
            bot.send_message(text, chat)
            text = "grafico"

        dia = re.match('[0-9]', split_text[2])

        if dia == None:
            dia = 7
        else:
            dia = split_text[2]

        if calculo == 'AVG':
            calculo = 1
        elif calculo == 'MAX':
            calculo = 2
        elif calculo == 'MIN':
            calculo = 3
        else:
            calculo = ""
            limite = ""

        img = 'TRUE'
        data_new = data(arquivo="TRUE")
        fim = data(data_hoje="TRUE")
        inicio = data(data_antes=int(dia))
        nome = split_text[3]
        acoes = busca_acoes(5, nome)
        for i in acoes:
            gerador_graficos(2, i[0], calculo, inicio, fim, img, data_new)
            bot2.send_photo(chat_id=chat, photo=open('../img/grafico_' + data_new + '.png', 'rb'))
        text = ""
    elif re.search('NOTICIA ', text, re.IGNORECASE):
        split_text = text.split(" ")
        nome = split_text[1].upper()
        acoes = busca_acoes(5, nome)
        for i in acoes:
            val = [i[0]]
            noticias = executaDB(
                "SELECT url_noticia,substring(noticia_descricao,1,300) AS noticia_descricao FROM admin_ia.noticias where acao_id = %s order by data_importacao DESC limit 10",
                val)
            for i in noticias:
                text += i[1] + "...\n\nLeia mais...\n\n"
                text += i[0]
                bot.send_message(text, chat)
                text = ""

        text = ""
    elif re.search('COTACAO ', text, re.IGNORECASE):
        split_text = text.split(" ")
        nome = split_text[1].upper()
        acoes = busca_acoes(5, nome)
        for i in acoes:
            val = [i[0]]
            ultimo_valor = executaDB(
                "SELECT preco,data_importacao FROM admin_ia.cotacao where acao_id = %s order by id desc limit 1", val)
            valor_robo = executaDB(
                "SELECT * FROM admin_ia.equipe5_robo where acao_id = %s order by data_consulta desc limit 1", val)
            for valor in ultimo_valor:
                for robo in valor_robo:
                    text = "O ultimo valor da ação é R$ " + str(valor[0]) + "\n\n"
                    text += "Os melhores valores para compras e vendas são:\nValor Compra: R$ " + str(
                        robo[1]) + "\nValor Venda: R$ " + str(robo[2])
                    text += "\nQuantidade " + str(robo[6])
                    bot.send_message(text, chat)
                    text = "AJUDA"

        text = ""
    elif re.search('VENDA ', text, re.IGNORECASE):
        print("VENDA")
        split_text = text.split(" ")
        nome = split_text[1].upper()
        acoes = busca_acoes(5, nome)
        for acao in acoes:
            val = [acao[0]]
            valor_robo = executaDB("SELECT * FROM admin_ia.equipe5_robo where acao_id = %s order by data_consulta desc limit 1", val)
            for i in valor_robo:
                val = [i[0]]
                print(val)
                executaDB("UPDATE equipe5_robo SET confirmado = 'vendido' WHERE id = %s", val)
                text = "Informada venda da açao "+acao[1] + " para informar compra use compra "+acao[1]
                bot.send_message(text, chat)
                text = ""

    elif re.search('COMPRA ', text, re.IGNORECASE):
        print("COMPRA")
        split_text = text.split(" ")
        nome = split_text[1].upper()
        acoes = busca_acoes(5, nome)
        for acao in acoes:
            val = [acao[0]]
            valor_robo = executaDB(
                "SELECT * FROM admin_ia.equipe5_robo where acao_id = %s order by data_consulta desc limit 1",
                val)
            for i in valor_robo:
                val = [i[0]]
                print(val)
                executaDB("UPDATE equipe5_robo SET confirmado = 'comprado' WHERE id = %s", val)
                text = "Informada compra da açao " + acao[1] + " para informar compra use venda " + acao[1]
                bot.send_message(text, chat)
                text = ""

    elif re.search('AVISO ', text, re.IGNORECASE):
        split_text = text.split(" ")
        modo = split_text[1].upper()
        nome = split_text[2].upper()
        if "TODAS" in nome:
            acoes = busca_acoes(5)
        else:
            acoes = busca_acoes(5, nome)
        confirmado = "naoavisar"
        text_confirmado = "Não alertar"
        if "SIM" in modo:
            confirmado = "avisar"
            text_confirmado = "Alertar"
        for acao in acoes:
            val = [acao[0]]
            print(val)
            valor_robo = executaDB(
                "SELECT * FROM admin_ia.equipe5_robo where acao_id = %s order by data_consulta desc limit 1", val)
            for i in valor_robo:
                val = [confirmado, i[0]]
                print(val)
                executaDB("UPDATE equipe5_robo SET confirmado = %s WHERE id = %s", val)
                text = acao[1] + " modo "+ text_confirmado
                bot.send_message(text, chat)
                text = ""

    else:
        bot2.send_photo(chat_id=chat, photo=open('../img/bot.jpg', 'rb'))
        text = "O que voce deseja?\n"
        text += "Escreva COTACAO para ver o valor de uma ação!\n"
        text += "Escreva NOTICIA para ver as noticias de uma ação!\n"
        text += "Escreva GRAFICO para ver as noticias de uma ação!\n"
        text += "Escreva AVISO para ver as opções de avisos!\n"
        bot.send_message(text, chat)

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









