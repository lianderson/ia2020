from  scipy import stats
import pandas as pd
import modulo as mod

manipula = {'T1':[2,6,7,8],'T2':[20,50,15,10]}
medidas = pd.DataFrame(manipula)
print(medidas)
media_geometrica = stats.gmean(manipula['T1'],axis=0)
media_geometrica = stats.gmean(manipula['T2'],axis=0)
print(media_geometrica)
h_geometrica = stats.hmean(manipula['T1'],axis=0)

##aplitude maior-menor=
#print(df[1].min())
#print(df[1].max())
#variança
#print(df[1].var())


'''
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
serie  =  pd.Series([10,20,30,50,60])
print(serie)
print(serie.count())  ### conta os elementos
serie.index = ['Acao1','Acao2','Acao3','acao4','Acao5']
print(serie)

data = {'nome':['lianderson','Paulo','Joao','Zeca','Jones'],'idade':[1,2,3,4,5]}
df =  pd.DataFrame(data)
print(df )
print(df['idade'].sum())
print(df['idade'].count())
print(df['idade'].min())
print(df['idade'].max())
print(df['idade'].std())#desvio padrao
print(df['idade'].mean())#//media
print(df.describe())
print(df.head())
print(df.tail())
#print(df.sort_index(axis=1,ascending=False))
print(df['idade']>30)
print(df.sort_values(by="nome"))
#print("Media ="+str(df['idade'].median()))#//media
print(df['idade'].median())#//mediana
print(df['idade'].mode())#//mediana
amplitudade =df['idade'].max() - df['idade'].min()
print(amplitudade)
print(df['idade'].var())#//variaca

=======================================================

from   scipy import  stats
import pandas as pd
manipula = {'T1':[2,6,7,8],'T2':[2,1,7,8]}

medidas = pd.DataFrame(manipula)
print(medidas)
media_geometrica  =  stats.gmean(manipula['T1'],axis=0)
print(media_geometrica)
media_geometrica  =  stats.gmean(manipula['T2'],axis=0)
print(media_geometrica)
media_harmonica  =  stats.hmean(manipula['T1'],axis=0)
print(media_harmonica)
media_harmonica  =  stats.hmean(manipula['T1'],axis=0)
print(media_harmonica)

'''