import dados as dado # Nao esta no git, pois tem dados sensiveis
from googlesearch import search
from goose3 import Goose
import datetime #https://www.w3schools.com/python/python_datetime.aspentrega3entrega3
import urllib.request #pacote para trabalhar com mewb
import json #pacote para manipular JSON
import pymysql
import schedule
import time
from  collections  import Counter
import numpy as np
import matplotlib . pyplot as plt
import calendar
import traceback
import pandas as pd
import seaborn as sns


def conta_palavra():
    lista = []
    conexao = pymysql.connect(host='viajuntos.com.br', user='admin_ia', passwd='admin_ia', db='admin_ia')
    cursor_banco = conexao.cursor()
    select_noticia = "SELECT id,noticia_descricao FROM noticias where equipe_id = '3'"
    cursor_banco.execute(select_noticia)
    for linha in cursor_banco.fetchall():
        lista.append(linha)

    for x in lista:
        word = Counter(x[1].split())
        for y in word.items():
            qtd_palavras = [y[0], y[1], x[0]]
            query = "INSERT INTO equipe3_palavra (palavra,quantidade,noticia_id) VALUES ('"+y[0]+"',,2)"
            print(query)
            cursor_banco.execute(query)
            cursor_banco.commit()
            cursor_banco.close()

conta_palavra()