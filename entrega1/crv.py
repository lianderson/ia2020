#http://dontpad.com/liandersonfranco
#criar modulo para ler arquivo, calcular a raiz quadrada das ações
import csv
import math
import Aulas.ia2020.entrega1.modulo as mod


total = 0.00
count = 0

data = csv.reader(open('bd.txt', newline=''), delimiter=';', quotechar='|')
for row in data:
    try :
        ##somar todos os valores de ação
        total = mod.soma(row[1],total)
        ##para calcular media
        count += 1
        ##Exibir raiz de cada valor
        mod.raiz(row[1],row[0])
    except Exception as e:
        print(e)

media = mod.media(total,count)

print("total: R$ "+ str(total))
print("media: R$ "+ str(media))


