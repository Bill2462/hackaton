
def process_request(intent_detector, preference_detector, requests, preferences):
    requests = requests.splitlines()
    preferences = preferences.splitlines()

    intents = []
    for request in requests:
        intent = intent_detector(request)
        intents.append("intent: " + intent)

    for preference in preferences:
        intent = preference_detector(preference)
        intents.append("preference: " + intent)

    return {"responses": intents}
