import json
import requests
import time
import urllib
import pymysql
import re
import modulo as mod
import telegram



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
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]

            if(text.upper()=="VALOR"):
                text = "Qual ação gostaria de ver o último valor? Veja o comando:\n"
                text += "COTACAO ITAU\n"
                text += "COTACAO AMBEV\n"
                text += "COTACAO PANVEL\n"

                bot.send_photo(chat_id=chat, photo=open('/home/cassolli/Aulas/IA/Projeto/entrega10/teste.png', 'rb'))
                send_message(text, chat)
                text = ""

            if (text.upper() == "NOTICIA"):
                text = "Qual ação você gostaria de ver as noticias existentes? Veja o comando:\n"
                text += "NOTICIAS ITAU\n"
                text += "NOTICIAS AMBEV\n"
                text += "NOTICIAS PANVEL\n"
                send_message(text, chat)
                text = ""

            if re.search('NOTICIAS', text, re.IGNORECASE):
                if re.search('ITAU', text, re.IGNORECASE):
                    val = [1]
                    noticias = mod.executaDB("SELECT url_noticia FROM admin_ia.noticias where acao_id = %s", val)
                    for i in noticias:
                        text = i[0]
                        send_message(text, chat)
                        text = "HELP"
                if re.search('PANVEL', text, re.IGNORECASE):
                    val = [2]
                    noticias = mod.executaDB("SELECT url_noticia FROM admin_ia.noticias where acao_id = %s", val)
                    for i in noticias:
                        text = i[0]
                        send_message(text, chat)
                        text = "HELP"
                if re.search('AMBEV', text, re.IGNORECASE):
                    val = [3]
                    noticias = mod.executaDB("SELECT url_noticia FROM admin_ia.noticias where acao_id = %s", val)
                    for i in noticias:
                        text = i[0]
                        send_message(text, chat)
                        text = "HELP"

            if re.search('COTACAO', text, re.IGNORECASE):
                if re.search('ITAU', text, re.IGNORECASE):
                    val = [1]
                    ultimo_valor = mod.executaDB("SELECT preco,data_importacao FROM admin_ia.cotacao where acao_id = %s order by id desc limit 1", val)
                    for i in ultimo_valor:
                        text = "O ultimo valor da ação é R$ " + str(i[0])
                        send_message(text, chat)
                        text = "HELP"

                if re.search('PANVEL', text, re.IGNORECASE):
                    val = [2]
                    ultimo_valor = mod.executaDB("SELECT preco,data_importacao FROM admin_ia.cotacao where acao_id = %s order by id desc limit 1", val)
                    for i in ultimo_valor:
                        text = "O ultimo valor da ação é R$ "+str(i[0])
                        send_message(text, chat)
                        text = "HELP"
                if re.search('AMBEV', text, re.IGNORECASE):
                    val = [3]
                    ultimo_valor = mod.executaDB("SELECT preco,data_importacao FROM admin_ia.cotacao where acao_id = %s order by id desc limit 1", val)
                    for i in ultimo_valor:
                        text = "O ultimo valor da ação é R$ " + str(i[0])
                        send_message(text, chat)
                        text = "HELP"

            if(text.upper() =="HELP"):
                text = "O que voce deseja?\n"
                text += "Escreva VALOR para ver o valor de uma ação!\n"
                text += "Escreva NOTICIA para ver as noticias de uma ação!\n"
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

    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':

    main()