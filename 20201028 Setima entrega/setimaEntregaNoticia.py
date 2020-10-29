# ===============================================================================
# inteligencia artificial
# data: 2020 10 28
# script: desenvolver script parar pesquisar as noticias e contas a palavras
# autores: mauricio zaquia, lindice lopes, gustavo berté
# ===============================================================================

# ===============================================================================
# importando as bibliotecas
# ===============================================================================
import moduloSetimaEntrega as mqe
import schedule
import time
import pymysql
from datetime import datetime
import sys
from collections import Counter

# ===============================================================================
# criacao de variaveis
# ===============================================================================
arrayNoticias = []
arrayPalavrasNoticias = []

id_noticia = 0
palavra = ''
quantidade = 0

erro = ''

# ===============================================================================
# criando a funcao para disparar a busca
# ===============================================================================


def rodarBusca():
    global erro
    try:
        arrayNoticias = []
        # ===============================================================================
        # conexao com o banco
        # ===============================================================================
        conexao = pymysql.connect(
            host='viajuntos.com.br', user='admin_ia', password='admin_ia', db='admin_ia')
        # ===============================================================================
        # fazendo o select das noticias
        # ===============================================================================
        # configurando um cursor (quem percorre a tabela)
        cursor_banco = conexao.cursor()
        sql = "SELECT * FROM noticias WHERE equipe_id = 2"
        cursor_banco.execute(sql)
        for linhas in (cursor_banco.fetchall()):
            arrayNoticias.append(linhas)
        cursor_banco.close()
        # ===============================================================================
        # lendo os dados
        # ===============================================================================
        for a in (arrayNoticias):
            # print(a[2])

            arrayPalavrasNoticias = []
            noticia = a[2]

            chaves_unicas = set(noticia.split())
            frequencia = [(item, noticia.split().count(item))
                          for item in chaves_unicas]

            for i in frequencia:
                #print('Codigo Noticia: ' + a[0])
                #print('Palavra: ' + i[0])
                #print('Quantidade: ' + str(i[1]))

                id_noticia = a[0]
                palavra = i[0]
                quantidade = i[1]

                listaTeste = []
                listaTeste = [id_noticia, palavra, quantidade]
                arrayPalavrasNoticias.append(listaTeste)                

            print(arrayPalavrasNoticias)
            print('\n'+'\n'+'\n')

        if (conexao.open):
            conexao.close()
    except:
        erro = "Erro sem tratamento:"
        print(erro, sys.exc_info()[0])
        #mqe.gravaLog(caminho, erro + str(datetime.now()) + '\n')
    finally:
        if (conexao.open):
            conexao.close()
        print('Executado em: ' + str(datetime.now()))
        #mqe.gravaLog(caminho, 'Executado em: ' + str(datetime.now()) + '\n')


# ===============================================================================
# configuracao para rodar a busca
# ===============================================================================
schedule.every(.1).minutes.do(rodarBusca)
# schedule.every().hour.do(rodarBusca) #descomentar para pegar os valores de hora e hora

now = datetime.now()
hora = str(now.hour) + str(now.minute)

while (1):
    schedule.run_pending()
    time.sleep(1)
