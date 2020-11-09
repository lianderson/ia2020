import modulo as mod

def switch(opcao):
    switcher = {
        1: acao,
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }
def acao():
    gravarBD = "SIM"
    # gravarBD = None
    mod.getDadosAcao("SELECT id,nome FROM acao where id_equipe = '5'",gravarBD)

switch(1)
