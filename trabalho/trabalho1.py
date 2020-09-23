import csv
import os
import time
import funcoes


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    print("---------------")
    print("1 - listar")
    print("2 - adicionar")
    print("3 - raiz quadrada")
    print("4 - sair")
    print("---------------")


print_menu()
menu = int(input("Digite o que deseja fazer: "))
cls()
while menu != 4:

    if menu == 2:
        f = open('cotacao.csv', 'a')
        sigla = str(input("Sigla:"))
        data = str(input("Data:"))
        cotacao = str(input("Cotacao:"))
        descricao = str(input("Descricao:"))
        fnames = ['sigla', 'data', 'cotacao', 'descricao']
        writer = csv.DictWriter(f, fieldnames=fnames)
        writer.writerow({'sigla': sigla, 'data': str(data), 'cotacao': cotacao, 'descricao': descricao})
        f.close()

    if menu == 1:
        f2 = open('cotacao.csv', 'r')
        strf2 = f2.read()
        print(strf2)
        f2.close()
        time.sleep(4);

    if menu == 3:
        funcoes.calculaRaiz()

    print_menu()
    menu = int(input("Digite o numero da acao: "))
    cls()
