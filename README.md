# Selenium proxy-rotator
A python wrapper around selenium that makes web automation anonymous through elite proxy rotation.

## Features
- Supports incognito
- Random MAC address
- Random user agent
- Rotating proxy support for IP change
- Browser geolocation rotation (matches IP from proxy)

## How it works
The algorithm changes the MAC address of your computer. It then initializes the random user agent and proxy IP which is scraped from 3 different elite proxy sources. A Selenium webdriver session is then started where you can automate your web scraping or surfing anonymously.

## Instructions
- If you get an error based on the interface, type `ifconfig` or `ipconfig` on cli and change the value.

### Chromedriver 
- Chromium version: 87.0.4280.88
- Tested on Ubuntu 20.04 (Focal Fossa)

## TODO
- [ ] Scrape elite proxies.
- [ ] Add debug mode for issue handling.
- [ ] Confirm proxies work.
- [x] Proxy rotation for IP change.
- [ ] Geological location change in relation to IP address.
- [ ] Refreshing cookies and chache 
- [ ] Add config file for entering the interface name and browser size.
- [ ] Server/continent proxy location support

Thank you for checking out this repo! 

If you found this helpful, feel free to star my work and tell me some of the creative applications you came up with. However, be minful of where and how you scrape. Make sure to stay within the confines of the law to not piss people off!