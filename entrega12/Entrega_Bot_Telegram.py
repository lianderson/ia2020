import json
import requests
import time
import urllib
import pymysql

conexao = pymysql.connect(host='viajuntos.com.br', user='admin_ia', passwd='admin_ia', db='admin_ia')

TOKEN = '1497521288:AAFEWNPfFRDVXqj8S3Gd-tptuuWBybrtEvQ'
URL = "https://api.telegram.org/bot{}/".format(TOKEN)



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



def pesquisarAcoes():
    with conexao.cursor() as cursor:
        sql = "SELECT * FROM acao WHERE id_equipe = 1"
        print(sql)
        cursor.execute(sql)
        for i in cursor.fetchall():
            text = "Ação: " + str(i[1]) + "\n"
            text += "Valor inicial: " + str(i[3]) + "\n"
            text += "Valor final: " + str(i[4]) + "\n"
            print(text)
        conexao.close()
    return text

def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]

            if (text=="1"):
                with conexao.cursor() as cursor:
                    sql = "SELECT * FROM acao WHERE id_equipe = 1"
                    print(sql)
                    cursor.execute(sql)
                    for i in cursor.fetchall():
                        text = "Ação: " + str(i[1]) + "\n"
                        text += "Valor inicial: " + str(i[3]) + "\n"
                        text += "Valor final: " + str(i[4]) + "\n"
                        print(text)
                        send_message(text, chat)
                cursor.close()


            if (text=="2"):
                with conexao.cursor() as cursor:
                    sql = "SELECT * FROM noticias WHERE equipe_id = 1"
                    print(sql)
                    cursor.execute(sql)
                    for i in cursor.fetchall():
                        print(i)
                        text = str(i[2])
                        print(text)
                        send_message(text, chat)
                cursor.close()



            if(text=="oi"):
                text = "Bem vindo! Selecione uma opção para consultar: \n"
                text += "1 - Para ver as ações da Equipe 1\n "
                text += "2 - Para ver as noticias relacionadas as ações da Equipe 1 \n"
                send_message(text, chat)
            else:
                text ="------------------------------------\n"
                text += "Selecione uma opção para consultar: \n"
                text += "1 - Para ver as ações da Equipe 1\n "
                text += "2 - Para ver as noticias relacionadas as ações da Equipe 1 \n"
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
