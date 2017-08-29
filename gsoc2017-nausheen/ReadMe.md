<h1> Knowledge Base Embeddings for DBpedia </h1>

This project is done as a part of participation at <b><a href="https://summerofcode.withgoogle.com/">Google Summer of Code 2017</a></b>, for the open source organisation <b>DBpedia</b>

<b>Word embeddings</b> has been found to be very useful in the research community in the recent years by bringing semantically similar word closer in the vector space. Word embeddings is being actively used in many applications such as sentiment analysis, recommendation systems, question answering, etc. Knowledge graphs have been popularly used for storing data in the form of graph in the form of entities and relationships. The objective of this project is to find embeddings for knowledge graphs entities and relationships. If we want to find word embedding for a movie like <i><b>“Beauty and the Beast”</b></i>, simple aggregation/averaging of word embeddings for individual word tokens may or may not make great sense , as these words may be scattered far away in the text space. It would be very useful if we can get embeddings of the complete phrase as 1 atomic unit. Since knowledge graphs already stores the data in entities and relationship form, it would be very useful to get embeddings representation for the same.

Read my week by week blogs here: https://nausheenfatma.wordpress.com/category/gsoc-2017/

<h3>Training the embeddings on FB15K and WN18K datasets:</h3>

```
THEANO_FLAGS='device=gpu' python complex/fb15k_run.py
THEANO_FLAGS='device=gpu' python complex/wn18_run.py

cd HOLE
./run_hole_wn18.sh
```

<h3>Experiment Results of the chosen models on FB15K and WN18K datasets:</h3>



<table>
<tr>
   <th>Model</th>
    <th colspan="5">WN18</th>
    <th colspan="5">FB15K</th>
  </tr>
  <tr>
    <th></th>
    <th>MRR (raw)</th>
    <th>MRR (filtered)</th>
    <th>Hits@1 </th>
    <th>Hits@3 </th>
    <th>Hits@10 </th>
    <th>MRR (raw)</th>
    <th>MRR (filtered)</th>
    <th>Hits@1 </th>
    <th>Hits@3 </th>
    <th>Hits@10 </th>
 </tr>
  
  
  <tr>
  <td>TransE</td>
  <td>0.431</td>
    <td>0.309</td>
    <td>0.083</td>
    <td>0.778</td>
    <td>0.936</td>
    <td>0.374</td>
    <td>0.219</td>
    <td>0.219</td>
    <td>0.471</td>
    <td>0.643</td>    
  </tr>
    <tr>
  <td>DistMult</td>
    <td>0.835</td>
    <td>0.561</td>
    <td>0.753</td>
    <td>0.913</td>
    <td>0.937</td>
    <td>0.651</td>
        <td>0.237</td>
    <td>0.544</td>
    <td>0.728</td>
    <td>0.825</td>
  </tr>
    <tr>
  <td>HolE</td>
  <td><b>0.62</b></td>
  <td><b>0.94</b></td>
        <td>0.928</td>
        <td><b>0.941</b></td>
    <td><b>0.944</b></td>
    <td>0.21</td>
    <td>0.46</td>
    <td>33.45</td>
    <td>53.63</td>
    <td>67.54</td>
  </tr>
    <tr>
  <td>ComplEx</td>
  <td>0.581</td>
    <td><b>0.94</b></td>   
        <td><b>0.937</b></td>
    <td><b>0.941</b></td>
    <td><b>0.944</b></td>
    <td><b>0.672</b></td>
        <td>0.235</td>
        <td><b>0.571</b></td>
    <td><b>0.746</b></td>
    <td><b>0.832</b></td>
  </tr>
</table>







<table>
<tr>
   <th>Model</th>  
   <th>Time Complexity </th>
   <th>Space Complexity</th>
    <th colspan="2">WN18 <br></th>
    <th colspan="2">FB15K <br></th>
  </tr>


<tr>
    <td></td>
     <td></td>
      <td></td>
    <th>#Epochs</th>
    <th>Training time <br>(in hours)</th>
    <th>#Epochs</th>
    <th>Training time <br>(in hours)</th>    
  </tr>
  
  
  <tr>
  <td>TransE</td>
    <td>O(K)</td>
    <td>O(K)</td>
    <td>251</td>
    <td>2.68 (CPU),<br> 0.61 (GPU)</td>
    <td>1000</td>
    <td>6.77</td>    
  </tr>
    <tr>
  <td>DistMult</td>
    <td>O(K)</td>
    <td>O(K)</td>
    <td>501</td>
    <td>3.22</td>
    <td>551</td>
    <td>20.38</td>
  </tr>
    <tr>
  <td>HolE</td>
    <td>O(K log K)</td>
    <td>O(K)</td>
    <td>500</td>
    <td>3.98</td>
    <td>1500</td>
    <td>59.59</td>
  </tr>
    <tr>
  <td>ComplEx</td>
    <td>O(K)</td>
    <td>O(K)</td>
    <td>551</td>
    <td>9.04</td>    
    <td>751</td>
    <td>107.33</td>
  </tr>
</table>


<h3>Making the DBpedia dataset mapped from Freebase subjects :</h3>
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


<h3>Training the DBpedia data : </h3>

```
THEANO_FLAGS='device=gpu' python complex/dbpedia_run.py
```

Experiment Results on DBpedia datasets:
<table>
<tr>
   <th>Model</th>
    <th colspan="5">DBpedia (train size=10000)</th>
  </tr>
  <tr>
    <th></th>
    <th>MRR (raw)</th>
    <th>MRR (filtered)</th>
    <th>Hits@1 </th>
    <th>Hits@3 </th>
    <th>Hits@10 </th>
     <th>#Epochs</th>
      <th>Training time (in seconds)</th>
 </tr>
 <tr>
  <td>TransE</td>
    <td>0.009</td>   
    <td>0.01</td>
    <td>0.001</td>
    <td>0.013</td>
    <td>0.028</td>
    <td>201</td>
    <td>424.68</td>
  </tr>
  
  
</table>



<h3> Predicting the time to train entire DBpedia </h3>
In order to compare the runtime for the approach DistMult on the three varying sets and predicting the training time for full DBpedia size dataset , I executed <b>DisMult</b> on each set for a fixed number of epochs which was 300. In order to understand why we chose DistMult approach, please read detailed blog post <a href="https://nausheenfatma.wordpress.com/2017/08/28/gsoc-final-submission/">here</a>. After plotting the results on a line graph using Microsoft Excel trendline feature, I got the following graph :


![alt text](https://github.com/nausheenfatma/embeddings/blob/master/gsoc2017-nausheen/polynomial.PNG)



<h3> Code and Contribution </h3>
You can find all the code contribution (new codes/ updated codes) information from this patch <a href="https://github.com/nausheenfatma/embeddings/blob/master/gsoc2017-nausheen/contribution_patch.patch ">file</a>.

You can download the 1 million DBpedia dataset for training, and the final DistMult embeddings from <a href="http://tsoru.aksw.org/gsoc2017/dbpedia201604-1M-triples/distmult-embeddings-100dim.zip">here</a>.
