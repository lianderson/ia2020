#===============================================================================
# inteligencia artificial
# data: 2020 09 16
# script: desenvolver script parar criar um arquivo .txt com os campos -> empresa, data_hora, valor_acao, descricao
# autores: mauricio zaquia, lindice lopes, gustavo berté
#===============================================================================

#===============================================================================
# criação das variaveis
#===============================================================================

caminho = 'D:\\Projetos\\python\\InteligenciaArtificial\\trabalhos\\2020 09 16 script\\db_acoes.txt'

empresa = ''
data_hora = ''
valor_acao = ''
descricao = ''

#===============================================================================
# regra de negócio
#===============================================================================

i = input("Deseja inserir novo registro? 1=SIM 0=NAO: ")

while int(i) >= 1:
    empresa = input("Empresa: ")
    data_hora = input("Data e Hora: ")
    valor_acao = input("Valor da ação: ")
    descricao = input("Descrição: ")

    #escrever arquivo
    f = open(caminho, 'a')
    f.write('empresa=' + empresa +
        ';data_hora=' + data_hora + 
        ';valor_acao=' + valor_acao + 
        ';descricao=' + descricao + '\n')
    f.close()

    i = input("Deseja inserir novo registro? 1=SIM 0=NAO: ")

#===============================================================================
# lendo arquivo e separando em linhas
#===============================================================================
with open(caminho) as fp:
    for cnt, line in enumerate(fp):
        print("Linha {}: {}".format(cnt, line))