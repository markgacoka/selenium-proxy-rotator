"""
1. Change IP (vpn, proxy) PROXY - DONE
2. Change geolocation (DONE)
3. Change MAC Address (DONE)
4. Browser fingerprint

CTR
Traffic consistency
Advertiser conversion rate

Refresh cookies (DONE)
Refresh session (DONE)

"""
import numpy as np
import subprocess as sub
from selenium import webdriver
from bs4 import BeautifulSoup
from proxy_checker import ProxyChecker
from selenium.webdriver.common.keys import Keys
from random_user_agent.user_agent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os, re, time, argparse, json, requests, random, sys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from random_user_agent.params import SoftwareName, OperatingSystem
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def get_user_agent(driver):
    return driver.execute_script("return navigator.userAgent")

def change_user_agent(driver):
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent":"python 2.7", "platform":"Windows"})

def random_user_agent():
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    #list of all user agents
    # user_agents = user_agent_rotator.get_user_agents()
    user_agent = user_agent_rotator.get_random_user_agent()
    return user_agent

# Function to generate a random MAC Address 
def get_random_mac_address(): 
    characters = "0123456789abcdef"
    random_mac_address = "00"
    for _ in range(5): 
        random_mac_address += ":" + random.choice(characters) + random.choice(characters) 
    return random_mac_address 

def change_mac(interface, new_mac):
    if len(new_mac) != 17:
        print('[-] Please enter a valid MAC Address')
        quit()

    print('[+] Changing the MAC Address to', new_mac)
    sub.call(['sudo', 'ifconfig', interface, 'down'])
    sub.call(['sudo', 'ifconfig', interface, 'hw', 'ether', new_mac])
    sub.call(['sudo', 'ifconfig', interface, 'up'])
  
def get_current_mac(interface):
    output = sub.check_output(['ifconfig', interface], universal_newlines = True)
    search_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", output)
    if search_mac:
        return search_mac.group(0)
    else:
        print('[-] Could not read the MAC Address')

def mac_address(interface):
    prev_mac = get_current_mac(interface)
    print('[+] MAC Address before change -> {}'.format(prev_mac))
    new_mac = get_random_mac_address()
    change_mac(interface, new_mac)
    changed_mac = get_current_mac(interface)
    print('[+] MAC Address after change -> {}'.format(changed_mac))
    if changed_mac == new_mac:
        print('[+] MAC Adress was successfully changed from {} to {}'.format(prev_mac, changed_mac))
    else:
        print('[-] Could not change the MAC Address')

def get_geo():
    r = requests.get('http://gimmeproxy.com/api/getProxy?country=US')
    output = json.loads(r.text)
    PROXY = output['ip']
    country = output['country']
    return [PROXY, country]

def random_proxy():
    headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'http://www.wikipedia.org/',
    'Connection': 'keep-alive',
    }
    #Define the IP and Port list
    random_ip, random_port, random_country = [], [], []
    try:
        url = 'https://www.sslproxies.org/'
        r = requests.get(url=url, headers=headers)
    except:
        print('SSL Proxies is either down or there is no Internet')
        quit()
    soup = BeautifulSoup(r.text, 'html.parser')

    # Get the Random IP Address
    for x in soup.findAll('td')[::8]:
        random_ip.append(x.get_text())

     # Get Their Port
    for y in soup.findAll('td')[1::8]:
        random_port.append(y.get_text())
    z = list(zip(random_ip, random_port))

    #Get their country
    for k in soup.findAll('td')[2::8]:
        random_country.append(k.get_text())
    
    # This will Fetch Random IP Address and corresponding PORT Number
    number = random.randint(0, len(z)-50)
    ip_random = z[number]
    country_random = random_country[number]

    # Create a Proxy
    proxy = "{}:{}".format(ip_random[0],ip_random[1])
    return [proxy, country_random]

def get_geo_data():
    target_url = 'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt'
    response = requests.get(target_url)
    data = response.text

    geo_data = []
    for count, line in enumerate(data.split('\n')):
        if count > 8 and count < len(data.split('\n'))-2:
            stripped_line = line.rstrip()
            ip_address = stripped_line.split(" ", 2)[0]
            country = stripped_line.split(" ", 2)[1]
            geo_data.append([ip_address, country])
    random_number = random.randint(0, len(geo_data)-1)
    ip, cntry = geo_data[random_number]
    cntry = cntry[:2]
    return [ip, cntry]

