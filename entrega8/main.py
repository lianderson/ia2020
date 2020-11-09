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
        gera_graficos()
    elif opcao == 5:
        exec(modo)
    else:
        mod.bug()
        exec()
    if len(sys.argv) < 1:
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

    tipo_grafico = input("Qual gráfico gostaria de visualizar?\n1) Bar \n2) Linha? ")
    acao = input("Qual acao deseja visualizar? \n1) ITUB3.SA \n2) PNVL4.SA \n3)ABEV3.SA \n4) Outra digite acao. Padrão ITUB3.SA ")
    inicio = input("Data inicial da visualização. Padrão 01-02-2020 ")
    fim = input("Data final da visualização. Padrão 02-02-2020 ")
    calculo = input("Que dados gostaria de visualizar? 1) Media diaria\n2) Maior valor diária \n3) Menor valor diário\n4) Valor de Abertura \n5) Valor de Fechamento ")
    ''' Para debug!
    acao = "ITUB3.SA"
    inicio = '20-09-2020'
    fim = '30-09-2020'
    calculo = 1
    tipo_grafico = 1
    '''
    mod.gerador_graficos(tipo_grafico, acao, calculo, inicio, fim)

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
            print(e)
            pergunta = 999


if len(sys.argv) > 1:
    mod.set_modo(sys.argv[1])
    #mod.get_modo()
    print(mod.data())
    switch(1,True)
else:
    #Para debug
    #switch(4, modo=True)
    exec()