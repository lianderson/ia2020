import Aulas.ia2020.entrega8.modulo as mod
import numpy as np
import matplotlib . pyplot as plt

try :

    valor = mod.executaDB("SELECT preco,data_importacao FROM cotacao WHERE acao_id = '1' order by data_importacao",None)
    datas = list()
    valores = list()
    for x in valor:
        #data = x[1].replace('18:00:01','')
        datas.append(x[1])
        valores.append(x[0])

    fig, ax = plt.subplots()
    #ax.bar(datas, valores, label=("$ " + str(valores)))
    ax.bar(datas, valores)
    plt.xlabel("Data")
    plt.ylabel("Valor")
    plt.show()


except Exception as e:
    print(e)