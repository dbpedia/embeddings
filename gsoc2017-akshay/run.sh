#!/usr/bin/env bash

bunzip2 enwiki-20180301-pages-articles-multistream.xml.bz2

python WikiExtractor.py --links -o output enwiki-20180301-pages-articles-multistream.xml

python WikiDetector.py output

python RVA_random.py output
