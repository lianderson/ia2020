import Aulas.ia2020.entrega7.modulo as mod
from  collections  import Counter

#from  collections  import Counter
#frases = "Hoje é dia de aula IA, queremos mais informações. Hoje"
#print(Counter(frases.split()))
#frases = "Hoje é dia de aula IA, queremos mais informações. Hoje"
#chaves_unicas = set(frases.split())
#frequencia= [(item,frases.split().count(item)) for item in chaves_unicas]
#print(frequencia)

try :
    mod.populaPalavras()
except Exception as e:
    print(e)
