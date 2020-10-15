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

acao = ''
data = ''
titulo = ''
noticia = ''

# ===============================================================================
# fazendo o select das acoes
# ===============================================================================
# configurando um cursor (quem percorre a tabela)
cursor_banco = conexao.cursor()

# fazendo uma consulta
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
        # retorna lista de urls
        listaUrls = mqe.retornaURL(a[1])

        for i in (listaUrls):
            # retorna noticias de acordo com cada url
            arrayNoticia = mqe.retornaInformacoesSite(i)

            #acao = a[1]
            noticia = arrayNoticia[1]
            #print(acao)
            #print(noticia)

            # ===============================================================================
            # inserindo a noticia na tabela cotacao no banco
            # ===============================================================================
            cursor_banco = conexao.cursor()

            sql = "INSERT INTO noticias(id_equipe,noticia_descricao,acao_id)  values(%s,'%s',%s) " % (a[2], noticia,a[1])
            print(sql)

            cursor_banco.execute(sql)
            conexao.commit()

            cursor_banco.close()        
            #conexao.close()


schedule.every(.1).minutes.do(rodarBusca)

now = datetime.now()
hora = str(now.hour) + str(now.minute)

while ((hora > '1000') and (hora < '2210')):
    schedule.run_pending()
    time.sleep(1)
    now = datetime.now()
    hora = str(now.hour) + str(now.minute)
