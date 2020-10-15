# ===============================================================================
# inteligencia artificial
# data: 2020 10 07
# script: desenvolver script parar pesquisar as informacoes das empresas utiolizando api do yahoo
# autores: mauricio zaquia, lindice lopes, gustavo berté
# ===============================================================================

# ===============================================================================
# importando as bibliotecas
# ===============================================================================
import moduloQuintaEntrega as mqe
import schedule
import time
import pymysql
from datetime import datetime

# ===============================================================================
# conexao com o banco
# ===============================================================================
conexao = pymysql.connect(
    host='viajuntos.com.br',
    user='admin_ia',
    password='admin_ia',
    db='admin_ia')

# ===============================================================================
# criacao de variaveis
# ===============================================================================
informacoes = ''
acoes = []

# ===============================================================================
# fazendo o select das acoes
# ===============================================================================
#configurando um cursor (quem percorre a tabela)
cursor_banco = conexao.cursor()

#fazendo uma consulta
sql = "SELECT * FROM acao WHERE id_equipe = 2"
cursor_banco.execute(sql)

for linhas in (cursor_banco.fetchall()):    
    acoes.append(linhas)

cursor_banco.close()

# ===============================================================================
# criando a funcao para disparar
# ===============================================================================
def rodarBusca():
    # ===============================================================================
    # lendo os dados
    # ===============================================================================
    for a in (acoes):        
        arrayInformacoes = mqe.retornaCamposFormatados(a[1])
        #print(arrayInformacoes[a[1]]['Simbolo'])
        #print(arrayInformacoes[a[1]]['Preço Atual'])

        # ===============================================================================
        # inserindo a cotacao na tabela cotacao no banco
        # ===============================================================================
        cursor_banco  = conexao.cursor()

        sql  = "INSERT INTO cotacao(equipe_id,preco,acao_id)  values(%s,%s,%s) " % (a[2],arrayInformacoes[a[1]]['Preço Atual'],a[0])
        print(sql)

        cursor_banco.execute(sql)
        conexao.commit()

        cursor_banco.close()
        #conexao.close()

schedule.every(.1).minutes.do(rodarBusca)

now = datetime.now()
hora = str(now.hour) + str(now.minute)

while ((hora > '1000') and (hora < '1800')):
    schedule.run_pending()
    time.sleep(1)
    now = datetime.now()
    hora = str(now.hour) + str(now.minute)
