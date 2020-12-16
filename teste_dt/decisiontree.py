import pandas as pd
from sklearn.tree import DecisionTreeClassifier,export_graphviz
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pydot
import graphviz
import numpy as np
from ipywidgets import interactive
from IPython.display import SVG,display
from graphviz import Source
from mlxtend.plotting import plot_decision_regions
import matplotlib.pyplot as plt

df_diabetes = pd.read_csv('C:\\Users\\Gabriel Soares\\Documents\\GitHub\\ia2020\\teste_dt\\diabetes.csv')
df_diabetes.head()

X_train, X_test, y_train, y_test = train_test_split(df_diabetes.drop('Outcome',axis=1),df_diabetes['Outcome'],test_size=0.3)
X_train.shape,X_test.shape
((537, 8), (231, 8))
y_train.shape,y_test.shape
((537,), (231,))

clf = DecisionTreeClassifier()

clf = clf.fit(X_train,y_train)

# Verificando as features mais importantes para o modelo treinado:
clf.feature_importances_

for feature,importancia in zip(df_diabetes.columns,clf.feature_importances_):
    print("{}:{}".format(feature, importancia))

resultado = clf.predict(X_test)
#resultado

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
#graph

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

def visualize_fronteiras(msamples_split,max_depth):
    X = df_diabetes[['Glucose','Insulin']].values
    y = df_diabetes.Outcome.values
    clf = DecisionTreeClassifier(min_samples_split=msamples_split,max_depth=max_depth)
    tree = clf.fit(X, y)

    plt.figure(figsize=(16,9))
    plot_decision_regions(X, y, clf=tree, legend=2)

    plt.xlabel('Glucose')
    plt.ylabel('Insulin')
    plt.title('Decision Tree')
    plt.show()

# Chamando a função criada anteriormente:

visualize_fronteiras(10,max_depth=8)