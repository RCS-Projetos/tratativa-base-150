import pandas as pd
from io import StringIO
import os
from dotenv import load_dotenv
from datetime import datetime
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from functions import validar_arquivos_pasta


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
env_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path=env_path)

    
def tratar_base_156(file_content: str) -> pd.DataFrame:
    df = pd.read_html(StringIO(file_content), header=0)[0]
    df['Opção'] = df['Opção'].str[0:3]
    return df
    

def busca_base_156(driver: Chrome):
    
    wait:  WebDriverWait = WebDriverWait(driver, 10)
    
    html = wait.until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/form/div[2]/div[2]/table[1]")
            ))
    
    table_html = html.get_attribute('outerHTML')
    
    return tratar_base_156(table_html)


def validar_relatorio_156(df: pd.DataFrame, option: str, date_time: datetime) -> list[int] | list[None]:
    df_validado = df.copy()

    date_time = pd.to_datetime(date_time)
     
    user = os.getenv("USUARIO")
    
    mascara = (
        (df_validado['Opção'] == option) & 
        (df_validado['Usuário'] == user) & 
        (df_validado['Data/Hora Solicitação'].astype('datetime64[ns]') >= date_time) &
        (df_validado['Unnamed: 8'] == 'Baixar')
    )

    df_validado['Validado'] = mascara

    indices_encontrados = df_validado[mascara].index.tolist()

    return indices_encontrados

def download_base(driver: Chrome, index: int):
    print(f"Baixando relatório na linha {index+2}")
    download_button = driver.find_element(By.XPATH, f'/html/body/form/div[2]/div[2]/table[1]/tbody/tr[{index+2}]/td[9]/div/a')
    actions = ActionChains(driver)
    actions.move_to_element(download_button).click().perform()
    

def acomplish_download(driver: Chrome, index: int, default_extension: str = '.crdownload'):
    downloads_path = os.path.join(os.path.expanduser("~"), 'Downloads')
    old_files = validar_arquivos_pasta(downloads_path)
    download_base(driver, index)
    
    TIMEOUT_DOWNLOAD = int(os.getenv('TIMEOUT_DOWNLOAD', 60))
    timeout = time.time() + TIMEOUT_DOWNLOAD
    while time.time() < timeout:
        new_files = validar_arquivos_pasta(downloads_path)
        downloaded_files = new_files - old_files
        
        if downloaded_files:
            
            file = max(downloaded_files, key=os.path.getctime)
            
            print(f"Arquivo baixado: {file}")
            
            if not file.endswith(default_extension):  
                return file

        time.sleep(1)
    
    if not file:
        return False
    
    driver.close()
    return file
     
    
    
    
def open_page_156(driver: Chrome, options: str, date_time: datetime):
    url = os.getenv('URL_156')
    
    if driver.current_url != url:
        driver.get(url) 
    else:
        time.sleep(2)
        driver.refresh()
        
    df = busca_base_156(driver)
    
    index_base = validar_relatorio_156(df, option=options, date_time=date_time)
    
    if index_base:
        file =acomplish_download(driver, index_base[0], default_extension='.crdownload')
        return file
    else:
        return False 
        