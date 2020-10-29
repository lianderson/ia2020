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
    noticias = mod.executaDB("SELECT id,noticia_descricao FROM noticias where equipe_id = '5'", None)

    for x in noticias:
        palavras = Counter(x[1].split())
        for y in palavras.items():
            val = [x[0], y[0]]
            noticias = mod.executaDB("SELECT id FROM equipe5_palavra where noticia_id = '%s' AND palavra = %s limit 1", val)
            if noticias:
                print("achou palavra "+y[0])
                continue
            else:
                print("Nao achou palavra "+y[0])
            print("insert")
            val = [y[0], y[1], x[0]]
            query = mod.executaDB("INSERT INTO equipe5_palavra (palavra,quantidade,noticia_id) values(%s,%s,%s)", val)

except Exception as e:
    print(e)
