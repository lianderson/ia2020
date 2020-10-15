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
# criacao de variaveis
# ===============================================================================
arrayNoticia = []
arrayAcoes = []

acao = ''
data = ''
titulo = ''
noticia = ''

equipe_id = 0
acao_id = 0
acao_simbolo = ''

# ===============================================================================
# criando a funcao para disparar a busca
# ===============================================================================
def rodarBusca():
    arrayAcoes = []
    listaUrls = []
    # ===============================================================================
    # conexao com o banco
    # ===============================================================================
    conexao = pymysql.connect(host='viajuntos.com.br',user='admin_ia',password='admin_ia',db='admin_ia')
    # ===============================================================================
    # fazendo o select das acoes
    # ===============================================================================
    # configurando um cursor (quem percorre a tabela)
    cursor_banco = conexao.cursor()
    sql = "SELECT id, nome, id_equipe FROM acao WHERE id_equipe = 2"
    cursor_banco.execute(sql)
    for linhas in (cursor_banco.fetchall()):
        arrayAcoes.append(linhas)
    cursor_banco.close()
    # ===============================================================================
    # lendo os dados
    # ===============================================================================
    for a in (arrayAcoes):
        acao_id = a[0]
        acao_simbolo = a[1]
        equipe_id = a[2]        

        # retorna lista de urls
        listaUrls.append(mqe.retornaURL(acao_simbolo))

    for i in (listaUrls):

        for k in (i):
            
            url_noticia = k
            # retorna noticias de acordo com cada url
            arrayNoticia = mqe.retornaInformacoesSite(url_noticia)
            noticia = arrayNoticia[1]

            # ===============================================================================
            # inserindo a noticia na tabela cotacao no banco
            # ===============================================================================
            cursor_banco = conexao.cursor()
            sql = 'INSERT INTO noticias (equipe_id,noticia_descricao,url_noticia,acao_id) values (%s,"%s","%s",%s)' % (equipe_id, noticia, url_noticia, acao_id)
            cursor_banco.execute(sql)
            conexao.commit()
            cursor_banco.close()        

            print(acao_simbolo + ': Registro inserido em: ' + str(datetime.now()))

    conexao.close()

# ===============================================================================
# configuracao para rodar a busca
# ===============================================================================
schedule.every(.1).minutes.do(rodarBusca)
#schedule.every().hour.do(rodarBusca) #descomentar para pegar os valores de hora e hora

now = datetime.now()
hora = str(now.hour) + str(now.minute)

while (1):    
    if (hora > '1000') and (hora < '1800'):
        schedule.run_pending()
        time.sleep(1)
        now = datetime.now()
        hora = str(now.hour) + str(now.minute)
