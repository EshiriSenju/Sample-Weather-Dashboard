import requests
import json
import time

def get_weather_data(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        if errh.response.status_code == 404:
            print(f"Weather data fir '{city} not found. Please check the city name.")
        else :
            print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Oops: Something Else", err)

def is_valid_city(city_name):
    return city_name.strip().isalpha()

# variables
api_key = 'a308ca9a98b6f16cd0621897316cbc14'

while True: #infinte loop
    city = input("Enter the city name: ")
    if not is_valid_city(city):
        print("Invalid city name. Please try agin.")
        continue
    for attempt in range(3):
        weather_data = get_weather_data(api_key, city)

        if weather_data:
            print(f"Weather in {city}: {weather_data['weather'][0]['description'].capitalize()}")
            print(f"Temperature: {weather_data['main']['temp']}°C")
            print(f"Humidity: {weather_data['main']['humidity']}%")
        else:
            print("Failed to retrieve weather data")
            time.sleep(5)

            print("Updating in 19 seconds...")
            time.sleep(2)