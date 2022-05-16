from selenium import webdriver  # type: ignore


def get_chromedriver():
    try:
        return webdriver.Chrome("./chromedriver")
    except Exception as e:
        print("Possible issue with Chromedriver", e)
        raise
