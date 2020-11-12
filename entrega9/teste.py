import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

serie = pd.Series([10,20,30,40,50])
print(serie)
print(serie.count())
serie.index = ['Acao1','Acao2','Acao3','Acao4','Acao5']
print(serie)