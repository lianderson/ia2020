import json
import requests
import time
import urllib
import pymysql

conexao = pymysql.connect(host='viajuntos.com.br', user='admin_ia', passwd='admin_ia', db='admin_ia')

TOKEN = '1351567877:AAEgEIO4uaUumBehL9QuOxSGKZmThAYppZc'
#1358807651:AAEhJaQ9r8J5sKzOjLgccrd6xvDId_HPqF0
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def busca_cotacoes(equipe):
    conexao2 = pymysql.connect(host='viajuntos.com.br', user='admin_ia', passwd='admin_ia', db='admin_ia')
    cursor_banco = conexao2.cursor()
    sql = "SELECT * FROM acao WHERE id_equipe = " + str(equipe)
    cursor_banco.execute(sql)
    conexao2.close()
    return cursor_banco

def busca_acao(acao):
    conexao2 = pymysql.connect(host='viajuntos.com.br', user='admin_ia', passwd='admin_ia', db='admin_ia')
    cursor_banco = conexao2.cursor()
    sql = "SELECT * FROM cotacao where acao_id = "+str(acao)+" ORDER BY data_importacao DESC LIMIT 1"
    cursor_banco.execute(sql)
    conexao2.close()
    return cursor_banco


def busca_acoes():
    retorno = "Confira os ultimos valores de nossas ações: \n"
    for x in busca_cotacoes(3).fetchall():
        for y in busca_acao(x[0]):
            retorno += str(x[1]) + " - R$ " + str(y[2]) + " - " + str(y[3]) + "\n"

    return retorno

def busca_noticias():
    retorno = "Confira as ultimas noticias sobre nossas ações: \n"
    conexao2 = pymysql.connect(host='viajuntos.com.br', user='admin_ia', passwd='admin_ia', db='admin_ia')
    cursor_banco = conexao2.cursor()
    sql = "SELECT * FROM noticias where equipe_id = 3 ORDER BY data_importacao DESC LIMIT 4"
    cursor_banco.execute(sql)
    conexao2.close()
    for x in cursor_banco.fetchall():
        retorno += str(x[4]) + " - " + str(x[3]) + "\n"
    return retorno

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
         #util.command_sql(sql)
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
            if(text=="1"):
                text = busca_acoes()
                send_message(text, chat)
                text = ""
            if(text=="2"):
                text = busca_noticias()
                send_message(text, chat)

            if(text=="oi"):
                text = "Como  voce esta?"
                text = "O que voce deseja? \n"
                text += "1 para ver ações ?\n "
                text += "2 para ver Noticias? \n"
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




