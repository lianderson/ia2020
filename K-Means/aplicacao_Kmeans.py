import numpy as np #para manipular os vetores
from matplotlib import pyplot as plt #para plotar os gráficos
from sklearn.cluster import KMeans #para usar o KMeans
import pymysql


conexao = pymysql.connect(
    host = '152.67.55.61',
    user = 'admin_ia',
    password = 'admin_ia',
    db = 'admin_ia',
    charset = 'utf8mb4',
    cursorclass = pymysql.cursors.DictCursor
)


with conexao.cursor() as cursor: #adicionando calculos esdtatisticos ao banco de dados
    sql = 'select c.acao_id, c.preco from cotacao as c inner join acao AS a on c.acao_id = a.id WHERE c.equipe_id = 4  order by c.data_importacao DESC';
    cursor.execute(sql)

    vetor = [] + []
    for row in cursor.fetchall(): ### linha da tabela do banco
        buscaAcao = (row['acao_id']) ###
        buscaPreco = (row['preco'])

        vetor.append([buscaAcao]+[buscaPreco])


        print(vetor)

dataset = np.array(vetor)

plt.scatter(dataset[:,1], dataset[:,0]) #posicionamento dos eixos x e y
plt.xlim(0, 30) #range do eixo x
plt.ylim(25, 35) #range do eixo y
plt.grid() #função que desenha a grade no nosso gráfico



kmeans = KMeans(n_clusters = 3, #numero de clusters
init = 'k-means++', n_init = 10, #algoritmo que define a posição dos clusters de maneira mais assertiva
max_iter = 300) #numero máximo de iterações
pred_y = kmeans.fit_predict(dataset)


plt.scatter(dataset[:,1], dataset[:,0], c = pred_y) #posicionamento dos eixos x e y
plt.xlim(0, 30) #range do eixo x
plt.ylim(25, 35) #range do eixo y
plt.xlabel("Valores")
plt.ylabel("Ação Id")
plt.title("Ação id X Valores \n K-Means")
plt.grid() #função que desenha a grade no nosso gráfico
plt.scatter(kmeans.cluster_centers_[:,1],kmeans.cluster_centers_[:,0], s = 70, c = 'red') #posição de cada centroide no gráfico
plt.show()