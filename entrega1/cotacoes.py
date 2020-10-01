
#Grupo 1
# Integrantes do grupo: Juliana, Jonathan e Matthias

var = 0
arquivo = open('cotacoes.txt' , 'a') # w escrever

while var != 2:
    var = int(input('Digite o que deseja fazer:\n 1 - cadastrar \n 2 - Sair\n'))

    if var == 1:
        empresa =(str(input('Empresa: ')))
        data_hora = (str(input('Data/Hora: ')))
        valor_acao = (str(input('Valor da ação: ')))
        desc = (str(input('Descrição: ')))
        arquivo.write('Empresa: {}| Data/hora: {}| Valor Cotação: {}| Descrição: {}\n'.format(empresa,data_hora,valor_acao,desc) )


arquivo.close()


arquivo = open('cotacoes.txt' , 'r')
print(arquivo.read())
