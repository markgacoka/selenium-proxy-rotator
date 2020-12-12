import requests, random

class Proxy2:
    def __init__(self):
        pass

    def proxy(self):
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