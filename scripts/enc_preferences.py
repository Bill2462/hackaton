import pickle
from sentence_transformers import SentenceTransformer

class Intent:
    def __init__(self, key, text):
        self.key = key
        self.text = text

FILEPATH = "prefs.pkl"
MODEL = "all-mpnet-base-v2"

INTENTS = [
    Intent("drive_mode", "drive car"),

    Intent("walk_mode", "walk"),

    Intent("prefer_few_people", "few people"),

    Intent("prefer_quiet", "quiet and no noise"),

    Intent("prefer_clean_air", "clean air"),
]

print("Loading transformers and badass explosions in the background...")

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
