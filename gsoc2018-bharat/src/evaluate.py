import numpy as np
import json
from gensim.models import FastText
import logging


logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO
model = FastText.load('model/entity_fasttext_n100')
wv = model.wv
del model

X = []
labels = []


with open('data/dbpedia_embeddings_db.json', 'r') as db_file:
    for line in db_file:
        jsonline = json.loads(line)
        entity = [_ for _ in jsonline.keys()][0]
        X.append(np.array(jsonline[entity]))
        labels.append(entity)


X = np.array(X)
mean_score = wv.cosine_similarities(wv['organisation'], X).mean()
