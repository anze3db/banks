import configparser
from datetime import date, timedelta

from selenium_testing_library import Screen

from .common import get_chromedriver

config = configparser.ConfigParser()
config.read("config.ini")


def get_config(name):
    return config["n26"][name]


def login():
    driver = get_chromedriver()
    screen = Screen(driver)
    driver.set_window_position(597, 0, windowHandle="current")
    driver.set_window_size(797, 900)
    driver.get("https://app.n26.com/login")
    screen.get_by_label_text("Email").send_keys(config["n26"]["email"])
    screen.get_by_label_text("Password").send_keys(config["n26"]["password"])
    screen.get_by_text("Log in").click()
    print("Confirm on your 📱")
    screen.find_by_text("Current balance", timeout=5 * 60, poll_frequency=1)
    return driver, screen


def export():
    driver, screen = login()
    driver.get("https://app.n26.com/downloads")

    end_prev_month = date.today().replace(day=1) - timedelta(days=1)
    start_date = screen.find_by_css("#start-date-picker")
    start_date.clear()
    start_date.send_keys(f"{end_prev_month.year}-{end_prev_month.month:02}-01")

    end_date = screen.find_by_css("#end-date-picker")
    end_date.clear()
    end_date.send_keys(
        f"{end_prev_month.year}-{end_prev_month.month:02}-{end_prev_month.day:02}"
    )

    screen.get_by_text("Download CSV").click()
    input("Success 🎉")
