import schedule
import moduloUtil
import time


schedule.every(1).minutes.do(moduloUtil.pesquisa) ###verificando o valor de 30 em 30 minutos
schedule.every(1).minutes.do(moduloUtil.ler_acao) ###verificando o valor de 30 em 30 minutos

while 1:
    schedule.run_pending()
    time.sleep(1)


