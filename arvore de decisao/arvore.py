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

df_diabetes = pd.read_csv('arvore de decisao/dados.csv')
df_diabetes.head()

df_diabetes.info()

X_train, X_test, y_train, y_test = train_test_split(df_diabetes.drop('Outcome',axis=1),df_diabetes['Outcome'],test_size=0.3)

X_train.shape,X_test.shape
((537, 8), (231, 8))
y_train.shape,y_test.shape
((537,), (231,))
# Instânciando o objeto classificador:
clf = DecisionTreeClassifier()

# Treinando o modelo de arvore de decisão:
clf = clf.fit(X_train,y_train)

# Verificando as features mais importantes para o modelo treinado:
clf.feature_importances_

for feature,importancia in zip(df_diabetes.columns,clf.feature_importances_):
    print("{}:{}".format(feature, importancia))

resultado = clf.predict(X_test)
resultado

print(metrics.classification_report(y_test,resultado))

dot_data = export_graphviz( 
         clf, 
         out_file=None,
         feature_names=df_diabetes.drop('Outcome',axis=1).columns,
         class_names=['0','1'],  
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
X,y = df_diabetes.drop('Outcome',axis=1),df_diabetes['Outcome']

# feature labels
features_label = df_diabetes.drop('Outcome',axis=1).columns

# class label
class_label = ['0','1']


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



#https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.csv