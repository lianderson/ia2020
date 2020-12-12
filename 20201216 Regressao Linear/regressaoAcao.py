# ===============================================================================
# inteligencia artificial
# data: 2020 12 16
# script: desenvolver script parar pesquisar as acoes e fazer regressao linear
# autores: mauricio zaquia, lindice lopes, gustavo berté
# ===============================================================================

# ===============================================================================
# importando as bibliotecas
# ===============================================================================
import pymysql
import pandas as pd

# ===============================================================================
# criacao de variaveis
# ===============================================================================
arrayRobo = []

# ===============================================================================
# conexao com o banco
# ===============================================================================
conexao = pymysql.connect(
    host='viajuntos.com.br', user='admin_ia', password='admin_ia', db='admin_ia')
# ===============================================================================
# fazendo o select das acoes
# ===============================================================================
cursor_banco = conexao.cursor()
sql = "SELECT valor_compra, valor_venda, valor_atual FROM equipe2_robo;"
cursor_banco.execute(sql)
for linhas in (cursor_banco.fetchall()):
    arrayRobo.append(linhas)
cursor_banco.close()

#for a in (arrayRobo):
    #valor_compra = a[1]
    #valor_venda = a[2]
    #acao_id = a[3]
    #valor_atual = a[6]

    #print(valor_compra)

#==========================================================================================
# ORGANIZANDO A BASE - ANALISE EXPLORATORIA
#==========================================================================================

base = pd.DataFrame(arrayRobo)
print(base)

base.columns = ['valor_compra', 'valor_venda', 'valor_atual']
print(base)

#==========================================================================================
# TREINO E TESTE
#==========================================================================================

# regressao linear multipla
X, y = base.drop('valor_compra', axis=1), base['valor_compra']

# dividindo 70% para treinamento 30% para teste, divisao
from sklearn.model_selection import train_test_split

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,   random_state=0)

# Treinando a base com os dados
from sklearn.linear_model import LinearRegression

regression = LinearRegression()
regression.fit(X_train, y_train)
# previsões
Y_prev = regression.predict(X_test)

# O Erro Médio Absoluto é a soma de todos esses erros divido pelo número de pontos.
from sklearn.metrics import mean_absolute_error
print(f'MAE {mean_absolute_error(y_test, Y_prev)}')

# O Erro Médio Quadrático tem como base o Erro Médio Absoluto, contudo, o erro (distância entre os pontos e a reta) é elevado ao quadrado.
from sklearn.metrics import mean_squared_error
print(f'MSE {mean_squared_error(y_test, Y_prev)}')

# A Validação Cruzada testa como o modelo se comporta diante de dados que não foram usados como treinamento.
from sklearn.model_selection import cross_val_score
resultado = cross_val_score(regression, X_test, y_test, cv = 10)
print(resultado.mean())

# Gerando o grafico
import matplotlib.pyplot as plt
#matplotlib inline
plt.scatter(y_test, Y_prev)
range = [y_test.min(), Y_prev.max()]
plt.plot(range, range, 'red')
plt.xlabel('Preço real')
plt.ylabel('Preço predito')
plt.show()
