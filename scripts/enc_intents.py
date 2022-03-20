import pickle
from sentence_transformers import SentenceTransformer

class Intent:
    def __init__(self, key, text):
        self.key = key
        self.text = text

FILEPATH = "intents.pkl"
MODEL = "all-mpnet-base-v2"

INTENTS = [
    Intent("go_hospital", "need to see doctor"),
    Intent("go_hospital", "want to go to hospital"),
    Intent("go_hospital", "need medical help"),

    Intent("go_covid_test", "want covid test"),

    Intent("fun_music", "want music"),
    Intent("find_zaklin", "find zaklin"),

    Intent("eat", "want to eat"),
    Intent("eat_ice_cream", "I want to be happy"),

    Intent("shop", "want to buy"),
    Intent("shop", "want to shop"),

    Intent("walk_city", "want to see interesting places in the city"),

    Intent("walk_park", "want to go to green park"),
    Intent("walk_park", "want to see trees"),

    Intent("get_drunk", "want to get drunk"),
    Intent("get_drunk", "want to go drinking"),
    Intent("get_drunk", "want to spend evening in a bar"),

    Intent("go_cinema", "want to see a movie")
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
