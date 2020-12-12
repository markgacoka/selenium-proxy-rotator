import requests, json

class Proxy3:
    def __init__(self):
        pass

    def proxy(self):
        r = requests.get('http://gimmeproxy.com/api/getProxy?country=US')
        output = json.loads(r.text)
        PROXY = output['ip']
        country = output['country']
        return [PROXY, country]