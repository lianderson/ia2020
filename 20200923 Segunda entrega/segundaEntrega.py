import moduloSegundaEntrega
import csv

#===============================================================================
# lendo o arquivo
#===============================================================================

#data = csv.reader(open('D:\\Projetos\\python\\InteligenciaArtificial\\#github\\ia2020\\20200923 Segunda entrega\\db_acoes.txt', newline=''), delimiter='|', quotechar='|')
data = csv.reader(open('D:\\Projetos\\python\\InteligenciaArtificial\\#github\\ia2020\\20200923 Segunda entrega\\db_acoes.txt', newline=''), delimiter=';', quotechar=';')

#===============================================================================
# percorrendo os valores
#===============================================================================

for row in data:
    try :
         #values = row[2].split()
         valorFormatado = row[2].replace('valor_acao=','')   
         valorFormatado = valorFormatado.replace(',','.')
         print('Valor: ' + valorFormatado + ' Valor raiz: ' + str(moduloSegundaEntrega.calcularRaiz(valorFormatado)))

    except Exception as e:
        print(e)            

