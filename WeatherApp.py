# Author Dominique Grimes
# Date 6/4/2022

import requests


# Obtain latitude and longitude coordinates through API based on either city/state or zipcode lookup.
# Account for data entry and connection exceptions. Return variables lat, lon.


def get_lat_lon():
    while True:
        location = input('\nPlease select your preferred search method. Enter 1 for city or 2 for zip code lookup.')
        if location == '1':
            city = input('Please enter the city:')
            state = input('Please enter the 2 letter state abbreviation:')
            url = f'http://api.openweathermap.org/geo/1.0/direct?q={city},{state}' \
                  f'US&appid=1232693f72c4af47b775be7e28b23406'
            try:
                response_test = requests.get(url)
                response_test.raise_for_status()
                # print(response_test.request.url)
            except requests.exceptions.HTTPError as err:
                print('A connection error has occurred.')
                print('The following exception has been raised: ', err)
            except requests.exceptions.ConnectionError as err:
                print('A connection error has occurred.')
                print('The following exception has been raised: ', err)
            else:
                while True:
                    try:
                        response_city = requests.get(url).json()
                        lat = response_city[0]['lat']
                        lon = response_city[0]['lon']
                        return lat, lon
                    except IndexError:
                        print('\nUnable to find this location. Please try again.')
                        print('You entered ', city, state)
                        break
        elif location == '2':
            ask_zip = input('Please enter the 5 digit zip code:')
            url = f'http://api.openweathermap.org/geo/1.0/zip?zip={ask_zip},' \
                  f'US&appid=1232693f72c4af47b775be7e28b23406'
            try:
                response_test = requests.get(url)
                response_test.raise_for_status()
                # print(response_test.request.url)
            except requests.exceptions.HTTPError as err:
                print('A connection error has occurred.')
                print('The following exception has been raised: ', err)
            except requests.exceptions.ConnectionError as err:
                print('A connection error has occurred.')
                print('The following exception has been raised: ', err)
            else:
                while True:
                    try:
                        response_zip = requests.get(url).json()
                        lat = response_zip['lat']
                        lon = response_zip['lon']
                        return lat, lon
                    except IndexError:
                        print('\nUnable to find this location. Please try again.')
                        print('You entered ', zip)
        else:
            print('\nEntry error. Please try again')
            print('You entered ', location)


# Ask for desired temperature method and update API accordingly based on selection.
# Account for data entry error. Return temp_url and output variables.


def set_temp_method(lat, lon):
    temp_method = input('Please select your temperature output method. '
                        'Enter F for Fahrenheit, C for Celsius, or K for Kelvin:')
    while True:
        if temp_method.upper() == 'F':
            output = '\N{DEGREE SIGN}F'
            temp_url = f'https://api.openweathermap.org/data/2.5/weather?' \
                       f'lat={lat}&lon={lon}&appid=1232693f72c4af47b775be7e28b23406&units=imperial'
            break
        elif temp_method.upper() == 'C':
            output = '\N{DEGREE SIGN}C'
            temp_url = f'https://api.openweathermap.org/data/2.5/weather?' \
                       f'lat={lat}&lon={lon}&appid=1232693f72c4af47b775be7e28b23406&units=metric'
            break
        elif temp_method.upper() == 'K':
            output = 'kelvins'
            temp_url = f'https://api.openweathermap.org/data/2.5/weather?' \
                       f'lat={lat}&lon={lon}&appid=1232693f72c4af47b775be7e28b23406'
            break
        else:
            print('You entered', temp_method)
            print('Invalid Entry. Try again.')
            temp_method = input('Please select your temperature output method. '
                                'Enter F for Fahrenheit, C for Celsius, or K for Kelvin:')
    return temp_url, output


# Request API. Return response variable.


def get_weather(url):
    response = requests.get(url).json()
    return response


# Parse JSON and print weather data.


def pretty_print(response_temp, output):
    temp = response_temp['main']['temp']
    pressure = response_temp['main']['pressure']
    humidity = response_temp['main']['humidity']
    clouds = response_temp['clouds']['all']
    max_temp = response_temp['main']['temp_max']
    min_temp = response_temp['main']['temp_min']

    print('\nCurrent Weather Conditions for', response_temp['name'], ':')
    print('Current Temp:', temp, output)
    print('High Temp:', max_temp, output)
    print('Low Temp:', min_temp, output)
    print('Pressure:', pressure, 'hPa')
    print('Humidity:', humidity, '%')
    print('Cloud Cover:', clouds, '%')


# Ask user if they need to look up weather for another location or end the program. Return the variable repeat.
# Account for input error.


def ask_repeat_lookup():
    while True:
        repeat = input('Would you like to look up the weather for another location? (Enter Y/N)')
        if repeat.upper() == 'Y' or repeat.upper() == 'N':
            break
        else:
            print('You entered:', repeat)
            print('Invalid entry. Try again.')
    return repeat


# Start with welcome message. Obtain lat, lon from user by either city/state or zip by using API.
# Ask for preferred temperature output. Pass lat, lon through weather look up API. Print results.
# Ask the user if they'd like to look up another location or quit the program.


def main():
    print('\nWelcome to your current weather lookup!')
    while True:
        lat, lon = get_lat_lon()
        temp_url, output = set_temp_method(lat, lon)
        response = get_weather(temp_url)
        pretty_print(response, output)
        repeat = ask_repeat_lookup()
        if repeat.upper() == 'N':
            break
    print('\nThank you for using the weather lookup application. See you next time!')


if __name__ == '__main__':
    main()
