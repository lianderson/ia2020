import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib . pyplot as plt

import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve, classification_report,\
                            accuracy_score, confusion_matrix, auc

# Importando de um repositório no github
titanic = pd.read_csv('https://raw.githubusercontent.com/agconti/kaggle-titanic/master/data/train.csv')
titanic.head()

# Transforma classe em categorico
titanic['Pclass'] = titanic['Pclass'].astype('category')

modelo = smf.glm(formula='Survived ~ Age + Pclass + Sex', data=titanic,
                family = sm.families.Binomial()).fit()
print(modelo.summary())

print(np.exp(modelo.params[1:]))
(np.exp(modelo.params[1:]) - 1) * 100
# Agora vamos fazer com sklearn para aproveitar as métricas
model = LogisticRegression(penalty='none', solver='newton-cg')
baseline_df = titanic[['Survived', 'Pclass', 'Sex', 'Age']].dropna()
y = baseline_df.Survived
X = pd.get_dummies(baseline_df[['Pclass', 'Sex', 'Age']], drop_first=True)
print(X)

model.fit(X, y)
LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                   intercept_scaling=1, l1_ratio=None, max_iter=100,
                   multi_class='warn', n_jobs=None, penalty='none',
                   random_state=None, solver='newton-cg', tol=0.0001, verbose=0,
                   warm_start=False)

print(model.coef_) # Temos o mesmo modelo!
# Predizendo as probabilidades
yhat = model.predict_proba(X)

yhat = yhat[:, 1] # manter somente para a classe positiva


confusion_matrix(y, model.predict(X)) # usando a função do sklearn
pd.crosstab(y, model.predict(X))  # fazendo "na mão"
acuracia = accuracy_score(y, model.predict(X))
print('O modelo obteve %0.4f de acurácia.' % acuracia)

print(classification_report(y, model.predict(X)))
print('AUC: %0.2f' % roc_auc_score(y, yhat))
eu = pd.DataFrame({'Age':29, 'Pclass_2':1, 'Pclass_3':0, 'Sex_male':1}, index=[0])
minha_prob = model.predict_proba(eu)
print('Eu teria {}% de probabilidade de sobrevivência se estivesse no Titanic'\
      .format(round(minha_prob[:,1][0]*100, 2)))

coleguinha = pd.DataFrame({'Age':32, 'Pclass_2':0, 'Pclass_3':0, 'Sex_male':1}, index=[0])
prob_do_coleguinha = model.predict_proba(coleguinha)
print('Meu coleguinha teria {}% de probabilidade de sobrevivência se estivesse no Titanic'\
      .format(round(prob_do_coleguinha[:,1][0]*100, 2)))