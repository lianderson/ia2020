import numpy as np
import matplotlib . pyplot as plt
fig,ax = plt.subplots()
x = np.linspace(0,10,1000)
y = np.sin(x)
z = np.cos(x)
ax.plot(x,y,'k--',linewidth=5, label='Aula Grafico preto')
ax.plot(x,z,'r--',linewidth=5, label='Aula Grafico Vermelho')
ax.set_title(' Teste ')
ax.legend(loc='upper center')
plt.xlabel("Altura") ####
plt.ylabel("Peso")
plt.show()



plt.plot([1,2,3,4,5],[1,4,5,6,9])
plt.xlabel("Y")
plt.ylabel("Y")
plt.show()



###bar
grupo    = ['Ação 1 ','Ação 2','Ação 3 ']
valores  = [5,10,50]
plt.bar(grupo,valores)
plt.show()
