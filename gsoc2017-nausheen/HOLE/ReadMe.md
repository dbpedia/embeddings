This code has been taken from : https://github.com/mnick/holographic-embeddings




The code requires an input bin file. In order to convert the standard dataset into a bin file, run the following commands:

python makeid_file.py

The above command requires 3 files : train.txt, test.txt, valid.txt. This code outputs two files entity2id.txt and relation2id.txt

python data2bin.py

The above command requires 5 files : train.txt, test.txt, valid.txt, entity2id.txt and relation2id.txt. This code outputs the bin file.

Now run the following HolE shell script

python run_hole_DBpedia.sh
