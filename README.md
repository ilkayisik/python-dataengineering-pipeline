# Creation of an automated data engineering pipeline on the cloud.

👋 Welcome! 

In this repository you can find my code to create an automated data pipeline on the cloud using Python, SQL and AWS.
(This project is a part of the [DataScience Bootcamp](https://www.wbscodingschool.com/data-science-bootcamp/) at WBS Coding School)

In this hypothetical project I am hired as a data scientist by an e-scooter-sharing company called gans and the goal is to assemble a data pipeline which is capable of collecting the data that is needed to predict e-scooter movement from external sources in an automated way.


## What did I do?

- I collected city information with web scraping and HTML parsing (using the Python library Beautiful Soup)

- I collected weather [OpenWeather]((https://openweathermap.org/api)) and flight information [Aerodatabox]((https://rapidapi.com/aedbx-aedbx/api/aerodatabox/)) by making requests to Application Programming Interfaces (APIs) using Python's requests library.

- I created a SQL database to store the data (MySQL Workbench)

- Transferred the project to the cloud and scheduled to run periodically (AWS, RDS, Lambda, EventBridge).


## The contents of the repository:

1. In [snippets_for_webscraping_and_APIcalls](https://github.com/ilkayisik/python-dataengineering-pipeline/tree/main/snippets_for_webscraping_and_APIcalls) you can find some examples of how to make API requests using Open weather map and Spotipy (You will need to add your own credentials)

2. [version_01](https://github.com/ilkayisik/python-dataengineering-pipeline/tree/main/version_01) and [version_02](https://github.com/ilkayisik/python-dataengineering-pipeline/tree/main/version_02) are very similar except in version_01 city and airport data are loaded from the .csv files and the code is structured to run only for one city. Whereas in version_02 city and airport data are collected with webscraping (city data from wikipedia) and API calls (airport icao codes with aerodata box).

3. For both version the main scripts are the notebooks called gans_main_script.ipynb.

You can refer to this [Medium article](https://medium.com/@ilkayisik/building-a-fully-automated-data-pipeline-with-python-mysql-and-aws-cb692b218b60) for a more detailed description of the project and the code. 

