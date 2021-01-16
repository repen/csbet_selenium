import os, time
from Globals import LOGIN, PASSWORD, SITE
from itertools import count

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tools import log
log_content  = log("MAIN")
URL = SITE

log_content.info( "Start script" )

def init_driver():
    co = Options()
    # co.add_argument('--headless')
    # co.add_argument('--no-sandbox')
    co.add_argument('--disable-dev-shm-usage')
    co.add_argument("--start-maximized")
    co.add_argument("--disable-blink-features=AutomationControlled")
    # co.add_argument("--start-fullscreen")
    # disable infobars
    co.add_argument('--disable-infobars')


    # co.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    co.add_experimental_option("excludeSwitches", ["enable-automation"])
    co.add_experimental_option('useAutomationExtension', False)
    chrome_prefs = {}
    # chrome_prefs["profile.default_content_settings"] = {"images": 2}
    # chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
    co.add_experimental_option("prefs", chrome_prefs)
    driver = webdriver.Chrome(
        os.path.join( os.getcwd(), "chromedriver"), options=co)
    return driver

def scene(driver):
    driver.execute_script('document.querySelector("a.userbar-login").click()')
    time.sleep(5)
    login = driver.find_element_by_css_selector("input.textField[name=username]")
    password = driver.find_element_by_css_selector("input.textField[name=password]")
    btn = driver.find_element_by_css_selector("#login_btn_signin input.btn_green_white_innerfade")
    login.send_keys( LOGIN )
    password.send_keys( PASSWORD )
    btn.click()
    time.sleep(5)

def work(driver, url):
    log_content.debug("Get %s", url)
    driver.get(url)
    time.sleep(10)
    html = str( driver.page_source )

    log_content.debug("Response %s. Length: %d", url, len( html ) )
    log_content.debug("Write to db")
    log_content.debug("End Job")

def main():
    driver = init_driver()

    log_content.debug("starting chrome")
    log_content.debug("open page {}".format(URL))
    log_content.debug("starting auth scene")
    driver.get(URL)
    log_content.info("Waiting 30 sec")
    time.sleep(30)
    scene(driver)
    driver.get( URL )
    log_content.debug("Checked length page:  {}".format( len( driver.page_source ) ))

    for _ in count():
        work(driver, URL)
        time.sleep(60)

if __name__ == '__main__':
    main()

