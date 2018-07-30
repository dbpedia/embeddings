import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import json


X = []
lines = []
labels = []
with open('data/embeddings_db.json', 'r') as db_file:
    for line in db_file:
        jsonline = json.loads(line)
        lines.append(jsonline)


for l in lines:
    entity = [_ for _ in l.keys()][0]
    X.append(np.array(l[entity]))
    labels.append(entity)


tsne = TSNE(n_components=2, random_state=0)
Y = tsne.fit_transform(X)

fig, ax = plt.subplots()
ax.scatter(Y[:, 0], Y[:, 1])

for i, txt in enumerate(labels):
    ax.annotate(txt, (Y[i, 0], Y[i, 1]))

plt.show()
