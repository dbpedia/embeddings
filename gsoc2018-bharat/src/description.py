import json
import sys
from urllib.parse import unquote
import codecs
import string, unicodedata

def main():
	"""
	The script processes input XML dump for all Wikipedia Abstracts and outputs
	a JSON file with the entities and their abstracts in key: value pairs.

	Saves the JSON file as
	-----------
	dictionary[entity] = abstract
	"""
	wiki_file, dictionary = sys.argv[1], sys.argv[2]
	count = 0
	table = str.maketrans('', '', string.punctuation)
	with open(file, 'r') as input_file:
		with open(dictionary, 'w+') as output_file:
			for line in input_file:
				"""
				I am trying to remove the url from the doc to get the
				title and then cleaning the abstract for that title.
				"""
				description = {}
				if line.startswith('<url>'):
					# Process the url
					entity = unquote(line)

					# Extracting document title from the url
					entity = "resource" + entity.replace('https://en.wikipedia.org/wiki', '').lstrip('<url>').replace('</url>', '').strip()
				if line.startswith('<abstract>'):

					# Removing trailing parantheses from the abstracts Wiki code
					abstract = line.lstrip('<abstract>').replace('</abstract>', '').replace('(', '').replace(')', '').strip()
					abstract = abstract.translate(table)
					abstract = ' '.join(abstract.split())
					count += 1
					print("Total abstracts : " + str(count), end='\r')

					# Plain text abstracts stored for each and every resource in the dump
					description[entity] = abstract
					json.dump(description, output_file)
					output_file.write('\n')
	print("Total abstracts : " + str(count))
	
if __name__ == '__main__':
	main()