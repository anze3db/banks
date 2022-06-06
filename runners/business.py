import configparser
from datetime import date, timedelta

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys  # type: ignore
from selenium_testing_library import Screen, Within

from .common import get_chromedriver, input_queue, input_request_queue

config = configparser.ConfigParser()
config.read("config.ini")


def get_config(name):
    return config["bankinter"][name]


def login():
    input_request_queue.put("Enter password 🔒")
    driver = get_chromedriver()
    screen = Screen(driver)
    driver.set_window_position(0, 0, windowHandle="current")
    driver.set_window_size(597, 900)
    driver.get("https://si.unicreditbanking.net/")
    username = screen.get_by_placeholder_text("Vnesi uporabniško ime")
    username.send_keys(config["business"]["username"])
    screen.get_by_display_value("NADALJUJ").click()

    password = input_queue.get()
    screen.find_by_placeholder_text("Vnesi geslo").send_keys(password)
    screen.get_by_display_value("VSTOPI").click()

    screen.find_by_text(
        "Računi in finančni pregled",
        timeout=600,  # Long timeout so that I have the time to dismiss messages
        poll_frequency=1,
    )
    return driver, screen


def export():
    driver, screen = login()
    menu = screen.get_by_css(".menuContainer")
    Within(menu).get_by_text("Promet").click()

    screen.find_by_text("Promet po računih")

    screen.get_by_display_value("FROM_TO").click()

    end_prev_month = date.today().replace(day=1) - timedelta(days=1)

    ActionChains(driver).send_keys(
        Keys.TAB
        + f"1.{end_prev_month.month}.{end_prev_month.year}"
        + Keys.TAB
        + f"{end_prev_month.day}.{end_prev_month.month}.{end_prev_month.year}"
    ).perform()

    screen.get_by_display_value("Išči").click()
    screen.find_by_display_value("Izvozi").click()
    screen.find_by_text("export.csv").click()

    input("Finished 🎊")
