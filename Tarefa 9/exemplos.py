import numpy as np
import matplotlib . pyplot as plt
import pandas as pd
import seaborn as sns
import pymysql
import time


serie = pd.Series([10,20,30,40,50])
serie.index = ['acao1', 'acao2', 'acao3', 'acao4', 'acao5']
print(serie)



data = {'nomes':['joao', 'gabriel', 'luis'], 'idade': [22,30,40]}
df = pd.DataFrame(data)
print(df['idade'].sum())