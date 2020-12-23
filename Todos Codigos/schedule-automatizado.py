import schedule
import moduloUtil
import time
from datetime import datetime

schedule.every(30).minutes.do(moduloUtil.ler_acao)
schedule.every(30).minutes.do(moduloUtil.decisaoAcao)
schedule.every(6).hours.do(moduloUtil.pesquisa)
schedule.every(6).hours.do(moduloUtil.contarPalavras)

while True:
    schedule.run_pending()
    time.sleep(1)

