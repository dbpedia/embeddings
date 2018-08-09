import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import json
import sys


db_file = sys.argv[1]
X = []
lines = set()
dictionary = {}
labels = []
with open(db_file, 'r') as f:
    for line in f:
        jsonline = json.loads(line)
        dictionary.update(jsonline)
        lines.add([_ for _ in jsonline.keys()][0])


for l in lines:
    entity = l
    X.append(np.array(dictionary[entity]))
    labels.append(entity)


tsne = TSNE(n_components=2, random_state=0)
Y = tsne.fit_transform(X)

fig, ax = plt.subplots()
ax.scatter(Y[:, 0], Y[:, 1])

for i, txt in enumerate(labels):
    ax.annotate(txt, (Y[i, 0], Y[i, 1]))

plt.show()