#Responses:
def check_response(proxy):
    proxy_found = False
    counter = 0
    while not proxy_found:
        if proxy == "random_proxy":
            proxy, country = random_proxy()
        elif proxy == "get_geo":
            proxy, country = get_geo()
        else:
            proxy, country = get_geo_data()
        counter += 1
        print("\r" + "[+] Looking for valid IP address: " + str(counter), end="")
        try:
            r = requests.get('https://pinchofyum.com/', proxies={'https': 'https://{}'.format(proxy)}, timeout=8)
            if r.status_code == 200:
                print('\n[+] IP Address used as proxy: ' + proxy)
                proxy_found = True
            else:
                if proxy == "random_proxy":
                    proxy, country = random_proxy()
                elif proxy == "get_geo":
                    proxy, country = get_geo()
                else:
                    proxy, country = get_geo_data()
        except:
            if proxy == "random_proxy":
                proxy, country = random_proxy()
            elif proxy == "get_geo":
                proxy, country = get_geo()
            else:
                proxy, country = get_geo_data()
    return proxy, country

def change_geolocation(driver, country):
    country = country[0:2]

    target_url = 'https://raw.githubusercontent.com/google/dspl/master/samples/google/canonical/countries.csv'
    response = requests.get(target_url)
    data = response.text

    prefix = {}
    for count, line in enumerate(data.split('\n')):
        if count > 0 and count < len(data.split('\n'))-1:
            country_code = line.split(",", 4)[0]
            lat = line.split(",", 4)[1]
            lon = line.split(",", 4)[2]
            country_name = line.split(",", 4)[3]
            prefix[country_code] = [lat, lon, country_name]
    
    latitude = prefix[country][0]
    longitude = prefix[country][1]

    params = {
    "latitude": float(latitude),
    "longitude": float(longitude),
    "accuracy": 100
    }
    print('[+] Geological country: ' + country + ' [Latitude: {}, Longitude: {}]'.format(latitude, longitude))
    driver.execute_cdp_cmd("Page.setGeolocationOverride", params)

def open_url(driver, url):
    driver.get(url)

def get_page_details(driver):
    print('[+] Page title: ' + driver.title)
    print('[+] Origin URL: ' + driver.current_url)

def get_status_code(driver):
    logs = chromedriver.get_log('performance')
    for log in logs:
        if log['message']:
            d = json.loads(log['message'])
            try:
                content_type = 'text/html' in d['message']['params']['response']['headers']['content-type']
                response_received = d['message']['method'] == 'Network.responseReceived'
                if content_type and response_received:
                    status_code = d['message']['params']['response']['status']
                    print('[+] Status code: ' + status_code)
            except:
                pass

def navigation(driver, url):
    driver.get(url)
    driver.back()
    driver.forward()
    driver.refresh()

def scroll_to_element(driver, element):
    window_height = driver.execute_script("return window.innerHeight")
    start_dom_top = driver.execute_script("return document.documentElement.scrollTop")
    element_location = element.location['y']
    desired_dom_top = element_location - window_height/2 #Center It!
    to_go = desired_dom_top - start_dom_top
    cur_dom_top = start_dom_top
    while np.abs(cur_dom_top - desired_dom_top) > 70:
        scroll = np.random.uniform(2,69) * np.sign(to_go)
        driver.execute_script("window.scrollBy(0, {})".format(scroll))
        cur_dom_top = driver.execute_script("return document.documentElement.scrollTop")
        time.sleep(np.abs(np.random.normal(1.22, 0.003)))

def direct_website(driver, url, timeout):
    article_titles = []
    print('[+] Directly opened the blog link')
    try:
        driver.get(url)
        get_page_details(driver)
        get_status_code(driver)
        articles = WebDriverWait(driver,timeout).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "post-title")))
        for article in articles:
            article_titles.append(article.text)

        print('[+] Choosing an article')
        random_link = WebDriverWait(driver,timeout).until(EC.element_to_be_clickable((By.LINK_TEXT, random.choice(article_titles))))
        scroll_to_element(driver, random_link)
        random_link.click()
        next_article = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR , 'div.next a')))
        previous_article = WebDriverWait(driver,timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR , 'div.previous a')))
        choice = random.choice([next_article, previous_article])
        print('[+] Scrolling to the bottom')
        scroll_to_element(driver, choice)
        print('[+] Choosing the next article')
        print('[+] Chose ' + choice.text)
        choice.click()
        print('[+] Scrolling to the bottom')
        bottom_page = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME , 'submit')))
        scroll_to_element(driver, bottom_page)
        time.sleep(5)
        #Cleaning up
        print('[+] Deleting all cookies and closing the browser')
        delete_all_cookies(driver)
        driver.quit()
        print("Done")
    except:
        print('[+] No Internet/Website could not be reached')
        driver.quit()

def direct_blog(driver, url, timeout):
    print('[+] Opening the blog directly')
    try:
        driver.get(url)
        get_page_details(driver)
        get_status_code(driver)
        next_article = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR , 'div.next a')))
        previous_article = WebDriverWait(driver,timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR , 'div.previous a')))
        choice = random.choice([next_article, previous_article])
        print('[+] Scrolling to the bottom')
        scroll_to_element(driver, choice)
        print('[+] Choosing the next article')
        print('[+] Chose ' + choice.text)
        choice.click()
        print('[+] Scrolling to the bottom')
        bottom_page = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME , 'submit')))
        scroll_to_element(driver, bottom_page)
        time.sleep(5)
        #Cleaning up
        print('[+] Deleting all cookies and closing the browser')
        delete_all_cookies(driver)
        driver.quit()
        print("Done")
    except:
        print('[+] No Internet/Website could not be reached') 
        driver.quit()

