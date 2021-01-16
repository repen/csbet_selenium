# http://docs.cntd.ru/document/gost-19-701-90-espd
import os, time
from Globals import LOGIN, PASSWORD, SITE
from Model import HtmlData
from datetime import datetime
from itertools import count

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tools import log
from fake_useragent import UserAgent
log_content  = log("MAIN")
ua = UserAgent()
userAgent = ua.random
URL = SITE
WAITH = 40

print(userAgent)

def init_driver():
    co = Options()
    co.add_argument('user-agent={}'.format(userAgent))
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
        os.path.join(os.getcwd(), "chromedriver"), options=co)
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

def prepare_site(driver):
    driver.get(URL)
    time.sleep(5)
    driver.execute_script('window.open("https://betscsgo.in/");')
    time.sleep(10)
    driver.switch_to.window(driver.window_handles[0])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def work(driver, url):
    log_content.debug("Get %s", url)
    driver.get(url)
    time.sleep(10)
    html = str( driver.page_source )
    # if len( html ) < 150000:
    #     log_content.debug("Page size less 150000 byte")
    #     return
    
    log_content.debug("Response %s. Length: %d", url, len( html ) )
    

    HtmlData.insert( {
        "html" : html,
        "m_time": datetime.now().timestamp(),
        } ).execute()


    log_content.debug("Write to db")
    HtmlData.auto_clear_db()
    log_content.debug("End Job")

def main():
    driver = init_driver()

    log_content.debug("starting chrome")
    log_content.debug("open page {}".format(URL))
    log_content.debug("starting autorization scene")
    prepare_site(driver)
    scene(driver)
    log_content.debug("Checked length page:  {}".format( len( driver.page_source ) ))

    for _ in count():
        work(driver, URL)
        time.sleep(60)

def test_cloudscraper():
    import cloudscraper
    scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
    print(scraper.get("https://betscsgo.in/").text)  # => "<!DOCTYPE html><html><head>..."

def test_selen():
    dr = init_driver()
    dr.get("https://betscsgo.cc/")
    log_content.debug("wait 40 second for load page")
    time.sleep(40)

    screen = dr.get_screenshot_as_png()
    with open("screen.png", "wb") as f:
        f.write(screen)

    scene(dr)


if __name__ == '__main__':
    main()

