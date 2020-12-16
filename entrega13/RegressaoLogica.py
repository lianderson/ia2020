import modulo as mod
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score, accuracy_score
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import roc_curve
import matplotlib . pyplot as plt

#val = [5, 1, "2020-12-01 00:00:00"]
valores_acao = mod.executaDB("SELECT *, IF(preco > UltimaModa, 1,0) as MODA, IF(preco > UltimaMedia, 1,0) as MEDIA FROM ( SELECT a.nome, c.preco, c.data_importacao, SUBSTRING_INDEX(MAX(CONCAT(e5a.data_importacao, '|', e5a.moda)), '|', -1) AS UltimaModa, SUBSTRING_INDEX(MAX(CONCAT(e5a.data_importacao, '|', e5a.media)), '|', -1) AS UltimaMedia,SUBSTRING_INDEX(MAX(CONCAT(e5a.data_importacao, '|', e5a.desvio_padra)), '|', -1) AS UltimoDesvioPadrao FROM acao AS a JOIN cotacao AS c ON a.id = c.acao_id JOIN equipe5_analise e5a ON a.id = e5a.acao_id WHERE c.equipe_id = 5 AND c.acao_id = 1 AND c.data_importacao >= '2020-11-24 00:00:00' GROUP BY a.nome, c.preco, c.data_importacao) tmp",None)
df = pd.DataFrame(valores_acao)
print(df)

#[1] = preco 14.23
#[4] = ultimaMedia 18.25
x = df.drop([0,2,3,5,6,7],1)
#[7] binario Media 0 abaixo e 1 acima.
y = df[7]
print(x)
print(y)
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state=42)

lm = LogisticRegression()
lm.fit(X_train, y_train)
'''
LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                   intercept_scaling=1, l1_ratio=None, max_iter=100,
                   multi_class='warn', n_jobs=None, penalty='none',
                   random_state=None, solver='newton-cg', tol=0.0001, verbose=0,
                   warm_start=False)
'''
pred = lm.predict(X_test)

#qualidde dados
dis = pd.DataFrame(y_test)
dis['Pred'] = pred

print(classification_report(y_test, pred))

# computa probabilidades
y_pred_prob = lm.predict_proba(X_test)[:,1]

# Gera fpr, tpr e thresholds
''''
A Curva Característica de Operação do Receptor (Curva COR), ou, do inglês, Receiver Operating Characteristic Curve (ROC curve), ou, simplesmente,
curva ROC, é uma representação gráfica que ilustra o desempenho (ou performance) de um sistema classificador binário à medida que o seu limiar de 
discriminação varia. A curva ROC é também conhecida como curva de característica de operação relativa, porque o seu critério de mudança é resultado 
da operação de duas características (PV e PF).

fpr, tpr, thresholds = roc_curve(y_test, y_pred_prob)


# curva ROC
plt.plot([0, 1], [0, 1], 'k--')
plt.plot(fpr, tpr)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.show()


yhat = lm.predict_proba(x)
yhat = yhat[:, 1]
acuracia = accuracy_score(y, lm.predict(x))
#print('O modelo obteve %0.4f de acurácia.' % acuracia)
print('AUC: %0.2f' % roc_auc_score(y, yhat))
'''
prob = pd.DataFrame({'preco':26.00, 'Ultimamedia':26.36}, index=[0])
minha_prob = lm.predict_proba(prob)
print('A probabilidade é de {}%'\
     .format(round(minha_prob[:,1][0]*100, 2)))