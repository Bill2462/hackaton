import pickle
from collections import OrderedDict
from sentence_transformers import SentenceTransformer, util

class Detector:
    """
    Provide path to intent embeddings pickle.
    """
    def __init__(self, embeddings_pickle_filepath, model="all-mpnet-base-v2", device="cpu"):
        with open(embeddings_pickle_filepath, "rb") as handle:
            obj = pickle.load(handle)

        self.model = SentenceTransformer(model, device=device)

        self.embeddings = obj["embeddings"]
        self.intents = obj["intents"]

    def __call__(self, querry):
        querry_embedding = self.model.encode(querry)
        similarities = util.dot_score(querry_embedding, self.embeddings)[0]

        result = OrderedDict(zip(self.intents, similarities))
        result = sorted(result.items(), key=lambda x: x[1], reverse=True)

        return result
