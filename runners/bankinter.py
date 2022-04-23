import time
from datetime import date, timedelta

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import traceback

from selenium_testing_library import Screen, locators
from selenium import webdriver  # type: ignore
from selenium.webdriver.common.keys import Keys  # type: ignore

import configparser

config = configparser.ConfigParser()
config.read("config.ini")


def get_config(name):
    return config["bankinter"][name]


def _get_driver():
    return webdriver.Chrome("./chromedriver")


def login():
    # 1st screen, enter username
    driver = _get_driver()
    screen = Screen(driver)
    driver.get("https://banco.bankinter.pt/particularesEN/indexHomeMC.jsp")
    screen.get_by_css("#onetrust-accept-btn-handler").click()
    username = screen.get_by(locators.Css("#txtUserName"))
    username.clear()
    username.send_keys(get_config("username") + Keys.RETURN)

    try:
        print("entering keys")
        for fiscal_element in screen.get_all_by(locators.Css(".box_unlock_mc")):
            name = fiscal_element.get_attribute("name")
            if "idNif" in name or not fiscal_element.is_enabled():
                continue
            idx = int(name[-1:]) - 1
            fiscal_element.send_keys(get_config(name[:-1])[idx])
        fiscal_element.send_keys(Keys.RETURN)
        # There are two alerts that we want to hide
        driver.switch_to.alert.dismiss()
        try:
            driver.switch_to.alert.dismiss()
        except:
            # sometimes the second alert isn't there
            pass
        driver.switch_to.default_content
        frame = driver.find_element_by_name("central")
        driver.switch_to.frame(frame)
    except:
        traceback.print_exc()
    finally:
        return driver


def set_date_field(driver, name, value):
    for idx, element in enumerate((f"seldia{name}", f"selmes{name}", f"selano{name}")):
        field = driver.find_element_by_id(element)
        field.clear()
        field.send_keys(value[idx])


def export():
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
    set_date_field(
        driver, "inic", ["01", "{:02d}".format(start.month), str(start.year)]
    )
    set_date_field(
        driver, "fim", [str(start.day), "{:02d}".format(start.month), str(start.year)]
    )

    find = driver.find_elements_by_xpath(
        "//img[@src='/particularesEN/images/botoes/b_find.png']"
    )[0]
    find.click()

    iframe = WebDriverWait(driver, 100000).until(
        EC.presence_of_element_located((By.ID, "listaMov"))
    )
    driver.switch_to.frame(iframe)

    export = WebDriverWait(driver, 100000).until(
        EC.presence_of_element_located(
            (By.XPATH, "//img[@src='/particularesEN/images/botoes/b_exportar.png']")
        )
    )
    export.click()
    input("Done 🎉 ")
