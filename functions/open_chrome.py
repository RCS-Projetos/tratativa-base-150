import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def driver(headless=False):
    chrome_options = webdriver.ChromeOptions()
    if not headless:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    
    download_folder = os.path.join(os.path.expanduser("~"), 'Downloads')

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
        # Dá permissão total na pasta (para garantir que o Chrome consiga escrever)
        os.chmod(download_folder, 0o777)

    print(f"DEBUG: Salvando arquivos em: {download_folder}")

    prefs = {
        "download.default_directory": download_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    
    chrome_options.add_experimental_option("prefs", prefs)
        
    return webdriver.Chrome(options=chrome_options)

def wait(driver: webdriver.Chrome):
    return WebDriverWait(driver, 10)

def actions(driver: webdriver.Chrome):
    return ActionChains(driver)