import sys
import re
import os
import codecs


class Reader(object):
    # Replaces the Gensim class LineSentence
    def __init__(self, directory_name):
        self.directory_name = directory_name

    def __iter__(self):
        for root, directories, files in os.walk(self.directory_name):
            for file_name in files:
                file_path = root + '/' + file_name
                for line in codecs.open(file_path, 'r', encoding='utf-8',
                                        errors='ignore'):
                    if line == "\n":
                        continue
                    yield line


def make_dictionary(directory):
    """
    All the links present in the corpus are treated as resources and
    the text is treated as the surface form for that very entity.
    """
    counter = 0
    print("Opened ", directory)
    sentences = Reader(directory)
    dictionary = {}
    for line in sentences:
        counter += 1

        # Finding all the anchor text, that is the <a> tags
        links = re.findall(r'\<a href\=\"([^\"\:]+)\"\>([^\<]+)\</a\>', line)
        for link in links:
            entity = link[0].capitalize().replace('%20', '_')
            entity = entity.replace('%28', '(').replace('%29', ')')
            anchor = link[1].split(' (')[0]
            try:
                dictionary[entity] += ';' + anchor
            except KeyError:
                dictionary[entity] = entity
                dictionary[entity] += ';' + anchor
            print(f'Anchor Text found : {counter}', end='\r')
    with open('../data/AnchorDictionary.csv', '+w') as output_file:
        for entity in dictionary:
            print('Writing to file: ' + entity, end='\r')
            output_file.write(dictionary[entity] + '\n')
    return None


if __name__ == "__main__":
    directory = sys.argv[1]
    make_dictionary(directory)
