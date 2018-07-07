import os
import sys
import codecs
import json
import re

root_directory, wiki_file, output = sys.argv[1], sys.argv[2], sys.argv[3]
punctuation = '!"#$%&\'()*+,./:;<=>?@[\\]^`{|}~'
table = str.maketrans('', '', punctuation)
"""
The following snippet is used to count the
unique resources in the entire corpus.
These are the injected entities which
were tagged with the help of Surface Forms
generated from the original dump.
"""
entities = set()
for root, directories, files in os.walk(root_directory):
    for f in files:
        path = root + '/' + f
        for line in codecs.open(path, 'r', encoding='utf-8', errors='ignore'):
            for ent in re.findall(r'(resource/)+(\w+)', line):
                entities.add(''.join(ent))
                print("Entities : " + str(len(entities)), end='\r')
print("Entities : " + str(len(entities)))
del entities


"""
Here I will create a dictionary containing the mappings
between the entities and their descriptions.
"""


def reader(file_name):
    with codecs.open(file_name, 'r', encoding='utf-8',
                     errors='ignore') as input_file:
        prev = next(input_file)
        for line in input_file:
            yield prev, line
            prev = line


"""
The following snippet combines the different files extracted
using the extract.py script and creates a single file with
complete text that can be used to generate pre-trained embeddings.
"""


with open(wiki_file, 'w+') as output_file:
    for root, directories, files in os.walk(root_directory):
        for f in files:
            print("Writing file " + str(root) + '/' + str(f))
            path = root + '/' + f
            with codecs.open(path, 'r', encoding='utf-8',
                             errors='ignore') as input_file:
                for line in input_file:
                    if '<doc' in line:
                        pass
                    else:

                        # Obtain just the processed text
                        # from the multiple files
                        line = line.replace('resource/', '')
                        line = line.lower().translate(table)
                        output_file.write(line)

count = 0

# Pattern to extract title from the document url
pattern = r'(title=)+(.\w+.)*'
with open(output, 'w+') as output_dictionary:
    for root, directories, files in os.walk(root_directory):
        for f in files:
            path = root + '/' + f
            with codecs.open(path, 'r', encoding='utf-8',
                             errors='ignore') as input_file:
                for prev, line in reader(path):
                    dictionary = {}
                    if prev.startswith('<doc') and not line.startswith('<doc'):
                        try:
                            ent = re.search(pattern, prev).group().strip('"')
                            ent = ent.replace(' ', '_').replace('title="', '')
                            ent = ent.lower().translate(table)

                            # Line serves the purpose of description
                            line = line.replace('resource/', '')
                            dictionary[ent] = line.lower().translate(table)
                            json.dump(dictionary, output_dictionary)
                            output_dictionary.write('\n')
                            count += 1
                            print("Descriptions : " + str(count), end='\r')
                            continue
                        except KeyError:
                            continue
                    else:
                        pass

print("Descriptions : " + str(count))
