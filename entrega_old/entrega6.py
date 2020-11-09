#http://dontpad.com/liandersonfranco
# -*- coding: utf-8 -*-
import urllib.request #pacote para trabalhar com mewb
import json #pacote para manipular JSON
import Aulas.ia2020.entrega6.modulo as mod

gravarBD = "SIM"
#gravarBD = None

try:
    mod.getDadosAcao("SELECT id,nome FROM acao where id_equipe = '5'",gravarBD)
except Exception as e:
    print(e)