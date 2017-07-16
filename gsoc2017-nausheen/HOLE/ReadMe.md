### This code has been taken from : https://github.com/mnick/holographic-embeddings




The code requires an input bin file. In order to convert the standard dataset into a bin file, run the following commands:
```
python makeid_file.py
```
The above command requires 3 files : train.txt, test.txt, valid.txt kept in <b>standard_data</b> folder. This code outputs two files entity2id.txt and relation2id.txt in the <b>standard_data</b> folder. This code assigns a unique integer id to every entity and relation found in train.txt, test.txt, valid.txt files.
```
python data2bin.py
```
The above command requires 5 files : train.txt, test.txt, valid.txt, entity2id.txt and relation2id.txt kept in the <b>standard_data</b> folder. This code outputs the bin file in the <b>data</b> folder.

Now run the following HolE shell script
```
python run_hole_DBpedia.sh
```
