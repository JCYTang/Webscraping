import json
import requests
import csv
import time

url = 'https://maps.google.com/maps/api/geocode/json'
key = 'AIzaSyDGbEiw-NI4mojpJr-0QCVfLeRt4SRtJsY'
parameters = {}
response = requests.get(url, params=parameters)
parameters['key'] = key

# only get result if address_components type is a postal_code
with open('postcodes.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    next(reader)
    for row in reader:
        code = row[0]
        suburb = row[1]
        state = row[2]
        parameters['address'] = suburb.replace(' ', '+') + ',+' + state + '+' + code + ',+Australia'
        time.sleep(0.1)
        response = requests.get(url, params = parameters)
        geodata = response.json()
        print(geodata)
        if geodata['status'] != 'ZERO_RESULTS':
            # if geodata['results'][0]['address_components'][0]['types'][0] == 'postal_code':
            ne_lat = geodata['results'][0]['geometry']['viewport']['northeast']['lat']
            ne_lng = geodata['results'][0]['geometry']['viewport']['northeast']['lng']
            sw_lat = geodata['results'][0]['geometry']['viewport']['southwest']['lat']
            sw_lng = geodata['results'][0]['geometry']['viewport']['southwest']['lng']
            print(code, suburb, state, ne_lat, ne_lng, sw_lat, sw_lng)
            with open('postcodes_latlng.csv', 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([code, suburb, state, ne_lat, ne_lng, sw_lat, sw_lng])