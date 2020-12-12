"""
TODO
1. Change IP
2. Change geolocation
3. Change MAC Address
4. Browser fingerprint

Refresh cookies 
Refresh session

"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def open_url(driver, url):
    print('[+] Opening url...')
    driver.get(url)

if __name__ == "__main__":
    #Starting the program
    print("Initializing browser...")

    #Starting URL
    url = 'https://google.com'

    #Set Chromedriver Options
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-dev-shm-using") 
    options.add_argument("--disable-extensions") 
    options.add_argument("--disable-gpu") 
    options.add_argument("--incognito")
    options.add_argument("--disable-notifications")
    options.add_argument("start-maximized") 
    options.add_argument("disable-infobars") 
    options.add_argument("--disable-setuid-sandbox") 
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument('--disable-dev-shm-usage')

    #Fire up chromedriver
    chromedriver = webdriver.Chrome("./chromedriver", options=options)

    #Open url
    open_url(chromedriver, url)
    time.sleep(5)

    # Get session
    print('[+] Session ID: ' + chromedriver.session_id)
    chromedriver.quit()

