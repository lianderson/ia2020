import matplotlib . pyplot as plt
import pymysql
from datetime import datetime


arrayPreco = []
arrayDatas = []

conexao = pymysql.connect(host='viajuntos.com.br',user='admin_ia', password='admin_ia', db='admin_ia')

cursor_banco = conexao.cursor()
sql = "select * from cotacao where acao_id = '32' order by data_importacao"

cursor_banco.execute(sql)
conexao.close()

for linhas in (cursor_banco.fetchall()):
    arrayPreco.append(linhas[2])
    data= linhas[3]
    arrayDatas.append(data.strftime('%d/%m'))
cursor_banco.close()


fig,ax = plt.subplots()
ax.bar(arrayDatas,arrayPreco,label='Aula Grafico')
plt.xlabel("Valor")
plt.ylabel("Data")
plt.show()