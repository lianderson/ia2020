import requests
import re
import datetime #https://www.w3schools.com/python/python_datetime.asp
import mysql.connector #pip3.8 install install mysql-connector
import sys  ## Para usar argv

'''
Este script tem duas possibilidades de execucao:

-> Execucao manual com adicao de um argv
    python /home/cassolli/Aulas/proj1/Aulas/acoes-new.py motivo
        Onde sera solicitado para cada acao:
            -> Motivo do valor
            -> url da noticia, caso tenha
-> Execucao automatica via cron
    ->Agendado via cron: 
        -> 0 6-18 * * 1-5 /home/cassolli/Aulas/proj1/venv/bin/python /home/cassolli/Aulas/proj1/Aulas/acoes-new.py
by grupo 5 
    -> Diego Casslli
    -> Luis Fayh
'''

## Conexao com o banco
#ponteiro
mycursor = mydb.cursor()
#Query padrao
sql = "INSERT INTO cotacao (empresa, valorAcao, dataHora, motivo, url) VALUES (%s, %s, %s, %s, %s)"
arquivo= "/home/cassolli/Aulas/proj1/Aulas/bd.txt"
#inicializar variaveis
motivo = 'NULL'
url = 'NULL'
##Data
today = datetime.datetime.now();
today = today.strftime("%d/%m/%Y %H:%M:%S")

##Saber que acoes deve buscar, ja com suporte a URL personalizada.
chamada = [['ITUB3.SA','https://br.financas.yahoo.com/quote/ITUB3.SA/'],
           ['PNVL4.SA','https://br.financas.yahoo.com/quote/PNVL4.SA/'],
           ['ABEV3.SA', 'https://br.financas.yahoo.com/quote/ABEV3.SA/']
           ]

count = 0
while count < 3:
        #req = requests.get(chamada[count][1]) ## Se por ventura mudar e a url for diferente para cada acao
        req = requests.get("https://br.financas.yahoo.com/quote/"+chamada[count][0]+"/")
        linha = req.text.split(' ')
        for i in linha:
            '''
            Procurar ocorrencia de HTML que conten o valor da acao do dia, ignorando case
            '''
            if re.search('data-reactid=\"32\">\d', i, re.IGNORECASE):
                '''
                remover htmls desnecessarios para pegar somente o valor
                '''
                valor = i.replace('data-reactid="32">', '')
                valor = valor.replace('</span><span', '')
                '''
                suporte a execucao manual, sintaxe:
                python /home/cassolli/Aulas/proj1/Aulas/acoes-new.py motivo, 
                assim ele ira buscar as cotacoes e solicitara o motivo de tal cotacao e url caso tenha, valores podem ser informados em branco
                '''
                if len(sys.argv) > 1:
                    motivo = input("Qual o motivo do valor da acao "+chamada[count][0]+" ?")
                    url = input("Qual URL " + chamada[count][0] + " ?")
                '''
                Caso o valor esteje vazio
                '''
                if len(motivo) < 1:
                     motivo = 'NULL'
                if len(url) < 1:
                    url = 'NULL'
                '''
                preparando valores para inserir no banco
                '''
                val = (chamada[count][0], valor, str(today), motivo, url)
                '''insere no banco'''
                mycursor.execute(sql, val)
                mydb.commit()
                '''
                grava em arquivo os dados, com delimitador ;
                acao;valor;data/hora;motivo(default=NULL);url(default=NULL)
                alterar variavel arquivo, com caminho fisico
                '''
                f = open(arquivo, 'a')
                f.write(chamada[count][0] + ";" + valor + ";" + str(today)+";"+motivo+";"+url+";\n")
                f.close()

        count += 1

#f = open(arquivo, 'r')
#print(f.read())
with open(arquivo) as fp:
    for cnt,line in enumerate(fp):
        print("Linha {}: {}".format(cnt, line))
