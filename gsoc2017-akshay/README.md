# Generating Word2Vec Embeddings

## Usage
Firstly, `python WikiDetector.py enwiki-20170520-pages-articles.xml` modifies the dump by replacing surface forms with their corresponding entites and saves it to the file 'updatedWiki'.

`python WikiExtractor.py -o output updatedWiki` clears the xml markup and saves the plain text files to the output/ directory.

`python WikiTrainer.py output` trains Word2Vec embeddings using the plain text articles.

`python RVA.py output` generates embeddings for the entities using the plain text articles in the output directory (uses multiprocessing module).

`python RVA_single.py output` generates embeddings for the entities using the plain text articles in the output directory.

## Workflow
1. WikiDetector.py (replaceAnchorText)

..1. For each article in the Wikipedia Dump, a 'local' dictionary is generated with the entity as the key and a list of surface forms as the values. 
`Dictionary[entity] = [surfaceForms1, surfaceForm2,...]`
Trailing parantheses are removed from the surface forms, each entity name is capitalized and the spaces are replaced by underscores.

..2. Within the same article, the occurences of all surface forms held by the dictionary are replaced by their corresponding entity names. For example, if the article contains the following text:
`"These are often described as [[stateless society|stateless societies]] and it is in a stateless society..."`
..While substituting the entity name string 'entity/' is appended at the beginning.
`"These are often described as [[stateless society|entity/Stateless_society]] and it is in a entity/Stateless_society..."`

2. WikiDetector.py (replaceSurfaceForms)

..1. replaceSurfaceForms generates a 'global' dictionary using all the anchor text in the Wikipedia Dump file.
..2. A list of all the linked entities for a specific article is generated.
..3. All the surface forms in the 'global' dictionary are replaced by their corresponding entities. For example the text:
`"[[Barack Obama]] is the president of the... When Obama did..."`
..The replacement is possible since, in some other article entity/Barack_Obama has the anchor text 'Obama' and this pair was stored in the 'global' dictionary.
`"[[entity/Barack_Obama]] is the president of the .. When entity/Barack_Obama did..."`

3. WikiExtractor.py
This python file clears xml markup from the Wikipedia Dump and retains clean text.

4. WikiTrainer.py
Using the plain text generated using the WikiExtractor.py, Word2Vec embeddings can be trained.

## Random Vector Accumulator

1. RVA.py
Generates word RVA word embeddings for entities.
