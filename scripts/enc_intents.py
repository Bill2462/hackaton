import pickle
from sentence_transformers import SentenceTransformer

class Intent:
    def __init__(self, key, text):
        self.key = key
        self.text = text

FILEPATH = "intents.pkl"
MODEL = "all-mpnet-base-v2"

INTENTS = [
    Intent("shopping", "shopping"),
    Intent("eating", "eating"),
    Intent("walking", "walking"),
    Intent("park_walking", "walking in park"),
    Intent("seeing_city", "walking around city")
]

model = SentenceTransformer("all-mpnet-base-v2", device="cpu")

embeddings = []
intents = []

for intent in INTENTS:
    embeddings.append(model.encode(intent.text))
    intents.append(intent.key)

output = {"embeddings": embeddings, "intents": intents}

with open(FILEPATH, "wb") as handle:
    pickle.dump(output, handle, protocol=pickle.HIGHEST_PROTOCOL)
