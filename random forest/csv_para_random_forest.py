import pandas as pd
import pymysql
import csv

conexao = pymysql.connect(host='viajuntos.com.br', user='admin_ia', passwd='admin_ia', db='admin_ia')


with conexao.cursor() as cursor:
        sql = "SELECT valor_compra, valor_venda, valor_atual FROM equipe1_robo;"

        cursor.execute(sql)

        for acoes in cursor.fetchall():
            with open('dados_acoes.csv','a') as csv_file:

                csv_reader = csv.writer(csv_file, delimiter=',', lineterminator='\n')
                print(acoes)
                csv_reader.writerow([int(acoes[0]), int(acoes[1]), int(acoes[2])])
cursor.close()