# Warning: If you know coding do not read this code.
# What you will see cannot be unseen.
# You have been warned.

import sqlite3
import math
import requests
import json

def find_journey_time(lat_1, lon_1, lat_2, lon_2, vehicle="car"):
    r = requests.get(f"http://router.project-osrm.org/route/v1/{vehicle}/{lon_1},{lat_1};{lon_2},{lat_2}?overview=false")
    routes = json.loads(r.content)
    return routes.get("routes")[0]["duration"]

def get_cursor():
    con = sqlite3.connect("db_v1.db")
    return con.cursor()

def get_vehicle_from_prefs(preferences):
    if "walk_mode" in preferences:
        return "foot"

    return "car"

def clip(value, lower, upper):
    return lower if value < lower else upper if value > upper else value

def get_time_score(time, vehicle):
    if vehicle == "car":
        max_time = 1*60*60
    else:
        max_time = 2*60*60
    return clip((max_time - time)/max_time, 0, 1)

def go_hospital_visit(request_text, preferences, location):
    cur = get_cursor()
    hospitals = cur.execute("SELECT * FROM medical_points")

    vehicle = get_vehicle_from_prefs(preferences)
    print(f"vehicle: {vehicle}")

    # 0.5 Distance, 0.5 how full it is.
    # For driving 2h is 0 for time, for walking 3h is 0 for time, 0h is 1
    scores = []
    entries = []
    longitudes = []
    latitudes = []
    for hospital in hospitals:
        print(f"hospital: {hospital}")
        time = find_journey_time(location.latitude, location.longitude, hospital[1], hospital[2], vehicle)
        time_score = get_time_score(time, vehicle)
        print(f"time: {time}, time_score: {time_score}")

        fullness = hospital[3] / hospital[4]
        fullness_score = 1 - fullness
        print(f"fulness: {fullness}, fullness_score: {fullness_score}")

        score = 0.5 * fullness_score + 0.5 * time_score
        print(f"score: {score}")
        scores.append(score)

        entry = {
            "title": hospital[6],
            "description": hospital[5],
            "footnotes": f"time to hospital {(time/60):.2f} min, hospital is {(fullness*100):.2f}% full"
        }
        entries.append(entry)

    _, entries = zip(*sorted(zip(scores, entries), reverse=True))

    # Sort entries by score and return.
    return entries

def fun_music(request_text, preferences, location):
    return [{
            "title": "Awesome music!",
            "description": "https://www.youtube.com/watch?v=EOxKo3Nn7Ps",
            "footnotes": ""}]

def find_zaklin(request_text, preferences, location):
    return [{
            "title": "Łódzki Ogród Zoologiczny",
            "description": "",
            "footnotes": ""}]

def _process_food_request(preferences, location, only_icecream, student_party_mode):
    cur = get_cursor()
    restaurants = cur.execute("SELECT * FROM restaurants")
    vehicle = get_vehicle_from_prefs(preferences)

    scores = []
    entries = []

    # Score weights here are 0.2 time score, 0.2 grade from google, 0.2 eating places
    # if I want few people is enabled fulness weight is increased to 1.0 for influence.
    for restaurant in restaurants:
        if only_icecream:
            if restaurant[7] != "ice shop":
                continue

        if student_party_mode:
            if restaurant[7] != "pub":
                continue

        time = find_journey_time(location.latitude, location.longitude, restaurant[1], restaurant[2], vehicle)
        time_score = get_time_score(time, vehicle)
        print(f"time: {time}, time_score: {time_score}")

        # Inconsistency in data whyyyyyyyyyyyyyy ):
        fullness = restaurant[4] / (restaurant[3] + restaurant[4])
        fullness_score = 1. - fullness

        rating_score = restaurant[5] / 5.
        print(f"fulness: {fullness}, fullness_score: {fullness_score}")
        print(f"rating score: {rating_score}")

        if "prefer_few_people" in preferences:
            # MAX so we see result xdddd
            score = time_score*0.2 + rating_score*0.2 + fullness_score*1.0
        else:
            score = time_score*0.2 + rating_score*0.2 + fullness_score*0.2

        print(f"score: {score}")
        scores.append(score)

        rating = restaurant[5]
        entry = {
            "title": restaurant[6],
            "description": "type: " + restaurant[7] + f", raiting: {rating:.2f}/5",
            "footnotes": f"eta: {(time / 60):.2f} min, restaurant is {(fullness*100):.2f}% full"
        }
        entries.append(entry)

    _, entries = zip(*sorted(zip(scores, entries), reverse=True))

    return entries

