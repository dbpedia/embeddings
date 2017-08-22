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

3) Remove unseen objects from test and valid sets. 


Rule: Every entity present in test and valid set must also be present in the the train set. Otherwise, how can a training algorithm predict an unseen entity?

In step 1, we have found the DBpedia triples for all the "subjects" found in Freebase train, test and valid set respectively. Since the Freebase set pre satisfies the above rule, the corresponding DBpedia set made already follows the rule for "subjects". However, "objects" entity has to be handled. So we prune out all the triples, in which the object entity is not present in train set. We do this by the following code:

```
python remove_unseen_objects.py
```


4) Use the following code to make different subsets from the shuffled dataset.

```
python make_subsets.py
```

The output of the above code can be directly used for training <b>TransE</b>, <b>DistMult</b> and <b>complex</b> codes. 
<b>HolE</b> would require one more step of converting these output files into bin file. Check HOLE folder for the steps.


