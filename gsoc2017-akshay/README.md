### Extracting anchor text
tokenizePhrases.py saves the linked entity along with the anchor text in AnchorWords.csv it also erases the anchor text and saves the output to output_corpus.xml
Usage:
	`tokenizePhrases.py enwiki-20170520-pages-articles1.xml-p10p30302`
### Clearing xml markup
WikiExtractor.py cleans the xml code and saves the text output. WikiExtractor is built using the code found at https://github.com/attardi/wikiextractor.
Usage:
	`WikiExtractor.py output_corpus.xml -o OutputFile`
