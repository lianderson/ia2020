import schedule
import moduloUtil
import time


schedule.every(.1).minutes.do(moduloUtil.ler_acao)
schedule.every(.1).minutes.do(moduloUtil.pesquisa)
schedule.every(.1).minutes.do(moduloUtil.contarPalavras)

while True:
    schedule.run_pending()
    time.sleep(1)


