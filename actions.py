import sqlite3
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
        latitudes.append(hospital[1])
        longitudes.append(hospital[2])

        time = find_journey_time(location.latitude, location.longitude, hospital[1], hospital[2], vehicle)
        if vehicle == "car":
            max_time = 1*60*60
        else:
            max_time = 2*60*60
        time_score = clip((max_time - time)/max_time, 0, 1)
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
            "footnotes": f"time to hospital {time/60} min, hospital is {fullness*100}% full"
        }
        entries.append(entry)

    _, entries = zip(*sorted(zip(scores, entries)))

    # Sort entries by score and return.
    return entries

def fun_music(request_text, preferences, location):
    return ["fun_music", "rickroll"]

def find_zaklin(request_text, preferences, location):
    return "zaklin"

def eat(request_text, preferences, location):
    return "eat"

def shop(request_text, preferences, location):
    return "shop"

def walk_city(request_text, preferences, location):
    return "city"

def walk_park(request_text, preferences, location):
    return "walk_park"

def get_drunk(request_text, preferences, location):
    return "drunk"

def go_cinema(request_text, preferences, location):
    return "cinema"
