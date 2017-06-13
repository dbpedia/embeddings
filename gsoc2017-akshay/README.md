# Generating Word2Vec Embeddings

## Usage
Firstly, `python WikiExtractor.py --links -o output enwiki-20170520-pages-articles.xml` clears the xml markup retaining only the links.

`python WikiDetector.py output/` replaces the surface forms using a dictionary local to each article.

`python WikiTrainer.py output` trains Word2Vec embeddings using the plain text articles.

## Workflow

### 1. WikiExtractor.py
This python file clears xml markup from the Wikipedia Dump and retains clean text.

### 2. WikiDetector.py (replaceAnchorText)

  2.1. For each article in the Wikipedia Dump, a 'local' dictionary is generated with the entity as the key and a list of surface forms as the values. 
`Dictionary[entity] = [surfaceForms1, surfaceForm2,...]`
Trailing parantheses are removed from the surface forms, each entity name is capitalized and the spaces are replaced by underscores.

  2.2. Within the same article, the occurences of all surface forms held by the dictionary are replaced by their corresponding entity names. For example, if the article contains the following text:
`"These are often described as [[stateless society|stateless societies]] and it is in a stateless society..."`
  While substituting the entity name string 'entity/' is appended at the beginning.
`"These are often described as [[stateless society|entity/Stateless_society]] and it is in a entity/Stateless_society..."`

### 3. WikiDetector.py (replaceSurfaceForms)

  3.1. replaceSurfaceForms generates a 'global' dictionary using all the anchor text in the Wikipedia Dump file.
  
  3.2. A list of all the linked entities for a specific article is generated.
  
  3.3. All the surface forms in the 'global' dictionary are replaced by their corresponding entities. For example the text:
  
`"[[Barack Obama]] is the president of the... When Obama did..."`

  The replacement is possible since, in some other article entity/Barack_Obama has the anchor text 'Obama' and this pair was stored in the 'global' dictionary.
  
`"[[entity/Barack_Obama]] is the president of the .. When entity/Barack_Obama did..."`

### 4. WikiTrainer.py
Using the plain text generated using the WikiExtractor.py, Word2Vec embeddings can be trained.
