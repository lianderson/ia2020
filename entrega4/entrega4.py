import moduloEntrega4
informacoes = ''
acoes = ["ITSA4.SA","MWET4.SA","LREN3.SA"]

for a in (acoes):
    retornoInformacoes = moduloEntrega4.retornarDados(a)
    print('---------------------------------------------------------------')
    print(retornoInformacoes)
