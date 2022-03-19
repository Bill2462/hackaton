from actions import *

def process_intent(intent, request_text, preferences):
    actions = {
        "go_hospital": go_hospital_visit,
        "go_covid_test": go_covid_test,
        "fun_music": fun_music,
        "find_zaklin": find_zaklin,
        "eat": eat,
        "shop": shop,
        "walk_city": walk_city,
        "walk_park": walk_park,
        "get_drunk": get_drunk,
        "go_cinema": go_cinema}

    return actions[intent](request_text, preferences)

def process_request(intent_detector, preference_detector, request, preferences):
    preferences_lines = preferences.splitlines()

    intent = intent_detector(request)

    preferences = []
    for preference_line in preferences_lines:
        preferences.append(preference_detector(preference_line))

    recommendations = process_intent(intent, request, preferences)

    result = {"recommendations": recommendations}
    if len(preferences) > 0:
        result["preferences"] = preferences
    else:
        result["preferences"] = None

    return result
