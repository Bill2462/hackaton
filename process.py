from actions import *

def find_intents(lines, detector):
    intents = []
    for line in lines:
        intents.append(detector(line))
    return intents

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

def process_request(intent_detector, preference_detector, requests, preferences):
    requests_lines = requests.splitlines()
    preferences_lines = preferences.splitlines()

    intents = find_intents(requests_lines, intent_detector)
    preferences = find_intents(preferences_lines, preference_detector)

    responses = []

    for request, intent in zip(requests_lines, intents):
        responses.append(process_intent(intent, request, preferences))

    result = {"responses": responses}
    if len(preferences) > 0:
        result["preferences"] = preferences
    else:
        result["preferences"] = None

    return result
