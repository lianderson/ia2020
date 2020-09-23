import math

def soma(valor,total):
    valor = float(valor.replace(',', '.'))
    total = total + valor
    return total

def media(total,count):
    total = total/count
    return total


def raiz(val):
    val = float(val.replace(',', '.'))
    print("raiz: R$ " + str(math.sqrt(val)))