import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

X = np.loadtxt("embeddings");
# print(X[0])
labels = []
with open('labels') as output:
	for line in output:
		labels.append(line.split('resource/')[1].strip())

tsne = TSNE(n_components=2, random_state=0)
Y = tsne.fit_transform(X[:3000])

fig, ax = plt.subplots()
ax.scatter(Y[:,0], Y[:,1]);

for i, txt in enumerate(labels):
	if i == 3000:
		break
	ax.annotate(txt.decode("utf-8"), (Y[i,0], Y[i,1]))
plt.show()
