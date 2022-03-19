import pickle
from sentence_transformers import SentenceTransformer

class Intent:
    def __init__(self, key, text):
        self.key = key
        self.text = text

FILEPATH = "prefs.pkl"
MODEL = "all-mpnet-base-v2"

INTENTS = [
    Intent("drive_mode", "I want to drive a car"),
    Intent("drive_mode", "I prefer to drive a car"),
    Intent("drive_mode", "I will drive"),
    Intent("drive_mode", "Select route for car"),
    Intent("drive_mode", "Select route for car"),

    Intent("walk_mode", "I want to walk"),
    Intent("walk_mode", "I prefer to walk"),
    Intent("walk_mode", "I will walk"),
    Intent("walk_mode", "Select route for car"),

    Intent("prefer_few_people", "I do not want to see a lot of people"),
    Intent("prefer_few_people", "I prefer places with few people"),
    Intent("prefer_few_people", "I don't want to stand in line"),
    Intent("prefer_few_people", "Prefer places with few people"),

    Intent("prefer_quiet", "I do not want noise"),
    Intent("prefer_quiet", "I want piece and quiet"),
    Intent("prefer_quiet", "I want quiet places"),
    Intent("prefer_quiet", "Prefer quiet places"),

    Intent("prefer_clean_air", "I want to breath air and not some poison"),
    Intent("prefer_clean_air", "I want clean air"),
    Intent("prefer_clean_air", "I prefer clean air"),
    Intent("prefer_clean_air", "Prefer clean air"),
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
