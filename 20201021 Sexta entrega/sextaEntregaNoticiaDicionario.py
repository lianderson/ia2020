# ===============================================================================
# inteligencia artificial
# data: 2020 10 07
# script: desenvolver script parar pesquisar as informacoes das empresas utilizando api do yahoo
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
caminho = 'D:\\Projetos\\python\\InteligenciaArtificial\\#github\\ia2020\\20201021 Sexta entrega\\log_noticias.txt'

arrayNoticia = []
arrayAcoes = []

acao = ''
data = ''
titulo = ''
noticia = ''

equipe_id = 0
acao_id = 0
acao_simbolo = ''

cont = 0

executando = False
erro = ''

# ===============================================================================
# criando a funcao para disparar a busca
# ===============================================================================


def rodarBusca():
    global executando
    global erro
    try:
        executando = True
        arrayAcoes = []
        listaUrls = []
        # ===============================================================================
        # conexao com o banco
        # ===============================================================================
        conexao = pymysql.connect(
            host='viajuntos.com.br', user='admin_ia', password='admin_ia', db='admin_ia')
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

            # dicionario
            # BBSE3.SA / 4
            if (acao_id == 4):
                listaUrls.append(mqe.retornaURL("noticias de  bb seguridade"))
                listaUrls.append(mqe.retornaURL("noticias de  banco do brasil"))

            # CCRO3.SA / 5
            if (acao_id == 5):
                listaUrls.append(mqe.retornaURL("noticias de  rodovias brasileiras"))
                listaUrls.append(mqe.retornaURL("noticias de  transportes rodovias"))

            # UNIP3.SA / 6
            if (acao_id == 6):
                listaUrls.append(mqe.retornaURL("noticias de  quimica brasileira"))
                listaUrls.append(mqe.retornaURL("noticias de  carbocloro"))
                listaUrls.append(mqe.retornaURL("noticias de usos industriais brasil"))

            for i in (listaUrls):

                #print(listaUrls)

                for k in (i):
                    arrayNoticia = []

                    url_noticia = k

                    # retorna noticias de acordo com cada url
                    arrayNoticia = mqe.retornaInformacoesSite(url_noticia)
                    noticia = arrayNoticia[1]

                    # ===============================================================================
                    # verifica se noticia não esta em branco
                    # ===============================================================================
                    if (len(noticia) > 0):
                        # ===============================================================================
                        # verifica se url ja foi inserida
                        # ===============================================================================
                        cursor_banco = conexao.cursor()
                        cont = mqe.verificaNoticiaDuplicada(cursor_banco, url_noticia)
                        cursor_banco.close

                        if (cont == 0):
                            # ===============================================================================
                            # inserindo a noticia na tabela cotacao no banco
                            # ===============================================================================
                            cursor_banco = conexao.cursor()
                            sql3 = 'INSERT INTO noticias (equipe_id,noticia_descricao,url_noticia,acao_id) values (%s,"%s","%s",%s)' % (equipe_id, noticia, url_noticia, acao_id)
                            cursor_banco.execute(sql3)
                            conexao.commit()
                            cursor_banco.close()
                            # escrever arquivo de log
                            mqe.gravaLog(caminho, acao_simbolo + ': Registro inserido em: ' + str(datetime.now()) + '\n')
            listaUrls = []
        if (conexao.open):
            conexao.close()
        executando = False
    except ValueError:
        erro = "Não foi possível converter"
        print(erro)
        mqe.gravaLog(caminho, erro + str(datetime.now()) + '\n')
    except BufferError:
        erro = "Buffer Cheio"
        print(erro)
        mqe.gravaLog(caminho, erro + str(datetime.now()) + '\n')
    except IOError:
        erro = "IOError"
        print(erro)
        mqe.gravaLog(caminho, erro + str(datetime.now()) + '\n')
    except:
        erro = "Erro sem tratamento:"
        print(erro, sys.exc_info()[0])
        mqe.gravaLog(caminho, erro + str(datetime.now()) + '\n')
    finally:
        if (conexao.open):
            conexao.close()
        print('Executado em: ' + str(datetime.now()))
        mqe.gravaLog(caminho, 'Executado em: ' + str(datetime.now()) + '\n')
        executando = False


# ===============================================================================
# configuracao para rodar a busca
# ===============================================================================
schedule.every(5).minutes.do(rodarBusca)
# schedule.every().hour.do(rodarBusca) #descomentar para pegar os valores de hora e hora

now = datetime.now()
hora = str(now.hour) + str(now.minute)

while (1):
    if (hora > '1000') and (hora < '1900'):
        if (executando == False):
            schedule.run_pending()
            time.sleep(1)
            now = datetime.now()
            hora = str(now.hour) + str(now.minute)
