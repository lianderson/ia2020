import time
import random
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn import model_selection
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import RandomizedSearchCV
import matplotlib.pyplot as plt

dataFrame = pd.read_csv('dados_acoes.csv')
print(dataFrame.head())

#exclusão de colunas
x = dataFrame.drop('valor_atual', axis=1)
y = dataFrame['valor_compra']

#Dividindo os dados entre treinamento e teste
x_train, x_teste, y_train, y_teste = train_test_split(x,y, test_size=0.33, random_state=66)



#criando o modelo da randomForest
randomForestClassificado = RandomForestClassifier()
randomForestClassificado.fit(x_train, y_train)

print("modelo = ", randomForestClassificado)

#Função que executa a previsão do código
previsao = randomForestClassificado.predict(x_teste)

#Validação cruzada dos dados inseridos
#esultado = cross_val_score(randomForestClassificado, x, y, cv=10)

print("Matriz confusão")
print(confusion_matrix(y_teste, previsao))
print('\n')

print("Classificacação")
print(classification_report(y_teste, previsao))
print('\n')

#print(resultado)
#print('\n')
#print("Média dos resultados")
#print("Média dos resultados: ", resultado.mean())

#Gráfico visual dos resultados
plt.plot(x_teste,y_teste)
plt.xlabel('Valor atual no mercado')
plt.ylabel('ótimo para vendas')
plt.show()

