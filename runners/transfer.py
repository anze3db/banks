import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .bankinter import login, get_config


def run(args):
    driver = login()
    try:
        transfers = driver.find_element_by_id("lnkTransferencias")
        transfers.click()
        domestic = driver.find_element_by_id("seta13")
        domestic.click()
        print("Waiting for a keyboard... (this part is still buggy)")
        iframe = WebDriverWait(driver, 100000).until(
            EC.presence_of_element_located((By.ID, "transfPontuaisDomesticaNew"))
        )
        driver.switch_to.frame(iframe)
        print("Switched to iframe...")
        element = WebDriverWait(driver, 100000).until(
            EC.presence_of_element_located((By.CLASS_NAME, "keyboard"))
        )
        element = WebDriverWait(driver, 100000).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "conteudo_bold_nopadding_new")
            )
        )
        print("Keyboard detected.")
        element_value = element.text.split()
        code = (ord(element_value[1]) - 65) * 7 + (int(element_value[4]) - 1)
        card_codes = get_config("codes").split()
        password = element.find_element_by_tag_name("input")
        driver.execute_script(f"arguments[0].value = '{card_codes[code]}';", password)
    except:
        traceback.print_exc()
    finally:
        print("Press CMD-C to quit")
        while True:
            time.sleep(10)
        driver.quit()
