"""
TODO
1. Change IP
2. Change geolocation
3. Change MAC Address (DONE)
4. Browser fingerprint

Refresh cookies 
Refresh session

"""

import time
from sample.mac_address import MacAddress
from sample.user_agents import UserAgents
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

    #MAC Address, User Agent, Proxy
    macaddress = MacAddress()
    macaddress.mac_address('usb0')
    useragents = UserAgents()
    user_agent = useragents.random_user_agent()

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
    options.add_argument("user-agent={}".format(user_agent))

    #Fire up chromedriver
    chromedriver = webdriver.Chrome("./chromedriver", options=options)

    #Confirm user agent
    agent = useragents.get_user_agent(chromedriver)
    print("[+] User Agent in use: ", agent)

    #Open url
    open_url(chromedriver, url)
    time.sleep(5)
    # Add your own code.

    # Get session
    print('[+] Session ID: ' + chromedriver.session_id)
    chromedriver.quit()

