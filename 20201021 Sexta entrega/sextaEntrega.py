# ===============================================================================
# inteligencia artificial
# data: 2020 10 07
# script: desenvolver script parar pesquisar as informacoes das empresas utiolizando api do yahoo
# autores: mauricio zaquia, lindice lopes, gustavo berté
# ===============================================================================

# ===============================================================================
# importando as bibliotecas
# ===============================================================================
import moduloSextaEntrega as mqe
import schedule
import time
import pymysql
from datetime import datetime
import sys

# ===============================================================================
# criacao de variaveis
# ===============================================================================
arrayInformacoes = []
arrayAcoes = []
equipe_id = 0
acao_id = 0
acao_preco_atual = 0
acao_simbolo = ''

# ===============================================================================
# criando a funcao para rodar a busca
# ===============================================================================


def rodarBusca():
    try:
        # limpando o arrayacoes (lista) para nao duplicar as cotacoes
        arrayAcoes = []
        # ===============================================================================
        # conexao com o banco
        # ===============================================================================
        conexao = pymysql.connect(
            host='viajuntos.com.br', user='admin_ia', password='admin_ia', db='admin_ia')
        # ===============================================================================
        # fazendo o select das acoes
        # ===============================================================================
        cursor_banco = conexao.cursor()
        sql = "SELECT * FROM acao WHERE id_equipe = 2"
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

            arrayInformacoes = mqe.retornaCamposFormatados(acao_simbolo)
            acao_preco_atual = arrayInformacoes[acao_simbolo]['Preço Atual']

            # ===============================================================================
            # inserindo a cotacao na tabela cotacao no banco
            # ===============================================================================
            cursor_banco = conexao.cursor()
            sql = 'INSERT INTO cotacao(equipe_id,preco,acao_id)  values(%s,%s,%s) ' % (
                equipe_id, acao_preco_atual, acao_id)
            cursor_banco.execute(sql)
            conexao.commit()
            cursor_banco.close()

            print(acao_simbolo + ': Registro inserido em: ' + str(datetime.now()))

        conexao.close()
    except ValueError:
        print("Não foi possível converter")
    except BufferError:
        print("Buffer Cheio")
    except IOError:
        print("IOError")
    except:
        print("Erro sem tratamento:", sys.exc_info()[0])
    finally:
        conexao.close()


# ===============================================================================
# configuracao para rodar a busca
# ===============================================================================
schedule.every(.1).minutes.do(rodarBusca)
# schedule.every().hour.do(rodarBusca) #descomentar para pegar os valores de hora e hora

now = datetime.now()
hora = str(now.hour) + str(now.minute)

while (1):
    if (hora > '1000') and (hora < '2300'):
        schedule.run_pending()
        time.sleep(1)
        now = datetime.now()
        hora = str(now.hour) + str(now.minute)
