"""from sklearn import tree

features = [[140, 1], [130, 1],
           [150, 0], [170, 0]]
labels = [0, 0, 1, 1] # 0 é maçã e 1 é laranja

# o classificador encontra padrões nos dados de treinamento
clf = tree.DecisionTreeClassifier() # instância do classificador
clf = clf.fit(features, labels) # fit encontra padrões nos dados

# iremos utilizar para classificar uma nova fruta
print(clf.predict([[150, 0]]))"""

import pandas as pd
from sklearn.tree import DecisionTreeClassifier,export_graphviz
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
import pydot
import graphviz
from ipywidgets import interactive
from IPython.display import SVG,display
from graphviz import Source
from mlxtend.plotting import plot_decision_regions
import matplotlib.pyplot as plt

df_dados = pd.read_csv('arvore de decisao/dados2.csv')
df_dados.head()

df_dados.info()

X_train, X_test, y_train, y_test = train_test_split(df_dados.drop('recomendacao',axis=1),df_dados['recomendacao'],test_size=0.3)

X_train.shape,X_test.shape
((16, 6), (14, 6))
y_train.shape,y_test.shape
((16,), (14,))
# Instânciando o objeto classificador:
clf = DecisionTreeClassifier()

# Treinando o modelo de arvore de decisão:
clf = clf.fit(X_train,y_train)

# Verificando as features mais importantes para o modelo treinado:
clf.feature_importances_

for feature,importancia in zip(df_dados.columns,clf.feature_importances_):
    print("{}:{}".format(feature, importancia))

resultado = clf.predict(X_test)
resultado

print(metrics.classification_report(y_test,resultado))

dot_data = export_graphviz( 
         clf, 
         out_file=None,
         feature_names=df_dados.drop('recomendacao',axis=1).columns,
         class_names=['esperar','comprar', 'vender'],  
         filled=True, rounded=True,
         proportion=True,
         node_ids=True,
         rotate=False,
         label='all',
         special_characters=True
        )  
graph = graphviz.Source(dot_data)  
graph

# feature matrix
X,y = df_dados.drop('recomendacao',axis=1),df_dados['recomendacao']

# feature labels
features_label = df_dados.drop('recomendacao',axis=1).columns

# class label
class_label = ['esperar','comprar', 'vender']


def plot_tree(crit, split, depth, min_samples_split, min_samples_leaf=0.2):
    estimator = DecisionTreeClassifier(
           random_state = 0 
          ,criterion = crit
          ,splitter = split
          ,max_depth = depth
          ,min_samples_split=min_samples_split
          ,min_samples_leaf=min_samples_leaf
    )
    estimator.fit(X, y)
    graph = Source(export_graphviz(estimator
      , out_file=None
      , feature_names=features_label
      , class_names=class_label
      , impurity=True
      , filled = True))
    display(SVG(graph.pipe(format='svg')))
    return estimator

inter=interactive(plot_tree 
   , crit = ["gini", "entropy"]
   , split = ["best", "random"]
   , depth=[1,2,3,4,5,10,20,30]
   , min_samples_split=(1,5)
   , min_samples_leaf=(1,5))

display(inter)

def visualize_fronteiras(msamples_split,max_depth):
    X = df_dados[['valor_venda','valor_compra']].values
    y = df_dados.recomendacao.values
    clf = DecisionTreeClassifier(min_samples_split=msamples_split,max_depth=max_depth)
    tree = clf.fit(X, y)

    plt.figure(figsize=(16,9))
    plot_decision_regions(X.astype(np.integer), y.astype(np.integer), clf=tree, legend=2)

    plt.xlabel('valor_venda')
    plt.ylabel('valor_compra')
    plt.title('Decision Tree')
    plt.show()

visualize_fronteiras(2,max_depth=30)



#https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.csv