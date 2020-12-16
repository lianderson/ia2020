import json
import requests
import time
import urllib
import pymysql
import moduloUtil

conexao = pymysql.connect(host='viajuntos.com.br', user='admin_ia', passwd='admin_ia', db='admin_ia')




TOKEN = '1485512743:AAEvttsw4i48QED8wMvTUGpFLojOiyfAelw'
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
            if(text=="1"):
                consulta = ["HGTX3.SA", "DTEX3.SA", "LOGN3.SA"]

                for j in range(0,len(consulta)):

                    with conexao.cursor() as cursor:
                        sql =  'select a.nome, c.preco from cotacao as c inner join acao AS a on c.acao_id = a.id where a.nome = "{}" group by a.nome order by c.data_importacao desc'.format(consulta[j])
                        cursor.execute(sql)

                        for i in cursor.fetchall():

                            text = "Ação: " +str(i[0]) +"----" + "Valor: " +str(i[1])
                            send_message(text, chat)
                            text = ""

                conexao.close()

            if(text=="2"):

                with conexao.cursor() as cursor:
                    sql =  'select a.nome, n.noticia_descricao from noticias as n inner join acao as a on n.acao_id = a.id where n.equipe_id = 4 group by n.acao_id order by n.data_importacao desc'
                    cursor.execute(sql)

                    for i in cursor.fetchall():

                        text = "Ação: " +str(i[0]) +"\n"
                        text+= "Noticia: " +str(i[1]) + "\n"
                        send_message(text, chat)
                        text = ""

                conexao.close()

            if(text=="oi"):
                text = "Como  voce esta?"
                text = "O que voce deseja? \n"
                text += "1 para ver ações atualizadas?\n "
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

def lerAcaoBot():

     consulta = ["HGTX3.SA", "DTEX3.SA", "LOGN3.SA"]

     for j in range(0,len(consulta)):

        with conexao.cursor() as cursor:
            cursor.execute('select a.nome, c.preco from cotacao as c inner join acao AS a on c.acao_id = a.id where a.nome = "{}" group by a.nome order by c.data_importacao desc'.format(consulta[j])) ### Select para buscar o id da ação
            buscar = cursor.fetchall()

            print(buscar)
        cursor.close() ### fecha cursor


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