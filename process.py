
def process_request(intent_detector, preference_detector, requests, preferences):
    requests = requests.splitlines()
    preferences = preferences.splitlines()

    # Extract each intent.
    intents = []
    for request in requests:
        intent = intent_detector(request)
        print(f"intents by similarity: {intent}")
        intent = next(iter(intent))[0] # Most likely intent.
        intents.append("intent: " + intent)

    for preference in preferences:
        intent = preference_detector(preference)
        print(f"prefs by similarity: {intent}")
        intent = next(iter(intent))[0] # Most likely intent.
        intents.append("preference: " + intent)

    return {"responses": intents}
