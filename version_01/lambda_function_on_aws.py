import pandas as pd
import numpy as np
import requests
# from my_module import get_flight_info


def get_flight_info(flight_json, airport_icoa):
    """
    This function helps to structure json data gathared from flights api
    """
    # terminal
    try:
        terminal = flight_json['arrival']['terminal']
    except:
        terminal = None
    # aircraft
    try:
        aircraft = flight_json['aircraft']['model']
    except:
        aircraft = None
    return {
        'dep_airport': flight_json['departure']['airport']['name'],
        'sched_arr_loc_time': flight_json['arrival']['scheduledTimeLocal'],
        'terminal': terminal,
        'status': flight_json['status'],
        'aircraft': aircraft,
        'icao_code': airport_icoa
    }


def lambda_handler(event, context):

    from datetime import datetime, timedelta

    airport_icoa = "EDDB"
    to_local_time = datetime.now().strftime('%Y-%m-%dT%H:00')
    from_local_time = (datetime.now() + timedelta(hours=9)).strftime('%Y-%m-%dT%H:00')
    
    flight_api_key = "your_flight_api_key"

    url = f"https://aerodatabox.p.rapidapi.com/flights/airports/icao/{airport_icoa}/{to_local_time}/{from_local_time}"
    querystring = {"withLeg": "true", "withCancelled": "true", "withCodeshared": "true",
                   "withCargo": "true", "withPrivate": "false", "withLocation": "false"}
    headers = {
        'x-rapidapi-host': "aerodatabox.p.rapidapi.com",
        'x-rapidapi-key': flight_api_key
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    arrivals_berlin = response.json()['arrivals']
    arrivals_berlin = pd.DataFrame([get_flight_info(flight, airport_icoa)
                                   for flight in arrivals_berlin])

    # Weather api
    city = "Berlin"
    country = "DE"
    OWM_key = "your_openweathermap_key"
    response = requests.get(
        f'http://api.openweathermap.org/data/2.5/forecast/?q={city},{country}&appid={OWM_key}&units=metric&lang=en')
    forecast_api = response.json()['list']
    weather_info = []
    for forecast_3h in forecast_api:
        weather_hour = {}
        # datetime utc
        weather_hour['datetime'] = forecast_3h['dt_txt']
        # temperature
        weather_hour['temperature'] = forecast_3h['main']['temp']
        # wind
        weather_hour['wind'] = forecast_3h['wind']['speed']
        # probability precipitation
        try:
            weather_hour['prob_perc'] = float(forecast_3h['pop'])
        except:
            weather_hour['prob_perc'] = 0
        # rain
        try:
            weather_hour['rain_qty'] = float(forecast_3h['rain']['3h'])
        except:
            weather_hour['rain_qty'] = 0
        # wind
        try:
            weather_hour['snow'] = float(forecast_3h['snow']['3h'])
        except:
            weather_hour['snow'] = 0
        weather_hour['municipality_iso_country'] = city + ',' + country
        weather_info.append(weather_hour)
    weather_data = pd.DataFrame(weather_info)

    # inserting data in our RDS
    schema = "gans"
    host = ""
    user = "admin"
    password = "your_pw"
    port = 3306
    con = f'mysql+pymysql://{user}:{password}@{host}:{port}/{schema}'

    # flight arrivals data
    (arrivals_berlin
        .replace({np.nan}, 'unknown')
        .assign(sched_arr_loc_time=lambda x: pd.to_datetime(x['sched_arr_loc_time']))
        .to_sql('arrivals', if_exists='append', con=con, index=False))

    # weather data
    (weather_data
        .assign(datetime=lambda x: pd.to_datetime(x['datetime']))
        .to_sql('weather', if_exists='append', con=con, index=False))

    return response.status_code
