from actions import *
from geopy.geocoders import Nominatim

geocoder = Nominatim(user_agent="weeia jam hackaton team")

def process_intent(intent, request_text, preferences, location):
    actions = {
        "go_hospital": go_hospital_visit,
        "go_covid_test": go_hospital_visit,
        "fun_music": fun_music,
        "find_zaklin": find_zaklin,
        "eat": eat,
        "eat_ice_cream": eat_ice_cream,
        "shop": shop,
        "walk_city": walk_city,
        "walk_park": walk_park,
        "get_drunk": get_drunk}

    return actions[intent](request_text, preferences, location)

def process_request(intent_detector, preference_detector, request, preferences, location):
    preferences_lines = preferences.splitlines()

    location = geocoder.geocode(f"{location}, Lodz, Poland")
    if location is None:
        return "Error: cannot recognize your address"

    print(location.latitude, location.longitude)

    intent = intent_detector(request)

    preferences = []
    for preference_line in preferences_lines:
        preferences.append(preference_detector(preference_line))

    recommendations = process_intent(intent, request, preferences, location)

    result = {"recommendations": recommendations}
    if len(preferences) > 0:
        result["preferences"] = preferences
    else:
        result["preferences"] = None

    return result
