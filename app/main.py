# http://docs.cntd.ru/document/gost-19-701-90-espd
import redis, pickle
from Globals import LOGIN, PASSWORD, REDIS_HOST, REDIS_PORT
from Model import HtmlData
from datetime import datetime

Redis = redis.StrictRedis( host=REDIS_HOST, port=REDIS_PORT, db=0 )
Redis.flushdb()

from selenium import webdriver, common
from selenium.webdriver.chrome.options import Options
import time
from tools import log, hash_
from fake_useragent import UserAgent
log_content  = log("CONTENT", "/logs/content.log")
ua = UserAgent()
userAgent = ua.random
URL = "https://betscsgo.cc/"
print(userAgent)
def init_driver():
    co = Options()
    co.add_argument('user-agent={}'.format(userAgent))
    co.add_argument('--headless')
    co.add_argument('--no-sandbox')
    co.add_argument('--disable-dev-shm-usage')
    # disable infobars
    co.add_argument('--disable-infobars')

    co.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    chrome_prefs = {}
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
    co.add_experimental_option("prefs", chrome_prefs)
    driver = webdriver.Chrome(chrome_options=co)
    return driver

class Browser:

    def __init__(self):
        self.driver = init_driver()

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

def main():
    chrome = Browser()
    driver = chrome.driver
    def __main():
        log_content.debug("starting chrome")
        log_content.debug("open page {}".format(URL))
        log_content.debug("starting autorization scene")

        try:
            driver.get("https://betscsgo.cc/")
            log_content.debug("wait 40 second for load page")
            time.sleep(40)
            scene(driver)
            log_content.debug("Checked length page:  {}".format( len( driver.page_source ) ))
        except ( common.exceptions.NoSuchElementException, common.exceptions.JavascriptException) as e:
            log_content.error("Error Not element {}. This stop process.(scene(driver) error)".format(str(e)))
            driver.close()
            raise ValueError("Error Element")
        log_content.debug("start cycle")

        while True:
            if Redis.get("stop"):
                break

            task = Redis.get("get_html")
            if task:

                task = pickle.loads( task )
                log_content.debug("task received {}".format( task ))
                driver.get( task['url'] )
                time.sleep(10)
                html = str( driver.page_source )
                if len( html ) < 150000:
                    log_content.debug("Page size less 150000 byte")
                    continue
                Redis.set( task['m_id'], pickle.dumps( { "html" : html, "url" : task['url'] } ))
                log_content.debug("response send. Data {}".format( len( html ) ))
                Redis.delete( "get_html" )


            log_content.debug("Get https://betscsgo.cc/")
            driver.get("https://betscsgo.cc/")
            time.sleep(10)
            html = str( driver.page_source )
            if len( html ) < 150000:
                log_content.debug("Page size less 150000 byte")
                continue
            log_content.debug("Response https://betscsgo.cc/ . Length: {}".format( len( html ) ) )
            

            try:
                HtmlData.insert( {
                    "html" : html,
                    "m_time": datetime.now().timestamp(),
                    } ).execute()
            except Exception:
                log_content.error("Exception occurred", exc_info=True)


            
            log_content.debug("Write to db")
            HtmlData.auto_clear_db()
            
            time.sleep(60)
            
        log_content.debug("End Job")

    try:
        __main()
    except Exception as e:
        log_content.error("Exception occurred", exc_info=True)
        driver.close()


if __name__ == '__main__':
    s = 30
    while s:
        main()
        log_content.debug("Wait 30 sec for restart main")
        time.sleep(30)
        s = s - 1

