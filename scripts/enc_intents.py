import pickle
from sentence_transformers import SentenceTransformer

class Intent:
    def __init__(self, key, text):
        self.key = key
        self.text = text

FILEPATH = "intents.pkl"
MODEL = "all-mpnet-base-v2"

INTENTS = [
    Intent("go_hospital", "I need to see a doctor"),
    Intent("go_hospital", "I want to see a doctor"),
    Intent("go_hospital", "I need to go to hospital"),
    Intent("go_hospital", "I want to go to hospital"),
    Intent("go_hospital", "I need medical help"),
    Intent("go_hospital", "I'm sick"),

    Intent("go_covid_test", "I want covid test"),
    Intent("go_covid_test", "I need covid test"),
    Intent("go_covid_test", "I want to test for covid"),

    Intent("eat", "I want to eat with my friends"),
    Intent("eat", "I will eat"),
    Intent("eat", "I want to eat something"),
    Intent("eat", "I want to go to the restaurant"),
    Intent("eat", "I want to have dinner"),
    Intent("eat", "I will have meal"),
    Intent("eat", "I want to have meal"),

    Intent("shop", "I want to buy something"),
    Intent("shop", "I want to go shopping in supermarket"),
    Intent("shop", "I want to go shopping in gallery"),
    Intent("shop", "I want to buy bricks"),
    Intent("shop", "I want to buy cloths"),
    Intent("shop", "I want to go shopping with my friends in castorama"),

    Intent("walk_city", "I want to see the city"),
    Intent("walk_city", "I want to see the city with my friends"),
    Intent("walk_city", "I want to spend some time with my friends and see the city"),
    Intent("walk_city", "I want to see some interesting places in the city"),
    Intent("walk_city", "I want to go to some interesing places in the city"),
    Intent("walk_city", "I want to see some interesting places"),

    Intent("walk_park", "I want to go to park"),
    Intent("walk_park", "I want to take a walk in a park"),
    Intent("walk_park", "I want spend some time in a park"),
    Intent("walk_park", "I want to see the park"),

    Intent("get_drunk", "I want to get drunk with my friends"),
    Intent("get_drunk", "I want to go drinking with my friends"),
    Intent("get_drunk", "I want to get drinks with my friends"),
    Intent("get_drunk", "I want to spend evening in a bar"),

    Intent("go_cinema", "I want to go and see a movie"),
    Intent("go_cinema", "I want to go to cinema"),
    Intent("go_cinema", "I want to see a movie with my friends"),
    Intent("go_cinema", "I want to go see some film")
]

print("Loading transformers and Michael Bay ...")

model = SentenceTransformer("all-mpnet-base-v2", device="cpu")

embeddings = []
intents = []

for intent in INTENTS:
    print(f"Encoding {intent.text} ...")
    embeddings.append(model.encode(intent.text))
    intents.append(intent.key)

output = {"embeddings": embeddings, "intents": intents}

with open(FILEPATH, "wb") as handle:
    pickle.dump(output, handle, protocol=pickle.HIGHEST_PROTOCOL)
