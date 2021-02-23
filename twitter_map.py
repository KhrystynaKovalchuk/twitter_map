import requests
import json
import folium
from geopy.geocoders import Nominatim


def get_information(name, token):

    base_url = 'https://api.twitter.com/'

    bearer_token = token

    search_url = '{}1.1/friends/list.json'.format(base_url)

    search_headers = {
        'Authorization': 'Bearer {}'.format(bearer_token)
    }

    search_params = {
        'screen_name': '@' + name,
        'count': 28
    }

    response = requests.get(search_url, headers=search_headers, params=search_params)

    json_response = response.json()
    return json_response

def write_to_file(name_1, token_1):
    """
    Function for writing data to .json file.
    """
    inf = get_information(name_1, token_1)
    with open("friends.json", "w") as file:
        return json.dump(inf, file, indent=4)


def get_data(file):
    file_1 = open(file, "r", encoding="utf-8")
    data = json.load(file_1)['users']
    information = []
    for dictionary in data:
        name = dictionary['screen_name']
        location = dictionary['location']
        information.append([name, location])
    return information


def find_coordinates(file):
    geolocator = Nominatim(user_agent="Maps")
    names_locations = get_data(file)
    for lst in names_locations:
        try:
            location = geolocator.geocode(lst[-1])
            coordinates = [location.latitude, location.longitude]
            del lst[-1]
            lst.append(coordinates)
        except AttributeError:
            continue
    return names_locations


def change_map(file):
    your_map = folium.Map([45,45], zoom_start=3)
    locations_names = find_coordinates(file)
    for lst in locations_names:
        try:
            try:
                folium.Marker([lst[1][0], lst[1][1]], popup=lst[0], icon=folium.Icon(color="blue")).add_to(your_map)
            except ValueError:
                continue
        except IndexError:
            continue
    return your_map
