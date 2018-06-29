import os
import re
import sys
import time
import tempfile
from joblib import Parallel, delayed
from urllib.parse import unquote
from collections import Counter


def replace_anchor_text(file_name):
    """
    Given the input file, the surface forms loaded from anchor text
    are used to extract entity mentions and replace them with the
    article title in the text corpus itself.

    Arguments
    ---------
    file_name : Input file containing the extracted text.
    """
    print(file_name)
    pattern = r'\<a href\=\"([^\"\:]+)\"\>([^\<]+)\</a\>'
    # A temporary file to track the input file document by document.
    t = tempfile.NamedTemporaryFile(mode='r+')
    dictionary = {}
    with open(file_name, 'r') as wiki_file:
        for line in wiki_file:
            if line.startswith("<doc"):
                t.write(line)

                # Get the title of the document from XML
                title = line.split('title="')[1].split('">')[0]
                TITLE = title.replace(' ', '_')

                dictionary = {}
                next(wiki_file)

                # Global surface forms dictionary
                global surface_forms
                try:
                    dictionary[TITLE] = surface_forms[TITLE]
                except KeyError:
                    dictionary[TITLE] = set([title])

                # Gender dictionary from checking persons
                global gender

                try:
                    if gender[title] == 'f':
                        dictionary[TITLE].add('she')
                        dictionary[TITLE].add('her')
                        dictionary[TITLE].add('hers')
                    else:
                        dictionary[TITLE].add('he')
                        dictionary[TITLE].add('him')
                        dictionary[TITLE].add('his')
                except KeyError:
                    pass

                continue

            # Regular expressions to find and
            # replace anchor text with resource entity
            elif not line == '\n':
                links = re.findall(pattern, line)
                for link in links:
                    entity = link[0].replace('wikt%3A', '')
                    entity = entity.replace('wiktionary%3A', '')
                    if entity == '':
                        entity = link[1]

                    entity = unquote(entity[0].upper() + entity[1:])
                    entity = entity.replace(' ', '_')
                    anchor = link[1].split(' (')[0]
                    anchor = re.escape(anchor)
                    if entity not in dictionary:
                        dictionary[entity] = set()
                    dictionary[entity].add(anchor)
                line = re.sub('<.*?>', '', line)
            for entity in sorted(dictionary, key=len, reverse=True):
                for surface_form in sorted(dictionary[entity],
                                           key=len, reverse=True):
                    try:
                        line = re.sub(r"\b(?<![\/\(])%s\b" % surface_form,
                                      'resource/' + entity,
                                      line, flags=re.IGNORECASE)
                    except TypeError:
                        dictionary[entity].remove(surface_form)

            if not line == '\n':
                t.write(line)

    t.seek(0)

    with open(file_name, 'w') as output_file:
        for line in t:
            output_file.write(line)

    t.close()

    return None


def load_surface_forms(file_name, most_frequent):
    """
    Takes the surface form dictionary as input and
    returns the loaded entities mapped onto their
    most common surface forms.

    Arguments
    ---------
    file_name : Input dictionary
    most_frequent : Parameter to decide the most frequent surface forms
    """
    surface_form = {}
    c = 0
    with open(file_name, 'r') as input_file:
        for line in input_file:
            c += 1
            t = int(c * 1000 / 746565) / 10
            print('Loading surface forms: ' + str(t) + '%', end='\r')
            resource = line.split(';', 1)[0]
            line_split = line.rstrip('\n').split(';', 1)[1].split(';')
            surface_form[resource] = set(x[0] for x in Counter(line_split).most_common(most_frequent))
    return surface_form


def load_dictionary(file_name):
    """
    Loads the entire surface form dictionary from memory
    """
    surface_form = {}
    with open(file_name, 'r') as input_file:
        for line in input_file:
            try:
                surface_form[line.rsplit(';', 1)[0]] = \
                    line.rstrip('\n').rsplit(';', 1)[1]
            except KeyError:
                pass
    return surface_form


def split_files(directory):
    """
    Iterate through the files in the extracted directory
    """
    names = []
    for root, directories, files in os.walk(directory):
        for f in files:
            names.append(root + '/' + f)
    flag = False
    for name in names:
        with open(name, 'r') as input_file:
            directory_name = name + '_'
            os.mkdir(directory_name)
            for line in input_file:
                if line.startswith('</doc'):
                    continue
                elif line.startswith('<doc'):
                    file_name = line.split('title="')[1].split('">')[0]. \
                        replace(' ', '_').capitalize()
                else:
                    with open(directory_name + '/' + file_name, '+a') \
                            as output_file:
                        if not line == '\n':
                            output_file.write(line)
        os.remove(name)
    return None


if __name__ == "__main__":
    directory = sys.argv[1]
    anchor_file, gender_file = sys.argv[2], sys.argv[3]

    surface_forms = load_surface_forms(anchor_file, 5)
    gender = load_dictionary(gender_file)

    names = []
    for root, directories, files in os.walk(directory):
        for f in files:
            names.append(root + '/' + f)

    Parallel(n_jobs=8, verbose=51)(delayed(replace_anchor_text)(name) for name in names)
