Run the following commands to make various subsets :

1) For every entity <b><i>e</i></b> in Freebase dataset, the following command extracts all the triples <b><i><s, p, o></i></b> from DBpedia. This command will output 3 files : <t>DBpedia_freebase_mapped_full_train.txt</t>, DBpedia_freebase_mapped_full_valid.txt, DBpedia_freebase_mapped_full_test.txt
```
python Freebase2DBpedia.py
```

2) For every entity from Freebase we get a 1:N mapping in DBpedia. This N can be as large as 200-300 triples. In order to get a better training it is a good idea to shuffle this data, so that triples of same entity are not grouped together. I use the following Linux command to shuffle the data.

```
shuf DBpedia_freebase_mapped_full_train.txt -o shuffled_train.txt
shuf DBpedia_freebase_mapped_full_test.txt -o shuffled_test.txt
shuf DBpedia_freebase_mapped_full_valid.txt -o shuffled_valid.txt
```

3) Use the following code to make different subsets from the shuffled dataset.

```
python make_subsets.py
```




