import json
import requests
import time
import urllib
import pymysql
import re
import telegram
import modulo as mod
import datetime #https://www.w3schools.com/python/python_datetime.aspentrega3entrega3

conexao = pymysql.connect(host='viajuntos.com.br', user='admin_ia', passwd='admin_ia', db='admin_ia')

TOKEN = '1464243153:AAEvApGons_u7ScnndVzBwF4yeswJ4Ua9DY'
bot = telegram.Bot(token='1464243153:AAEvApGons_u7ScnndVzBwF4yeswJ4Ua9DY')

URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_news():
    dados = ""
    msg = ""
    cursor_banco = conexao.cursor()
    sql = "SELECT  id,twitter_word FROM  acoesnews where send_telegram IS null  order by id desc limit 10"
    cursor_banco.execute(sql)
    for dados in cursor_banco.fetchall():
         id  = dados[0]
         msg += "==================\n\n\n\n"+dados[1]
         sql = "UPDATE acoesnews SET  send_telegram = 'Y' WHERE id  = '"+str(id)+"'   "
         print(sql)
         util.command_sql(sql)
    cursor_banco=""
    return msg

def get_stock(url):
    print("stock")


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    print(js)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    if updates is None:
        ids = ['148673856']
        for i in ids:
            updates = {'ok': True, 'result': [{'update_id': 791210036, 'message': {'message_id': 1023, 'from': {'id': i, 'is_bot': False, 'first_name': 'Nome', 'language_code': 'en'}, 'chat': {'id': 148673856, 'first_name': 'Name', 'type': 'private'}, 'date': 1607119112, 'text': 'STATUS'}}]}

    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]

            if(text.upper()=="STATUS"):
                acoes = mod.busca_acoes(5, None)
                text = ""
                for acao in acoes:
                    val = [acao[0]]
                    ultimo_valor = mod.executaDB("SELECT preco,data_importacao FROM cotacao where acao_id = %s order by id desc limit 1",val)
                    val = ["%Y-%m-%d_%H:%i",acao[0]]
                    valor_robo = mod.executaDB("SELECT *,DATE_FORMAT (avisou, %s) AS datafo FROM admin_ia.equipe5_robo where acao_id = %s order by data_consulta desc limit 1",val)
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
                                            text = "COMPRA A ACAO "+str(acao[1])
                                            text += "\nValor " + str(valor)
                                            text += "\nCompra sujerida " + str(compra)
                                            val = [robo[0]]
                                            mod.executaDB("UPDATE `admin_ia`.`equipe5_robo` SET `avisou` = now() WHERE `id` = %s", val)
                                            send_message(text, chat)
                                    elif valor >= venda:
                                        if "vendido" not in robo[8]:
                                            text = "VENDA A ACAO "+str(acao[1])
                                            text += "\nValor " + str(valor)
                                            text += "\nVenda sujerida " + str(venda)
                                            val = [robo[0]]
                                            mod.executaDB("UPDATE `admin_ia`.`equipe5_robo` SET `avisou` = now() WHERE `id` = %s", val)
                                            send_message(text, chat)
            elif(text.upper()=="COTACAO"):
                acoes = mod.busca_acoes(5)
                text = "Qual ação você gostaria de ver o último valor? Veja o comando:\n"
                for i in acoes:
                    text += "COTACAO "+i[1]+"\n"
                send_message(text, chat)
                text = ""
            elif (text.upper() == "NOTICIA"):
                acoes = mod.busca_acoes(5)
                text = "Qual ação você gostaria de ver as noticias existentes? Veja o comando:\n"
                for i in acoes:
                    text += "NOTICIA " + i[1] + "\n"
                send_message(text, chat)
                text = ""
            elif (text.upper() == "COMPRA"):
                acoes = mod.busca_acoes(5)
                text = "Qual ação você gostaria de ver de informa compra? Veja o comando:\n"
                for i in acoes:
                    text += "COMPRA " + i[1] + "\n"
                send_message(text, chat)
                text = ""
            elif (text.upper() == "VENDA"):
                acoes = mod.busca_acoes(5)
                text = "Qual ação você gostaria de ver de informa compra? Veja o comando:\n"
                for i in acoes:
                    text += "VENDA " + i[1] + "\n"
                send_message(text, chat)
                text = ""
            elif (text.upper() == "AVISO"):
                acoes = mod.busca_acoes(5)
                text = "Qual ação você gostaria de ver de informa compra? Veja o comando:\n"
                for i in acoes:
                    text += "AVISO NAO " + i[1] + "\n"
                for i in acoes:
                    text += "AVISO SIM " + i[1] + "\n"
                send_message(text, chat)
                text = ""
            elif (text.upper() == "GRAFICO"):
                acoes = mod.busca_acoes(5)
                text = "Qual ação você gostaria de ver o gráfico de valores dos últimos 15 dias?\n"
                text += "Legenda:\n"
                text += "MIN: Valor minimo.\n"
                text += "AVG: Valor médio.\n"
                text += "MAX: Valor máximo.\n"
                text += "DIAS: Quantidades de dias.\n"
                text += "Comandos possiveis:\n"
                for i in acoes:
                    text += "======== "+i[1]+" ===========\n"
                    text += "GRAFICO MIN DIAS " + i[1] + "\n"
                    text += "GRAFICO AVG DIAS " + i[1] + "\n"
                    text += "GRAFICO MAX DIAS " + i[1] + "\n"

                send_message(text, chat)
                text = ""
            elif re.search('GRAFICO ', text, re.IGNORECASE):
                split_text = text.split(" ")
                calculo = split_text[1].upper()
                calculos_possiveis = ['MIN','AVG','MAX']
                if calculo not in calculos_possiveis:
                    text = "Opção inválida!\n"
                    text += "Comandos possiveis:\n"
                    send_message(text, chat)
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
                data = mod.data(arquivo="TRUE")
                fim = mod.data(data_hoje="TRUE")
                inicio = mod.data(data_antes=int(dia))
                nome = split_text[3]
                acoes = mod.busca_acoes(5,nome)
                for i in acoes:
                    mod.gerador_graficos(2, i[0], calculo, inicio, fim, img, data)
                    bot.send_photo(chat_id=chat, photo=open('../img/grafico_' + data + '.png', 'rb'))
                text = ""
            elif re.search('NOTICIA ', text, re.IGNORECASE):
                split_text = text.split(" ")
                nome = split_text[1].upper()
                acoes = mod.busca_acoes(5, nome)
                for i in acoes:
                    val = [i[0]]
                    noticias = mod.executaDB("SELECT url_noticia,substring(noticia_descricao,1,300) AS noticia_descricao FROM admin_ia.noticias where acao_id = %s order by data_importacao DESC limit 10", val)
                    for i in noticias:
                        text += i[1]+"...\n\nLeia mais...\n\n"
                        text += i[0]
                        send_message(text, chat)
                        text = ""

                text = ""
            elif re.search('COTACAO ', text, re.IGNORECASE):
                split_text = text.split(" ")
                nome = split_text[1].upper()
                acoes = mod.busca_acoes(5, nome)
                for i in acoes:
                    val = [i[0]]
                    ultimo_valor = mod.executaDB("SELECT preco,data_importacao FROM admin_ia.cotacao where acao_id = %s order by id desc limit 1", val)
                    valor_robo = mod.executaDB("SELECT * FROM admin_ia.equipe5_robo where acao_id = %s order by data_consulta desc limit 1",val)
                    for valor in ultimo_valor:
                        for robo in valor_robo:
                            text = "O ultimo valor da ação é R$ " + str(valor[0])+"\n\n"
                            text += "Os melhores valores para compras e vendas são:\nValor Compra: R$ " + str(robo[1])+"\nValor Venda: R$ "+str(robo[2])
                            text += "\nQuantidade " + str(robo[6])
                            send_message(text, chat)
                            text = "AJUDA"

                text = ""
            elif re.search('VENDA ', text, re.IGNORECASE):
                split_text = text.split(" ")
                nome = split_text[1].upper()
                acoes = mod.busca_acoes(5, nome)
                for i in acoes:
                    val = [i[0]]
                    valor_robo = mod.executaDB(
                        "SELECT * FROM admin_ia.equipe5_robo where acao_id = %s order by data_consulta desc limit 1",
                        val)
                    for i in valor_robo:
                        val = [i[0]]
                        print(val)
                        mod.executaDB("UPDATE equipe5_robo SET confirmado = 'vendido' WHERE id = %s", val)

            elif re.search('COMPRA ', text, re.IGNORECASE):
                split_text = text.split(" ")
                nome = split_text[1].upper()
                acoes = mod.busca_acoes(5, nome)
                for i in acoes:
                    val = [i[0]]
                    valor_robo = mod.executaDB(
                        "SELECT * FROM admin_ia.equipe5_robo where acao_id = %s order by data_consulta desc limit 1",
                        val)
                    for i in valor_robo:
                        val = [i[0]]
                        print(val)
                        mod.executaDB("UPDATE equipe5_robo SET confirmado = 'comprado' WHERE id = %s", val)

            elif re.search('AVISO ', text, re.IGNORECASE):
                split_text = text.split(" ")
                modo = split_text[1].upper()
                nome = split_text[2].upper()
                if "TODAS" in nome:
                    acoes = mod.busca_acoes(5)
                else:
                    acoes = mod.busca_acoes(5, nome)
                confirmado = "naoavisar"
                if "SIM" in modo:
                    confirmado = "avisar"
                for i in acoes:
                    val = [i[0]]
                    print(val)
                    valor_robo = mod.executaDB("SELECT * FROM admin_ia.equipe5_robo where acao_id = %s order by data_consulta desc limit 1",val)
                    for i in valor_robo:
                        val = [confirmado, i[0]]
                        print(val)
                        mod.executaDB("UPDATE equipe5_robo SET confirmado = %s WHERE id = %s", val)
            else:
                bot.send_photo(chat_id=chat, photo=open('../img/bot.jpg', 'rb'))
                text = "O que voce deseja?\n"
                text += "Escreva COTACAO para ver o valor de uma ação!\n"
                text += "Escreva NOTICIA para ver as noticias de uma ação!\n"
                text += "Escreva GRAFICO para ver as noticias de uma ação!\n"
                text += "Escreva AVISO para ver as opções de avisos!\n"
                send_message(text, chat)

        except Exception as e: print(e)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    print(text)
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def main():
    last_update_id = None
    echo_all(None)

    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)
        echo_all(None)

if __name__ == '__main__':

    main()