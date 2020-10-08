import csv
import modulo_raiz_equipe4
decisao = 0
arquivo = open('cotacao.txt' , 'a') # w escrever

while decisao != 5:
    decisao = int(input('Digite:\n 1 - cadastrar \n 2 - Raiz Quadrada Cotações\n 3 - Pesquisa \n 4 - Informação Ação \n 5 - Sair '))

    if decisao == 1:
        empresa =(str(input('Empresa: ')))
        data_hora = (str(input('Data/Hora: ')))
        val_acao = (str(input('Valor da ação: ')))
        desc = (str(input('Descrição: ')))
        arquivo.write('Empresa: {}| Data/hora: {}| Valor Cotação: {}| Descrição: {}\n'.format(empresa,data_hora,val_acao,desc) )



    if decisao == 2:
        data = csv.reader(open('C:\\Users\\ultra\\Desktop\\IA\\Equipe_4\\cotacao.txt', newline=''), delimiter='|', quotechar='|')# ABRE O ARQUIVO EM CSV

        for row in data:
            try :
                valor_corrigido = row[2].replace('Valor Cotação:','')#primeiro busca somente qu esta escrita no que foi delimitado pelo row[2]..Após retira a palavra "valor cotação:" e deixa somento o valor com virgula
                valor_corrigido = valor_corrigido.replace(',','.')# susbtitue a virgula pelo ponto
                print('{}: Valor Cotação{} e sua raiz quadrada = {:.3f} ' .format(row[0],valor_corrigido,modulos_equipe4.calcula_raiz(valor_corrigido)))#ibuscando no modulo da equipe 4 a função raiz quadrada

            except Exception as e:
                print(e)

    if decisao == 3:
        consulta = input(str("Digite sua pesquisa: "))
        modulos_equipe4.pesquisa(consulta)

    if decisao == 4:
        modulo_raiz_equipe4.ler_acao()



arquivo.close()