import sys
from gensim.models import Word2Vec
import gensim

#load the dataset along with the saved embeddings
def evaluate(filename, fname):
	counter = 0
	top3Counter = 0
	top5c = 0
	linec = 0
	model = Word2Vec.load(fname)
	questions = []
	with open(filename) as test:
		for line in test:
			questions.append(line)

	for line in questions:
		if line.startswith(':'):
			try:
				print('Accuracy: ' + str(100*counter/linec) + '\n')
			except:
				pass
			print("Evaluating " + line.rstrip('\n'))
		else:	
			try:
				linec += 1
				source, target, question, answer = line.encode('utf-8').decode('utf-8').lower().rstrip('\n').replace('(', '').replace(')', '').split(' ')
				# word_vectors.most_similar(positive=['woman', 'king'], negative=['man'])
				result = model.wv.most_similar(positive=[target, question], negative=[source])
				if result[0][0] == answer:
					counter += 1
				print('Accuracy: ' + str(100*counter/linec), end = '\r')
				for i in range(0, 3):
					if result[i][0] == answer:
						top3Counter += 1
						break
				for i in range(0, 10):
					if result[i][0] == answer:
						top5c += 1
						break
			except:
				pass
	print('Correct guess: ' + str(100 * counter / linec))
	print('Correct guess in top 3:' + str(100 * top3Counter / linec))
	print('Correct guess in top 10:' + str(100 * top5c / linec))
	return None

if __name__ == '__main__':
	filename, fname = sys.argv[1:3]
	evaluate(filename, fname)