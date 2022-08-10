import pandas as pd
from datetime import datetime, timedelta
import requests

def lambda_handler(event, context):
    
    # connection to my RDS instance
    schema="gans_02"
    host="wbs-project3-db.c2btp8jeti51.eu-central-1.rds.amazonaws.com"
    user="admin"
    password="your_pw"
    port=3306
    con = f'mysql+pymysql://{user}:{password}@{host}:{port}/{schema}'
    
    
    # Collect flight arrival info using aerodatabox API
    to_local_time = datetime.now().strftime('%Y-%m-%dT%H:00')
    from_local_time = (datetime.now() + timedelta(hours=9)).strftime('%Y-%m-%dT%H:00')

    querystring = {"withLeg":"true","withCancelled":"true","withCodeshared":"true",
                   "withCargo":"true","withPrivate":"false","withLocation":"false"}

    headers = {
        'x-rapidapi-host': "aerodatabox.p.rapidapi.com",
        'x-rapidapi-key': 'your_key'
        }
    
    # this line is very important!!!
    # it loads the icao info from the database and turns it into a list to use 
    # in the forloop. For now I am only using 2 airports
    city_icao_list = pd.read_sql('SELECT icao FROM airports', con)[0:2]['icao'].to_list()
    
    arrival_df_list = []
    
    for icao_code in city_icao_list:
        print(icao_code)
    
        url = f"https://aerodatabox.p.rapidapi.com/flights/airports/icao/{icao_code}/{to_local_time}/{from_local_time}"
        response = requests.request("GET", url, headers=headers, params=querystring)
    
        try:
            arrival_df = pd.json_normalize(response.json()['arrivals'])
            print(arrival_df.columns)
            filtered_df = arrival_df.filter(['departure.airport.name',
                                             'departure.airport.icao',
                                             'arrival.scheduledTimeLocal',
                                             'status', 'airline.name'])
            print(filtered_df.columns)
            filtered_df['arr_airport_icao'] = icao_code
    
            filtered_df.rename(columns={'departure.airport.name': 'dep_airport',
                                        'arrival.scheduledTimeLocal': 'arr_sched_loc_time',
                                        'departure.airport.icao': 'dep_airport_icao',
                                        'status': 'status',
                                        'airline.name': 'airline',
                                        'arr_airport_icao': 'arr_airport_icao'
                                        }, inplace=True)
    
        except:
            pass
        arrival_df_list.append(filtered_df)

    # concat the dataframes in the list:
    arrivals_df = pd.concat(arrival_df_list, axis=0, ignore_index=False)
    
    
    # Weather info
    # weather_city_list = np.unique(pd.read_sql('SELECT municipalityName FROM airports', con)['municipalityName'].to_list()) # to select all cities use this line
    weather_city_list = pd.read_sql('SELECT municipalityName FROM airports', con)['municipalityName'].to_list()[0:1] # to select only the first city
    weather_df_list = []
    for ind, city in enumerate(weather_city_list):
        country = pd.read_sql('SELECT * FROM airports', con)['countryCode'].iloc[ind]
        print(city, country)

        OWM_key = 'your_omw_key'
        response = requests.get(f'http://api.openweathermap.org/data/2.5/forecast/?q={city},{country}&appid={OWM_key}&units=metric&lang=en')
    
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
            except: weather_hour['prob_perc'] = 0
            # rain
            try:
                weather_hour['rain_qty'] = float(forecast_3h['rain']['3h'])
            except: weather_hour['rain_qty'] = 0
            # wind
            try:
                weather_hour['snow'] = float(forecast_3h['snow']['3h'])
            except: weather_hour['snow'] = 0
            weather_hour['municipality'] = city
            weather_hour['country'] = country
            weather_hour['municipality_iso_country'] = city + ',' + country
            weather_info.append(weather_hour)

        weather_data = pd.DataFrame(weather_info)
        weather_df_list.append(weather_data)
    # concat the dataframes in the list:
    weather_df = pd.concat(weather_df_list, axis=0, ignore_index=False)
    

    # update the arrival df
    (
    arrivals_df
    .dropna()
    .to_sql('arrivals', con=con, if_exists='append', index=False)
    )
    
    # update the weather df
    (
    weather_df
    # .dropna()
    .to_sql('weather', con=con, if_exists='append', index=False)
    )
    
    return city_icao_list