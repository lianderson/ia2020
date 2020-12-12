from sklearn.datasets import load_boston
boston = load_boston()

#==========================================================================================
# ORGANIZANDO A BASE - ANALISE EXPLORATORIA
#==========================================================================================
print(boston.keys())
# Resultado
#dict_keys(['data', 'target', 'feature_names', 'DESCR', 'filename'])

print(boston.feature_names)
# Resultado
#['CRIM' 'ZN' 'INDUS' 'CHAS' 'NOX' 'RM' 'AGE' 'DIS' 'RAD' 'TAX' 'PTRATIO' 'B' 'LSTAT']

print(f'Target {boston.target.shape}, Data {boston.data.shape}')
# Resultado
#Target (506,), Data (506, 13)

import pandas as pd
base = pd.DataFrame(boston.data)
#print(base.head())

base.columns = boston.feature_names
#print(base.head())

base['PRICE'] = boston.target
#print(base.head())

base.describe()
#print(base.describe)

#==========================================================================================
# TREINO E TESTE
#==========================================================================================

# y para guardar os preços das habitações de Boston e X será preenchido com todos os outros recursos, exceto os preços
X, y = base.drop('PRICE', axis=1), base['PRICE']

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

#fonte
#https://medium.com/@datalivre/regressao-linear-metricas-com-python-953af0a5dd74