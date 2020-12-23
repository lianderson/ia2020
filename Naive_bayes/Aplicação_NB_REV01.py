# Importando as bibliotecas que iremos utilizar:
from nltk import word_tokenize
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.model_selection import cross_val_predict
from nltk.tokenize import TweetTokenizer
from TwitterSearch import *


# Lendo a base de dados:
df = pd.read_csv('Tweets_Mg.csv', encoding='utf-8')

# Visualizando os dados:
#print(df)

# Distribuição das classes da coluna ‘Classificação’:
#print(df.Classificacao.value_counts())


#pre processamento de texto para o twitter

tweet_tokenizer = TweetTokenizer()

# Removendo os valores duplicados da base de dados:
df.drop_duplicates(['Text'], inplace=True)

# Separando tweets e suas classes:
tweets = df['Text']
classes = df['Classificacao']



# Instancia o objeto que faz a vetorização dos dados de texto: faz isso palavras por palavras e utilizada o tokenizador do twiter
vectorizer = CountVectorizer(analyzer="word", tokenizer=tweet_tokenizer.tokenize)

# Aplica o vetorizador nos dados de texto e retorna uma matriz esparsa ( contendo vários zeros):
freq_tweets = vectorizer.fit_transform(tweets)


# Treino de modelo de Machine Learning com algoritmo Naive bayes:
modelo = MultinomialNB()
modelo.fit(freq_tweets,classes)

# Pesquisa de Tweets
vetor_texto = []

ts = TwitterSearch(
    consumer_key = '0fxQoPEzt2OpGUXZs9MepH9pC',
    consumer_secret = 'CZHcgaFgwUA0ypebLxA3lPuZQdbS06lqmbyvlLC7XkJ6LkPPx0',
    access_token = '291335726-xfri5zybR3O4fQFnwEiAp0WLUSriDqxmTSahbkfG',
    access_token_secret = 'pCpE1bEhjvBMugfjZjfgQ6SZyG507SRiZfmBJp7fMoTST'
 )

tso = TwitterSearchOrder()
tso.set_keywords(['dtex3'])
tso.set_language('pt')

for tweet in ts.search_tweets_iterable(tso):
    texto = tweet['text']
    vetor_texto.append(texto)

print(vetor_texto)

# Transforma os dados de teste em vetores de palavras:
freq_testes = vectorizer.transform(vetor_texto)



# Fazendo a classificação com o modelo treinado:
for t, c in zip (vetor_texto,modelo.predict(freq_testes)):
    # t representa o tweet e c a classificação de cada tweet.
    print (t +", "+ c)

# Probabilidades de cada classe:
print("\n")

print (modelo.classes_)
print(modelo.predict_proba(freq_testes).round(2))


