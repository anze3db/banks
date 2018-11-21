import time
from datetime import date, timedelta
from .common import login

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def set_date_field(driver, name, value):
    for idx, element in enumerate((f'seldia{name}', f'selmes{name}', f'selano{name}')):
        field = driver.find_element_by_id(element)
        field.clear()
        field.send_keys(value[idx])


def run(args):
    driver = login()
    current_accounts = driver.find_element_by_id("lnkContasOrdem")
    current_accounts.click()

    current_accounts = driver.find_element_by_id("lnkDOMov")
    current_accounts.click()

    down_arrow = WebDriverWait(driver, 100000).until(
        EC.presence_of_element_located((By.ID, "setaMov"))
    )
    down_arrow.click()

    start = date.today().replace(day=1) - timedelta(days=1)
    set_date_field(driver, 'inic', ['01', str(start.month), str(start.year)])
    set_date_field(driver, 'fim', [str(start.day), str(start.month), str(start.year)])

    find = driver.find_elements_by_xpath("//img[@src='/particularesEN/images/botoes/b_find.png']")[0]
    find.click()

    iframe = WebDriverWait(driver, 100000).until(
        EC.presence_of_element_located((By.ID, "listaMov"))
    )
    driver.switch_to.frame(iframe)

    export = WebDriverWait(driver, 100000).until(
        EC.presence_of_element_located((By.XPATH, "//img[@src='/particularesEN/images/botoes/b_exportar.png']"))
    )
    export.click()
    while True:
        time.sleep(10)
