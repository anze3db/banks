import configparser
import time
from datetime import date, timedelta

from selenium.common.exceptions import (
    NoAlertPresentException,
    NoSuchElementException,
    UnexpectedAlertPresentException,
)
from selenium.webdriver.common.keys import Keys  # type: ignore
from selenium_testing_library import Screen, locators

from .common import get_chromedriver

config = configparser.ConfigParser()
config.read("config.ini")


def get_config(name):
    return config["bankinter"][name]


def login():
    # 1st screen, enter username
    driver = get_chromedriver()
    screen = Screen(driver)
    driver.set_window_position(1194, 0, windowHandle="current")
    driver.set_window_size(797, 900)
    driver.get("https://banco.bankinter.pt/particularesEN/indexHomeMC.jsp")
    screen.find_by_css("#onetrust-accept-btn-handler").click()
    username = screen.get_by(locators.Css("#txtUserName"))
    username.clear()
    username.send_keys(get_config("username") + Keys.RETURN)

    print("entering keys")
    for fiscal_element in screen.find_all_by(locators.Css(".box_unlock_mc")):
        name = fiscal_element.get_attribute("name")
        if "idNif" in name or not fiscal_element.is_enabled():
            continue
        idx = int(name[-1:]) - 1
        fiscal_element.send_keys(get_config(name[:-1])[idx])
    fiscal_element.send_keys(Keys.RETURN)

    # There might be one or two alerts that we want to hide before continuing
    while True:
        try:
            screen.find_by_text("invalid", timeout=2)
        except UnexpectedAlertPresentException:
            try:
                driver.switch_to.alert.dismiss()
            except NoAlertPresentException:
                pass
        except NoSuchElementException:
            break
    frame = screen.find_by_name("central")
    driver.switch_to.frame(frame)
    return driver, screen


def set_date_field(screen, name, value):
    for idx, element in enumerate((f"seldia{name}", f"selmes{name}", f"selano{name}")):
        field = screen.get_by_id(element)
        field.clear()
        field.send_keys(value[idx])


def export():
    driver, screen = login()
    screen.find_by_text(
        "Client Position Summary - Deposits and Investments", timeout=300
    )
    current_accounts = screen.find_by_id("lnkContasOrdem")
    current_accounts.click()

    current_accounts = screen.find_by_id("lnkDOMov")
    current_accounts.click()

    screen.find_by_text("Find Entries")
    down_arrow = screen.get_by_id("setaMov")
    down_arrow.click()

    start = date.today().replace(day=1) - timedelta(days=1)
    set_date_field(
        screen, "inic", ["01", "{:02d}".format(start.month), str(start.year)]
    )
    set_date_field(
        screen, "fim", [str(start.day), "{:02d}".format(start.month), str(start.year)]
    )

    find = screen.find_all_by_xpath(
        "//img[@src='/particularesEN/images/botoes/b_find.png']"
    )[0]
    find.click()

    iframe = screen.find_by_id("listaMov", timeout=100000)
    driver.switch_to.frame(iframe)

    export_el = screen.find_by_xpath(
        "//img[@src='/particularesEN/images/botoes/b_exportar.png']", timeout=10000
    )
    export_el.click()
    time.sleep(2)  # Wait for download to finish
    print("Bankinter: Done 🎉 ")
