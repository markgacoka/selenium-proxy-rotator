import requests, random
from bs4 import BeautifulSoup

class Proxy1:
    def __init__(self):
        pass

    def proxy(self):
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