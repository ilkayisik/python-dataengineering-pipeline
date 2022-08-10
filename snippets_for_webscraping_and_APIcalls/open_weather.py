#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 16:06:55 2022
@author: ilkayisik
"""
import requests
import json
import pandas as pd

api_key = ''  # replace with your API key
url = "http://api.openweathermap.org/data/2.5/forecast?q={}&appid={}&units=metric".format(
    'Frankfurt', api_key)
# use lat and long rather than city name:
lat, lon = "50.110924", "8.682127"  # frankfurt
url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (
    lat, lon, api_key)


response = requests.get(url)
data = json.loads(response.text)
print("Open weather:", response.status_code)
print(data)