def delete_all_cache(driver):
    driver.execute_script("window.open('');")
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(2)
    driver.get('chrome://settings/cleardriverData')
    time.sleep(2)
    actions = ActionChains(driver) 
    actions.send_keys(Keys.TAB * 3 + Keys.DOWN * 3) # send right combination
    actions.perform()
    time.sleep(2)
    actions = ActionChains(driver) 
    actions.send_keys(Keys.TAB * 4 + Keys.ENTER) # confirm
    actions.perform()
    time.sleep(5) # wait some time to finish
    driver.quit() # close this tab
    driver.switch_to.window(driver.window_handles[0]) # switch back

def delete_cookie(driver, cookie):
    driver.delete_cookie(cookie)

def delete_all_cookies(driver):
    print('[+] Deleting all cookies...')
    driver.delete_all_cookies()


if __name__ == "__main__":
    #Starting the program
    print("Initializing browser...")

    #Starting URL
    url = 'https://blog.markgacoka.com'
    fb_url = 'https://l.facebook.com/l.php?u=https://blog.markgacoka.com/long-distance-real-estate-investing/?fbclid=IwAR0VHVBMV3aF1drwtV5MxEfXsn1sbVTHkZx5IMjnxZeR6XjDLGheJ-szHJA&h=AT0QiFAY4D3afr96mnIvaCyIGMn0lPWIfKlDINAZY3dhyaoTllhW7Ft9JkxAU3CEDh-5F-VzDvkVYKk--41rCrHCmkTg_rJbyf-G173um3TcbPiVTXwsQXXoTUl0&__tn__=-UK-R&c[0]=AT3dkHJTEhAk6dvzyKBAmctwPCITx_hfBR6x6dQxwfEpzQaS-414FA_tyat6lQrhRBBrXX5AK0K71e_l_nwtXa-dcWBQMDsibH5x8DgTiEAjuQpHUEde4ZbM1H_h7aDMrJNh_ahPIKE8jqIZhnE'
    blog_articles = {
        "How to Purchase an REO Property": "https://blog.markgacoka.com/purchase-reo-property/",
        "How To Make $10,000 A Month With Rental Properties": "https://blog.markgacoka.com/make-money-with-rental-properties/",
        "How To Buy An Apartment Building": "https://blog.markgacoka.com/how-to-buy-an-apartment-building/",
        "How to Style Your Ultimate Outdoor Kitchen": "https://blog.markgacoka.com/style-outdoor-kitchen/",
        "What To Do After Closing a Rental Property": "https://blog.markgacoka.com/closing-a-rental-property/",
        "Home Improvement Ideas": "https://blog.markgacoka.com/home-improvement-ideas/",
        "How To Become A Real Estate Developer": "https://blog.markgacoka.com/become-a-real-estate-developer/",
        "Most affordable neighborhoods in the US": "https://blog.markgacoka.com/affordable-neighborhoods-in-the-us/",
        "Long-Distance Real Estate Investing": "https://blog.markgacoka.com/long-distance-real-estate-investing/",
        "How To Do a Home Makeover": "https://blog.markgacoka.com/home-makeover/"
    }

    #MAC Address, User Agent, Proxy
    mac_address('usb0')
    user_agent = random_user_agent()
    proxy_choice = random.choice(["random_proxy", "get_geo", "get_geo_data"])
    print('[+] Proxy of choice: ' + proxy_choice)
    PROXY, country = check_response(proxy_choice)

    #Set Chromedriver Options
    options = Options()
    # options.add_argument("--headless")
    # options.add_argument("--start-maximized")
    # options.add_argument("--disable-notifications")
    # options.add_argument("--incognito")
    options.add_argument('--no-sandbox')
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
    chromedriver = webdriver.Chrome(options=options, desired_capabilities=capabilities)

    #Confirm User Agent and change geolocation
    print('[+] Session ID: ' + chromedriver.session_id)
    change_geolocation(chromedriver, country)
    agent = get_user_agent(chromedriver)
    print("[+] User Agent in use: ", agent)

    #Get page information and status codes
    #open_url(chromedriver, url)
    raffle = random.randint(0, 1)
    raffle2 = random.randint(0, 1)
    if raffle == 1:
        direct_website(chromedriver, url, 12)
        get_status_code(chromedriver)
    else:
        if raffle2 == 1:
            direct_blog(chromedriver, random.choice(list(blog_articles.values())), 12)
            get_status_code(chromedriver)
        else:
            direct_blog(chromedriver, fb_url, 12)
            get_status_code(chromedriver)