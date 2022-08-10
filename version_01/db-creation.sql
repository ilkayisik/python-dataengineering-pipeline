DROP DATABASE gans;
CREATE DATABASE IF NOT EXISTS gans; 
USE gans;

DROP TABLE IF EXISTS cities;
CREATE TABLE IF NOT EXISTS cities (
    city VARCHAR(200),
    mayor TEXT,
    city_size TEXT, 
    elevation TEXT, 
    city_population TEXT, 
    urban_population TEXT, 
    metro_population TEXT, 
    latitude TEXT, 
    longitude TEXT, 
	municipality_iso_country varchar(200),
    PRIMARY KEY(municipality_iso_country)
); 

DROP TABLE IF EXISTS airports;
CREATE TABLE IF NOT EXISTS airports(
	name text, 
    latitude_deg float, 
    longitude_deg float, 
    iso_country varchar(10), 
    iso_region varchar(10),
    municipality text, 
    icao_code varchar(4), 
    iata_code varchar(6), 
    municipality_iso_country varchar(200),
    primary key(icao_code)
    -- foreign key (municipality_iso_country) references cities(municipality_iso_country)
);


DROP TABLE IF EXISTS weather; 
CREATE TABLE IF NOT EXISTS weather (
	weather_id int auto_increment, 
    datetime datetime, 
    temperature float, 
    wind float, 
    prob_perc float, 
    rain_qty float, 
    snow integer, 
    municipality_iso_country varchar(200),
    primary key(weather_id),
    foreign key (municipality_iso_country) references cities(municipality_iso_country)
);

DROP TABLE IF EXISTS arrivals; 
CREATE TABLE IF NOT EXISTS arrivals(
	arrivals_id int auto_increment, 
    dep_airport text, 
    sched_arr_loc_time datetime, 
    terminal text, 
    status text, 
	aircraft text, 
    icao_code varchar(4),
    primary key (arrivals_id)
    -- foreign key (icao_code) references airports(icao_code)
);


USE gans;
SELECT * FROM arrivals;
SELECT * FROM weather;
SELECT * FROM cities;
SELECT * FROM airports;
