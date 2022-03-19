
def process_request(intent_detector, preference_detector, requests, preferences):
    requests = requests.splitlines()
    preferences = preferences.splitlines()

    # Extract each intent.
    intents = []
    for request in requests:
        intent = intent_detector(request)
        intent = next(iter(intent))[0] # Most likely intent.
        intents.append(intent)

    return {"responses": intents}
