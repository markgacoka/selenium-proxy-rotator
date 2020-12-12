import requests

class Geolocation:
    def __init__(self):
        pass

    def change_geolocation(self, driver, country):
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