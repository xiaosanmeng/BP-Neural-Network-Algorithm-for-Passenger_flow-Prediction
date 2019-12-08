import requests
# import cfscrape
from bs4 import BeautifulSoup as bs
import time

# python
import json, urllib
from urllib.parse import urlencode


class GetWeather():
    def get_weather(self, date, hour):
        url = 'http://api.k780.com'
        date = date[:4] + '-' + date[4:6] + '-' + date[6:]
        hour = int(hour)
        params = {
            'app': 'weather.history',
            'weaid': '46',
            'date': date,
            'appkey': '47217',
            'sign': 'eeadab9968ff07302f40f6fc852423d9',
            'format': 'json',
        }
        params = urlencode(params)

        f = urllib.request.urlopen('%s?%s' % (url, params))
        nowapi_call = f.read()
        # print content
        a_result = json.loads(nowapi_call)
        if a_result:
            if a_result['success'] != '0':
                # change a_result to dict {datehour: {t: , hum: , weather:' ', wind:'', }}
                last_hour = None
                for hweather in a_result['result']:
                    last_hour = hweather
                    uptime = int(hweather['uptime'][11:13])
                    if uptime >= hour:
                        weather = {}
                        weather['t'] = hweather['temperature']
                        weather['hum'] = hweather['humidity']
                        weather['wind'] = hweather['winp']
                        weather['weather'] = hweather['weather']
                        return weather
                # if hour=23 and only measure to 22 this day:
                weather = {}
                weather['t'] = last_hour['temperature']
                weather['hum'] = last_hour['humidity']
                weather['wind'] = last_hour['winp']
                weather['weather'] = last_hour['weather']
                return weather
            else:
                print(a_result['msgid'] + ' ' + a_result['msg'])
        else:
            print('Request nowapi fail.')

# Test:
# cla = GetWeather()
# print(cla.get_weather('20180101', 17))
