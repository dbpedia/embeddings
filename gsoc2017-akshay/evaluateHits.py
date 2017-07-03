import sys
from gensim.models import Word2Vec

def filterHits(candCountry, actCountry, Continent):
	rank = 15
	for i in range(15):
		# print(candCountry[i][0])
		if candCountry[i][0] == actCountry:
			rank = i
		while True and rank > 0:
			if candCountry[rank][0] in Continent:
				rank -= 1
				continue
			else:
				rank += 1
				break
	return rank

if __name__ == '__main__':
	fil, mod = sys.argv[1:3]
	model = Word2Vec.load(mod)
	top1 = 0; top3 = 0; top10 = 0
	topf1 = 0; topf3 = 0; topf10 = 0
	total = 0
	countries = {}
	continents = set()
	with open(fil, 'r') as output:
		for line in output:
			if line.startswith(':'):
				name = line.strip(':').strip().replace(' ', '_')
				continents.add(name.lower().replace('(', '').replace(')', ''))
				countries[name.lower().replace('(', '').replace(')', '')] = set()
				continue
			else:
				countries[name.lower().replace('(', '').replace(')', '')].add(line.strip().replace(' ', '_').lower().replace('(', '').replace(')', ''))
	for continent in continents:
		for continent2 in continents:
			if not continent == continent2:
				for country in countries[continent]:
					for country2 in countries[continent2]:
					# try:
						countr = model.wv.most_similar(positive=[country, continent2], negative=[continent], topn=15)
					#.wv.most_similar(positive=['woman', 'king'], negative=['man'])
						total += 1
						print(str(total) + '. ' + continent + ':' + country + '::' + continent2 + ':' + country2)
						rank = 10
						for i in range(10):
							# print(countr[i][0])
							if countr[i][0] == country2:
								rank = i
						if rank == 0:
							top1 += 1
						elif rank < 3:
							top3 += 1
						elif rank < 10:
							top10 += 1
						rank1 = filterHits(countr, country2, countries[continent2])
						if rank1 == 0:
							topf1 += 1
						elif rank1 < 3:
							topf3 += 1
						elif rank1 < 10:
							topf10 += 1
						print('Hit: ' + str(rank) + ';' + 'FiltHit: ' + str(rank1))
					# except:
						pass
	print("Raw Hits@1: " + str(100*top1/total) + "%")
	print("Raw Hits@3: " + str(100*top3/total) + "%")
	print("Raw Hits@10: " + str(100*top10/total) + "%")
	print("Filtered Hits@1: " + str(100*topf1/total) + "%")
	print("Filtered Hits@3: " + str(100*topf3/total) + "%")
	print("Filtered Hits@10: " + str(100*topf10/total) + "%")