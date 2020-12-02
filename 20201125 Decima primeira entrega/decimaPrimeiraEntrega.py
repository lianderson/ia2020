import json
import requests
import time
import urllib
import pymysql
#import modulo.py

conexao = pymysql.connect(host='viajuntos.com.br',
                          user='admin_ia', passwd='admin_ia', db='admin_ia')


TOKEN = '1448255531:AAEs2-W5QaebpiozCMVHXK7ciREeupBpeSA'
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_news():
    dados = ""
    msg = ""
    cursor_banco = conexao.cursor()
    sql = "SELECT  id,twitter_word FROM  acoesnews where send_telegram IS null  order by id desc limit 10"
    cursor_banco.execute(sql)
    for dados in cursor_banco.fetchall():
        id = dados[0]
        msg += "==================\n\n\n\n"+dados[1]
        sql = "UPDATE acoesnews SET  send_telegram = 'Y' WHERE id  = '" + \
            str(id)+"'   "
        print(sql)
        util.command_sql(sql)
    cursor_banco = ""
    return msg


def retornaNoticias():
    conexao = pymysql.connect(host='viajuntos.com.br',
                              user='admin_ia', passwd='admin_ia', db='admin_ia')
    arrayNoticias = []
    cursor_banco = conexao.cursor()
    sql = "SELECT * FROM noticias WHERE equipe_id = 2"
    cursor_banco.execute(sql)
    for linhas in (cursor_banco.fetchall()):
        arrayNoticias.append(linhas)
    return arrayNoticias


def retornaAcoes():
    conexao = pymysql.connect(host='viajuntos.com.br',
                              user='admin_ia', passwd='admin_ia', db='admin_ia')
    arrayAcoes = []
    cursor_banco = conexao.cursor()
    sql = "SELECT * FROM acao WHERE id_equipe = 2"
    cursor_banco.execute(sql)
    for linhas in (cursor_banco.fetchall()):
        arrayAcoes.append(linhas)
    return arrayAcoes


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

            if(text == "1"):

                # retornar array
                arrayAcoes = retornaAcoes()

                for linhas in (arrayAcoes):
                    text = "Ação: " + linhas[1] + " Valor: R$" + str(linhas[4])
                    send_message(text, chat)
                    text = ""

            if(text == "2"):

                # retornar array
                arrayNoticias = retornaNoticias()

                for linhas in (arrayNoticias):
                    text = linhas[2]
                    send_message(text, chat)
                    text = ""

            if(text == "oi"):
                text = "Como  voce esta?"
                text = "O que voce deseja? \n"
                text += "1 para ver Ações ?\n "
                text += "2 para ver Noticias? \n"
                send_message(text, chat)

        except Exception as e:
            print(e)


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
