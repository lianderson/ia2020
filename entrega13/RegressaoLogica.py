import modulo as mod
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
import pandas as pd


#val = [5, 1, "2020-12-01 00:00:00"]
#valores_acao = mod.executaDB("SELECT a.nome,c.preco,c.data_importacao from acao as a join cotacao as c ON a.id = c.acao_id where c.equipe_id= %s AND c.acao_id= %s AND c.data_importacao >= %s", val)
valores_acao = mod.executaDB("SELECT *, IF(preco > UltimaModa, 1,0) as MODA, IF(preco > UltimaMedia, 1,0) as MEDIA FROM ( SELECT a.nome, c.preco, c.data_importacao, SUBSTRING_INDEX(MAX(CONCAT(e5a.data_importacao, '|', e5a.moda)), '|', -1) AS UltimaModa, SUBSTRING_INDEX(MAX(CONCAT(e5a.data_importacao, '|', e5a.media)), '|', -1) AS UltimaMedia,SUBSTRING_INDEX(MAX(CONCAT(e5a.data_importacao, '|', e5a.desvio_padra)), '|', -1) AS UltimoDesvioPadrao FROM acao AS a JOIN cotacao AS c ON a.id = c.acao_id JOIN equipe5_analise e5a ON a.id = e5a.acao_id WHERE c.equipe_id = 5 AND c.acao_id = 1 AND c.data_importacao >= '2020-11-24 00:00:00' GROUP BY a.nome, c.preco, c.data_importacao) tmp",None)
df = pd.DataFrame(valores_acao)
print(df)

x = df.drop([0,2,4,5,6,7],1)
y = df[7]
print(x)
print(y)
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state=42)

lm = LogisticRegression()
lm.fit(X_train, y_train)

pred = lm.predict(X_test)

dis = pd.DataFrame(y_test)
dis['Pred'] = pred

print(classification_report(y_test, pred))