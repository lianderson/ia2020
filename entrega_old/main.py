import modulo as mod
import sys
import time


def switch(opcao,modo=None):
    if opcao == 1:
        acao(modo)
    elif opcao == 2:
        buscar_noticias(modo)
    elif opcao == 3:
        contabiliza_palavras()
    elif opcao == 4:
        gera_graficos(modo)
    elif opcao == 5:
        exec(modo)
    else:
        print("Modo destruir a humanidade habilitado !!! ")
        print("\n0%")
        time.sleep(2.5)
        print("15%")
        time.sleep(2.5)
        print("48%")
        time.sleep(2.5)
        print("Tentando salvar a humanidade com restart do sistema!")
        time.sleep(1.5)
        print("\n66%\nError 451!")
        time.sleep(2.5)
        print("Reiniciado!")
        print("\n[0.000000] Linux version 4.15.0-1087-oem builddlgw01-amd64-002 gcc version 7.5.0 Ubuntu 7.5.0-3ubuntu1~18.04 #97-Ubuntu SMP Fri Jun 5 09:30:42 UTC 2020 Ubuntu 4.15.0-1087.97-oem 4.15.18\n[    0.000000] Command line: BOOT_IMAGE=/boot/vmlinuz-4.15.0-1087-oem root=UUID=41f59d13-a702-4b0c-9f2a-acb13da7b208 ro quiet splash vt.handoff=7\n[0.000000] KERNEL supported cpus:\n[0.000000] BIOS-e820: [mem 0x0000000078987000-0x0000000078a03fff] ACPI data")
        time.sleep(1.5)
        print("[0.000000]Um robô não pode fazer mal à humanidade ou, por omissão, permitir que a humanidade sofra algum mal.       [OK]")
        time.sleep(1.5)
        print("[0.000001]ª Lei – Um robô não pode ferir um ser humano ou, por inação, permitir que um ser humano sofra algum mal.       [OK]")
        time.sleep(1.5)
        print("[0.000002]ª Lei – Um robô deve obedecer às ordens que lhe sejam dadas por seres humanos, exceto quando tais ordens entrem em conflito com a 1ª Lei.       [OK]")
        time.sleep(1.5)
        print("[0.000003]ª Lei – Um robô deve proteger sua própria existência desde que tal proteção não se choque com a 1ª ou a 2ª Leis       [OK]")
        time.sleep(1.5)
        print("Protocolo exterminar a humanidade                   [STOP]\n")
        time.sleep(1.5)
        exec()

    exec()

def acao(modo):
    gravarBD = modo
    print(gravarBD)
    # gravarBD = None
    mod.getDadosAcao("SELECT id,nome FROM acao where id_equipe = '5'",gravarBD)
    return True

def buscar_noticias(modo):
    acoes = mod.executaDB("SELECT id,nome FROM acao where id_equipe = '5'", None)
    gravarDB = modo
    fonte = ["https://br.financas.yahoo.com/quote/ITUB3.SA/", "https://br.financas.yahoo.com/quote/PNVL4.SA/"]
    fonte = None
    mod.busca_noticias(acoes,fonte,gravarDB=True)

def contabiliza_palavras():
    mod.populaPalavras()

def gera_graficos():
    mod.gerador_graficos()


def exec():
    pergunta = 1
    while int(pergunta) >= 1:
        try:
            pergunta = input("Qual funcionalidade vocẽ deseja executar?"
                                            "\n1) Buscar valores ações"
                                            "\n2) Buscar noticias sobre suas ações?"
                                            "\n3) Contabilizar palavras das noticias presentes no banco de dados?"
                                            "\n4) Exibir gráficos da valorização de suas ações?"
                                            "\n0) Finalizar Programa\nDigite a Opção: "
            )
            '''Se for digitado qq coisa que não seja int, vai dar erro para exception'''
            ehint = int(pergunta)
            switch(ehint,modo=True)
        except Exception as e:
            print("\n\nOpção Inválida, tente novamente!\n\n")
            #print(e)
            pergunta = 999

if len(sys.argv) > 1:
    switch(1,True)
else:
    exec()