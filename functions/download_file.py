import os
import time
from selenium.webdriver import Chrome
from functions import validar_arquivos_pasta
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
env_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path=env_path)


def acomplish_download(driver: Chrome, default_extension: str = '.crdownload'):
    downloads_path = os.path.join(os.path.expanduser("~"), 'Downloads')
    old_files = validar_arquivos_pasta(downloads_path)
    
    
    TIMEOUT_DOWNLOAD = int(os.getenv('TIMEOUT_DOWNLOAD', 60))
    timeout = time.time() + TIMEOUT_DOWNLOAD
    while time.time() < timeout:
        new_files = validar_arquivos_pasta(downloads_path)

        six_months = len(new_files) - len(old_files)
        
        if six_months == 6:
            print(f"Arquivos baixados: {new_files}")
            
            if not new_files.endswith(default_extension):  
                return new_files

        time.sleep(1)
    
    if not new_files:
        return False
    
    driver.close()
    return new_files