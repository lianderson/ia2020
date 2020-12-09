# ===============================================================================
# inteligencia artificial
# data: 2020 10 07
# script: desenvolver script parar pesquisar as informacoes das empresas utiolizando api do yahoo
# autores: mauricio zaquia, lindice lopes, gustavo berté
# ===============================================================================

# ===============================================================================
# importando as bibliotecas
# ===============================================================================
import moduloDecimaSegundaEntrega as mqe
import schedule
import time
import pymysql
from datetime import datetime
import sys

# ===============================================================================
# criacao de variaveis
# ===============================================================================
caminho = 'D:\\Projetos\\python\\InteligenciaArtificial\\#github\\ia2020\\20201021 Sexta entrega\\log_cotacoes.txt'

arrayInformacoes = []
arrayAcoes = []
equipe_id = 0
acao_id = 0
acao_preco_atual = 0
acao_simbolo = ''
decisao = ''

# ===============================================================================
# criando a funcao para rodar a busca
# ===============================================================================


def rodarBusca():
    try:
        # limpando o arrayacoes (lista) para nao duplicar as cotacoes
        arrayAcoes = []
        arrayAnalise = []
        # ===============================================================================
        # conexao com o banco
        # ===============================================================================
        conexao = pymysql.connect(host='viajuntos.com.br', user='admin_ia', password='admin_ia', db='admin_ia')
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
            arrayAnalise=[]
            acao_id = a[0]
            acao_simbolo = a[1]
            equipe_id = a[2]

            arrayInformacoes = mqe.retornaCamposFormatados(acao_simbolo)
            acao_preco_atual = arrayInformacoes[acao_simbolo]['Preço Atual']

            # ===============================================================================
            # busca informacoes da analise
            # ===============================================================================
            conexao = pymysql.connect(host='viajuntos.com.br', user='admin_ia', password='admin_ia', db='admin_ia')
            cursor_banco = conexao.cursor()
            sql = 'SELECT media, desvio_padra FROM equipe2_analise WHERE acao_id = %s' % (acao_id)
            cursor_banco.execute(sql)            
            for b in (cursor_banco.fetchall()):
                arrayAnalise.append(b)
            cursor_banco.close()

            for c in(arrayAnalise):                
                v_analise_media = c[0]
                v_desvio_padrao = c[1]

                # o valor de compra é definido pelo valor atual menos o desvio padrão, ou seja, se mais barato comprar
                v_valor_compra =  (acao_preco_atual - v_desvio_padrao)
                # o valor de venda é definido pelo valor atual mais o desvio padrão, ou seja, se mais caro vender
                v_valor_venda = (acao_preco_atual + v_desvio_padrao)
            
                v_valor_compra = float(v_valor_compra)
                v_valor_venda = float(v_valor_venda)

            # se o preco atual da acao for menor que a media da analise, então comprar 
            # se o preco atual da acao for maior que a media da analise, então vender 
            # ou se igual define-se como neutro
            if (acao_preco_atual < float(v_analise_media)):
                decisao = ''
                decisao = 'comprar'
                print(acao_simbolo + " Preco " + str(acao_preco_atual) + " menor que a media " + str(v_analise_media) + ", comprar!")
            elif (acao_preco_atual > float(v_analise_media)):
                decisao = ''
                decisao = 'vender'
                print(acao_simbolo + " Preco " + str(acao_preco_atual) + " maior que a media " + str(v_analise_media) + ", vender!")
            else:                
                decisao = ''
                decisao = 'neutro'
                print(acao_simbolo + " Preco " + str(acao_preco_atual) + " igual a media " + str(v_analise_media) + ", neutro!")

            # ===============================================================================
            # inserindo a cotacao na tabela cotacao no banco
            # ===============================================================================
            cursor_banco = conexao.cursor()
            sql = 'INSERT INTO equipe2_robo(valor_compra,valor_venda,acao_id,equipe_id,valor_atual,decisao) values(%s,%s,%s,%s,%s,"%s") ' % (v_valor_compra,v_valor_venda,acao_id,equipe_id,acao_preco_atual,decisao)
            cursor_banco.execute(sql)
            conexao.commit()
            cursor_banco.close()

            print(acao_simbolo + ': Registro inserido em: ' + str(datetime.now()))
            mqe.gravaLog(caminho, acao_simbolo +': Registro inserido em: ' + str(datetime.now()) + '\n')

        if (conexao.open):
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
        if (conexao.open):
            conexao.close()
        mqe.gravaLog(caminho, 'Executado em: ' + str(datetime.now()) + '\n')


# ===============================================================================
# configuracao para rodar a busca
# ===============================================================================
schedule.every(.1).minutes.do(rodarBusca)
# schedule.every().hour.do(rodarBusca) #descomentar para pegar os valores de hora e hora

now = datetime.now()
hora = str(now.hour) + str(now.minute)

while (1):
    rodarBusca()
    # if (hora > '1000') and (hora < '2400'):
    # schedule.run_pending()
    # time.sleep(1)
    #now = datetime.now()
    #hora = str(now.hour) + str(now.minute)
