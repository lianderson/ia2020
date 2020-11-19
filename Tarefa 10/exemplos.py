import numpy as np
import matplotlib . pyplot as plt
import pandas as pd
import seaborn as sns
import pymysql
import time
from scipy import stats


""" serie = pd.Series([10,20,30,40,50])
serie.index = ['acao1', 'acao2', 'acao3', 'acao4', 'acao5']
print(serie)



data = {'nomes':['joao', 'gabriel', 'luis'], 'idade': [22,30,40]}
df = pd.DataFrame(data)
print(df['idade'].sum()) """

#mediana - média aritimetica - median()

#moda - maior frequencia - mode

manipula = {'T1':[2,6,8,7], 'T2':[20,50,15,10]}
manipula = {'T1':[2,6,8,7], 'T2':[20,50,15,10]}

medidas = pd.DataFrame(manipula)
print(medidas)

#media geometrica
med_geo = stats.gmean(manipula['T1'], axis=0)
print('mgt1 = ' + str(med_geo))

med_geo = stats.gmean(manipula['T2'], axis=0)
print('mgt2 = ' + str(med_geo))

#media harmonica
med_harm = stats.hmean(manipula['T1'], axis=0)
print('mht1 = ' + str(med_harm))

med_harm = stats.hmean(manipula['T2'], axis=0)
print('mht2 = ' + str(med_harm))

#amplitude
amp = (medidas['T1'].max() - medidas['T1'].min())
print('ampt1 = ' + str(amp))

amp = (medidas['T2'].max() - medidas['T2'].min())
print('ampt2 = ' + str(amp))

#varianca
var = medidas['T1'].var()
print('vart1 = ' + str(var))

var = medidas['T2'].var()
print('vart2 = ' + str(var))
