"""
TODO
1. Change IP (DONE)
2. Change geolocation (DONE)
3. Change MAC Address (DONE)
4. Browser fingerprint

Refresh cookies (DONE) - though not any, it is still good practice to delete them
Refresh session (DONE)

"""

import time, random, requests
from sample.proxy1 import Proxy1
from sample.proxy2 import Proxy2
from sample.proxy3 import Proxy3
from selenium import webdriver
from sample.geolocation import Geolocation
from sample.mac_address import MacAddress
from sample.user_agents import UserAgents
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def open_url(driver, url):
    print('[+] Opening url...')
    driver.get(url)

if __name__ == "__main__":
    #Starting the program
    print("Initializing browser...")

    #Starting URL
    url = 'https://google.com'

    #MAC Address, User Agent
    macaddress = MacAddress()
    macaddress.mac_address('usb0')
    useragents = UserAgents()
    user_agent = useragents.random_user_agent()
    
    # Proxy
    proxy1 = Proxy1()
    proxy2 = Proxy2()
    proxy3 = Proxy3()
    proxy_choices = {'SSL Proxies': proxy1.proxy(), 'GitHub elite proxies':proxy2.proxy(), 'GimmeProxies': proxy3.proxy()}

    #Confirm proxy's validity
    def check_proxy():
        proxy_found = False
        counter = 0
        PROXY, country = '',''
        while proxy_found:
            proxy_choice = random.choice(list(proxy_choices.values()))
            print(proxy_choice)
            PROXY, country = proxy_choice
            counter += 1
            print("\r" + "[+] Looking for valid IP address: " + str(counter), end="")
            try:
                r = requests.get('https://pinchofyum.com/', proxies={'https': 'https://{}'.format(PROXY)}, timeout=8)
                if r.status_code == 200:
                    print('\n[+] IP Address used as proxy: ' + PROXY)
                    proxy_not_found = True
                else:
                    PROXY, country = proxy_choice()
            except:
                PROXY, country = proxy_choice()
        return PROXY, country

    PROXY, country = check_proxy()
    print('[+] Proxy of choice: ' + str(PROXY))

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

    #Set DesiredCapabilities
    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
    capabilities['proxy'] = {
        "httpProxy": PROXY,
        "ftpProxy": PROXY,
        "sslProxy": PROXY,
        "noProxy": None,
        "proxyType": "MANUAL",
        "class": "org.openqa.selenium.Proxy",
        "autodetect": False
    }

    #Fire up chromedriver
    chromedriver = webdriver.Chrome("./chromedriver", options=options, desired_capabilities=capabilities)

    #Confirm user agent
    agent = useragents.get_user_agent(chromedriver)
    print("[+] User Agent in use: ", agent)
    location_change = Geolocation()
    location_change.change_geolocation(chromedriver, country)

    #Open url
    open_url(chromedriver, url)
    time.sleep(5)
    #### Add your own code here.

    # Get session
    print('[+] Session ID: ' + chromedriver.session_id)
    print('[+] Deleting all cookies...')
    chromedriver.delete_all_cookies()
    chromedriver.quit()

