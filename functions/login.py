import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
env_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path=env_path)


cpf = os.getenv("CPF")
login = os.getenv("USUARIO")
senha = os.getenv("SENHA")


def make_login(driver: Chrome):
    try:
        actions = ActionChains(driver)
        wait = WebDriverWait(driver, 10)
        
        driver.get("https://sistema.ssw.inf.br/bin/ssw0422")
        
        rcs_input = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/input[1]")))
        actions.move_to_element(rcs_input).click().send_keys("RCS").perform()
        cpf_input = driver.find_element(By.XPATH, "/html/body/form/input[2]")
        actions.move_to_element(cpf_input).click().send_keys(cpf).perform()
        login_input = driver.find_element(By.XPATH, "/html/body/form/input[3]")
        actions.move_to_element(login_input).click().send_keys(login).perform()
        senha_input = driver.find_element(By.XPATH, "/html/body/form/input[4]")
        actions.move_to_element(senha_input).click().send_keys(senha).perform()
        login_button = driver.find_element(By.XPATH, "/html/body/form/a")
        actions.move_to_element(login_button).click().perform()

    except Exception as e:
        raise e
