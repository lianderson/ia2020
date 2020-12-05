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

            if re.search(' ', text, re.IGNORECASE):
                mod.funcoesBot(text,chat)
            else:
                mod.menuBot(text, chat)
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