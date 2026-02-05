import os
import time
from datetime import timedelta
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from functions import validar_arquivos_pasta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
load_dotenv()

url = os.getenv('URL_150')

def treat_150(driver: Chrome):
    wait = WebDriverWait(driver, 20)
    
    try:
        downloads_path = os.path.join(os.path.expanduser("~"), 'Downloads')
        old_files = validar_arquivos_pasta(downloads_path)

        driver.get(url)
        
        dt_0 = datetime.now().strftime("%d%m%y")
        dt_1 = (datetime.now() - timedelta(days=31)).strftime("%d%m%y")
        dt_2 = (datetime.now() - timedelta(days=62)).strftime("%d%m%y")
        dt_3 = (datetime.now() - timedelta(days=93)).strftime("%d%m%y")
        dt_4 = (datetime.now() - timedelta(days=124)).strftime("%d%m%y")
        dt_5 = (datetime.now() - timedelta(days=155)).strftime("%d%m%y")
        dt_6 = (datetime.now() - timedelta(days=186)).strftime("%d%m%y")

        meses = [
            dt_0,
            dt_1,
            dt_2,
            dt_3,
            dt_4,
            dt_5,
            dt_6
        ]

        for i in range(len(meses)-1):
            data_inicial = meses[i+1]
            data_final = meses[i]

            campos = [
                ("/html/body/form/input[1]", data_inicial),
                ("/html/body/form/input[2]", data_final),
                ("/html/body/form/input[8]", "S"),
                ("/html/body/form/input[9]", "S")
            ]
        
            for xpath, valor in campos:
                campo = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                driver.execute_script("arguments[0].value = arguments[1]", campo, valor)
                time.sleep(1)
        
        
            search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/a[1]")))
            search_button.click()
            time.sleep(3)

        time.sleep(10)

        new_files = validar_arquivos_pasta(downloads_path)
        downloaded_files = new_files - old_files

        files = [file for file in downloaded_files if file.endswith('.sswweb')]

        return files

    except Exception as e:
        print(f"Erro ao processar o relatório 150: {e}")
        raise Exception(f"Falha no processo 150: {e}")
        