def eat(request_text, preferences, location):
    return _process_food_request(preferences, location, False, False)

def eat_ice_cream(request_text, preferences, location):
    return _process_food_request(preferences, location, True, False)

# WHYYYYYYY do we have so many tables with so many column arrangements?!!!!
def shop(request_text, preferences, location):
    cur = get_cursor()
    shops = cur.execute("SELECT * FROM shops")
    vehicle = get_vehicle_from_prefs(preferences)

    scores = []
    entries = []

    for shop in shops:
        time = find_journey_time(location.latitude, location.longitude, shop[1], shop[2], vehicle)
        time_score = get_time_score(time, vehicle)
        print(f"time: {time}, time_score: {time_score}")

        fullness = shop[4] / (shop[3] + shop[4])
        fullness_score = 1. - fullness

        rating_score = shop[5] / 5.
        print(f"fullness: {fullness}, fullness_score: {fullness_score}")
        print(f"rating score: {rating_score}")

        if "prefer_few_people" in preferences:
            score = time_score*0.2 + rating_score*0.2 + fullness_score*1.0
        else:
            score = time_score*0.2 + rating_score*0.2 + fullness_score*0.2

        print(f"score: {score}")
        scores.append(score)

        rating = shop[5]
        entry = {
            "title": shop[6],
            "description": "type: " + shop[7] + f", raiting: {rating:.2f}/5",
            "footnotes": f"eta: {(time / 60):.2f} min, shop is {(fullness*100):.2f}% full"
        }
        entries.append(entry)

    _, entries = zip(*sorted(zip(scores, entries), reverse=True))

    return entries

def get_distance(p, q):
    """
    Return euclidean distance between points p and q
    assuming both to have the same number of dimensions
    """
    # sum of squared difference between coordinates
    s_sq_difference = 0
    for p_i,q_i in zip(p,q):
        s_sq_difference += (p_i - q_i)**2

    # take sq root of sum of squared difference
    distance = s_sq_difference**0.5
    return distance

# Whyyyyy I am doing this to myself, oh god why
# It's almost 12pm second night, I swear I will delete this garbage if I see one more runtime error.
def _process_walking(preferences, location, parks):
    cur = get_cursor()
    points = cur.execute("SELECT * FROM recraation")
    vehicle = get_vehicle_from_prefs(preferences)

    scores = []
    entries = []

    for point in points:
        if parks:
            if point[3] != "park":
                continue

        time = find_journey_time(location.latitude, location.longitude, point[1], point[2], vehicle)
        time_score = get_time_score(time, vehicle)
        print(f"time: {time}, time_score: {time_score}")

        rating_score = point[4] / 5.

        print(f"rating score: {rating_score}")

        # Get data from nearest air quality monitor
        cur2 = get_cursor()
        monitors = cur2.execute("SELECT * FROM air_quality")
        closest_distance = 100000000 # XD
        for monitor in monitors:
            d = get_distance([point[1], point[2]], [monitor[1], monitor[2]])
            if closest_distance > d:
                closest_distance = d
                quality = monitor[3]
                noise_level = monitor[4]

        if "prefer_quiet" in preferences:
            quiet_weight = 0.5
        else:
            quiet_weight = 0

        if "prefer_clean_air" in preferences:
            clean_air_weight = 0.5
        else:
            clean_air_weight = 0

        quiet_score = 1 - noise_level/100.0
        quality_score = quality/100.0

        score = time_score*0.2 + rating_score*0.2 + quiet_score*quiet_weight + quality_score*clean_air_weight
        print(f"quiet score: {quiet_score}, quality_score: {quality_score}")

        print(f"score: {score}")
        scores.append(score)

        rating = point[4]
        entry = {
            "title": point[5],
            "description": "type: " + point[3] + f", raiting: {rating:.2f}/5, air quality: {(quality_score*100):.2f}%, quiet: {(quiet_score*100):.2f}%",
            "footnotes": f"eta: {(time / 60):.2f} min,"
        }
        entries.append(entry)

    _, entries = zip(*sorted(zip(scores, entries), reverse=True))

    return entries

def walk_city(request_text, preferences, location):
    return _process_walking(preferences, location, False)

# I'm getting burried under everest of technical debt ):
def walk_park(request_text, preferences, location):
    return _process_walking(preferences, location, True)

def get_drunk(request_text, preferences, location):
    return _process_food_request(preferences, location, False, True)

# aaaaaaaaaaaaaaaaaa ):
