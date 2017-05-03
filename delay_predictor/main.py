import pandas as pd
from math import sin, cos, sqrt, atan2, radians
import operator
from collections import OrderedDict
from delay_predictor import predictor
from os import path

airlines_csv = None
airlines_codes_csv = None
merged_csv = None


def init():
    global airlines_csv, merged_csv, airlines_codes_csv
    airlines_csv = pd.read_csv(path.abspath(path.join(__file__, '../../data/airline.csv')))
    merged_csv = pd.read_csv(path.abspath(path.join(__file__, '../../data/airportCodes.csv')))
    # df1 = pd.read_csv(path.abspath(path.join(__file__, '../../data/flightsWithAirportCode.csv')))
    # df2 = pd.read_csv(path.abspath(path.join(__file__, '../../data/flightsWithAirportCode1.csv')))
    # df3 = pd.read_csv(path.abspath(path.join(__file__, '../../data/flightsWithAirportCode2.csv')))
    # df4 = pd.read_csv(path.abspath(path.join(__file__, '../../data/flightsWithAirportCode3.csv')))
    # df5 = pd.read_csv(path.abspath(path.join(__file__, '../../data/flightsWithAirportCode4.csv')))
    # frames = [df1, df2, df3, df4, df5]
    # merged_csv = pd.concat(frames)
    # airlines_codes_csv = pd.read_csv(path.abspath(path.join(__file__, '../../data/airlines_codes.csv')))


def _get_distance(lat1, lon1, lat2, lon2):
    r = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return r * c


def _get_closest_airports(lat, lon, amount):
    global airlines_csv
    airports = OrderedDict()

    for i in range(0, len(airlines_csv)):
        lat2 = airlines_csv['lat'][i]
        lon2 = airlines_csv['lon'][i]
        airports[airlines_csv['airport'][i]] = _get_distance(lat, lon, lat2, lon2)

    sorted_airports = sorted(airports.items(), key=operator.itemgetter(1))
    return sorted_airports[0:amount]


def predict(data):
    global merged_csv
    result = {
        "departure": [],
        "arrival": [],
        "suggestion": {}
    }

    dep_airports = _get_closest_airports(data['departure']['lat'], data['departure']['lon'], 3)
    arr_airports = _get_closest_airports(data['arrival']['lat'], data['arrival']['lon'], 3)

    for airport in dep_airports:
        result['departure'].append({
            "airport": airport[0],
            "delay": int((predictor.predict(merged_csv, _get_airport_code(airport))[0]-56) * 100),
            "distance": '...'
        })
    for airport in arr_airports:
        result['arrival'].append({
            "airport": airport[0],
            "delay": int((predictor.predict(merged_csv, _get_airport_code(airport))[0]-56) * 100),
            "distance": '...'
        })
    result['suggestion'] = {
        "from": "_from_",
        "to": "_to_",
        "delay": {
            "departure": "_dep_delay_",
            "arrival": "_arr_delay_"
        }
    }

    print(result)
    return result


def _get_airport_code(airport_string):
    global airlines_csv
    result = airlines_csv.loc[airlines_csv['airport'] == airport_string[0]]
    print(result)
    return result['airport_code']


def _get_suggestion(results):
    pass


if __name__ == '__main__':
    init()
    print('init finished')
    _get_closest_airports(52.2296756, 21.0122287, 3)
