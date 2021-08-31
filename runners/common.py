import traceback

from selenium_testing_library import Screen, locators
from selenium import webdriver # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore

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
    print("log in")
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
