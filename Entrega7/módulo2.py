import schedule
import moduloUtil
import time


schedule.every().hour.do(moduloUtil.pesquisa) ###verificando o valor de 30 em 30 minutos
schedule.every().hour.do(moduloUtil.ler_acao) ###verificando o valor de 30 em 30 minutos
schedule.every().hour.do(moduloUtil.contarPalavras)


while 1:
    schedule.run_pending()
    time.sleep(1)


