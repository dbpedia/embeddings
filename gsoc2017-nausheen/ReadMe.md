<h1> Knowledge Base Embeddings for DBpedia </h1>

This project is done as a part of participation at <b><a href="https://summerofcode.withgoogle.com/">Google Summer of Code 2017</a></b>, for the open source organisation <b>DBpedia</b>

<b>Word embeddings</b> has been found to be very useful in the research community in the recent years by bringing semantically similar word closer in the vector space. Word embeddings is being actively used in many applications such as sentiment analysis, recommendation systems, question answering, etc. Knowledge graphs have been popularly used for storing data in the form of graph in the form of entities and relationships. The objective of this project is to find embeddings for knowledge graphs entities and relationships. If we want to find word embedding for a movie like <i><b>“Beauty and the Beast”</b></i>, simple aggregation/averaging of word embeddings for individual word tokens may or may not make great sense , as these words may be scattered far away in the text space. It would be very useful if we can get embeddings of the complete phrase as 1 atomic unit. Since knowledge graphs already stores the data in entities and relationship form, it would be very useful to get embeddings representation for the same.

Read my week by week blogs here: https://nausheenfatma.wordpress.com/category/gsoc-2017/

<h2>Training the embeddings on FB15K and WN18K datasets:</h2>

```
THEANO_FLAGS='device=gpu' python complex/fb15k_run.py
THEANO_FLAGS='device=gpu' python complex/wn18_run.py

cd HOLE
./run_hole_wn18.sh
```
<h3>Making input bin file which HolE supports</h3>

The open source HoLe <a href="https://github.com/mnick/holographic-embeddings">code</a> requires an input bin file and not text files. In order to convert the standard dataset into a bin file, run the following commands:
```
python makeid_file.py
```
The above command requires 3 files : train.txt, test.txt, valid.txt kept in <b>HOLE/standard_data</b> folder. This code outputs two files entity2id.txt and relation2id.txt in the <b>HOLE/standard_data</b> folder. This code assigns a unique integer id to every entity and relation found in train.txt, test.txt, valid.txt files.
```
python data2bin.py
```
The above command requires 5 files : train.txt, test.txt, valid.txt, entity2id.txt and relation2id.txt kept in the <b>HOLE/standard_data</b> folder. This code outputs the bin file in the <b>HOLE/data</b> folder.

Now run the following shell script to train the embeddings and find the performance results :
```
./run_hole_DBpedia.sh
```




<h2>Experiment Results of the chosen models on FB15K and WN18K datasets:</h2>



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


<h2>Making the DBpedia dataset mapped from Freebase subjects :</h2>
Run the following commands to make various subsets :

1) For every entity <b><i>e</i></b> in Freebase dataset, the following command extracts all the triples <b><i><s, p, o></i></b> from DBpedia. This command will output 3 files : <t>DBpedia_freebase_mapped_full_train.txt</t>, DBpedia_freebase_mapped_full_valid.txt, DBpedia_freebase_mapped_full_test.txt
```
python createDBpediaData/Freebase2DBpedia.py
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
python createDBpediaData/remove_unseen_objects.py
```


4) Use the following code to make different subsets from the shuffled dataset.

```
python createDBpediaData/make_subsets.py
```

The output of the above code can be directly used for training <b>TransE</b>, <b>DistMult</b> and <b>complex</b> codes. 
<b>HolE</b> would require one more step of converting these output files into bin file. Check HOLE folder for the steps.


<h2>Training the DBpedia data : </h2>

```
THEANO_FLAGS='device=gpu' python complex/dbpedia_run.py
```

<h2>Experiment Results on DBpedia datasets:</h2>
<table>
<tr>
   <th></th>
    <th colspan="8">DBpedia (train size=10000)</th>
  </tr>
  <tr>
    <th>Model</th>
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
    
  <tr>
  <td>DistMult</td>
  <td><b>0.012</b>
</td>   
    <td>0.014
</td>
    <td>0.013
</td>
    <td>0.015
</td>
    <td>0.016
</td>
    <td>301
</td>
    <td>489.8
</td>
  </tr> 

  
   
<tr>
  <td>HolE</td>
    <td>0.01
</td>   
<td><b>0.02</b>
</td>
<td><b>0.017</b>
</td>
    <td><b>0.017</b>
</td>
    <td>0.0186
</td>
    <td>3000
</td>
    <td>4007.95
</td>
  </tr>  
  
    
<tr>
  <td>complEx</td>
    <td>0.012
</td>   
    <td>0.015
</td>
    <td>0.013
</td>
    <td>0.015
</td>
    <td>0.015
</td>
    <td>601
</td>
    <td>1707
</td>
  </tr>  
 <tr>
   <th></th>
    <th colspan="8">DBpedia (train size=100000)</th>
  </tr>   
<tr>
  <td>TransE</td>
    <td>0.046
</td>   
    <td>0.061
</td>
    <td>0.022
</td>
    <td>0.089
</td>
<td><b>0.112</b>
</td>
    <td>801
</td>
    <td>6866.93
</td>
  </tr>  
  
  
  <tr>
  <td>DistMult
</td>
<td><b>0.061</b></td>   
<td><b>0.104</b></td>
<td><b>0.099</b></td>
<td><b>0.102</b></td>
    <td>0.111</td>
    <td>1201</td>
    <td>8226.67</td>
  </tr>  
  
  
  
  
  
   <tr>
  <td>HolE</td>
<td>0.05</td>   
<td>0.08</td>
<td>0.065</td>
<td>0.086</td>
<td>0.093    </td>
<td>4000</td>
<td>77891</td>

 <tr>
  <td>ComplEx</td>
<td>0.059</td>   
<td>0.091</td>
<td>0.077</td>
<td>0.095    </td>
<td>0.114</td>
<td>451</td>
 <td>4119
</td>
   
  </tr>
 <tr>
   <th></th>
    <th colspan="8">DBpedia (train size=1000000)</th>
  </tr>
     <tr>
  <td>DistMult</td>
<td>0.293</td>   
<td>0.668</td>
<td>0.551</td>
<td>0.742</td>
<td>0.089    </td>
<td>1701</td>
<td>79644.69
</td>
</table>



<h2> Predicting the time to train entire DBpedia </h2>
As a part of the project, we wanted to predict how much time would it take to train entire DBpedia datatset of size (~100 million) dataset.

We used the <b>DistMult</b> approach on the three sets of size ranges 10^4, 10^5, and 10^6.  I executed <b>DisMult</b> on each set for a fixed number of epochs which was 300. In order to understand why we chose <b>DistMult</b> approach, please read detailed blog post <a href="https://nausheenfatma.wordpress.com/2017/08/28/gsoc-final-submission/">here</a>. After plotting the results on a line graph using Microsoft Excel <a href="https://support.office.com/en-us/article/Add-change-or-remove-a-trendline-in-a-chart-fa59f86c-5852-4b68-a6d4-901a745842ad">trendline</a> feature to predict time for larger sizes, I got the following graph :


![alt text](https://github.com/nausheenfatma/embeddings/blob/master/gsoc2017-nausheen/polynomial.PNG)

After plotting, I found the closest curve which fits the data is that of a ploynomial curve of order 2. From the curve, we can see that for 10^8 size (the magnitude for entire DBpedia), the time estimation is approximately 80,000 seconds which means ~22 hours.

<h2> Code and Contribution </h2>
You can find all the code contribution (new codes/ updated codes) information from this patch <a href="https://github.com/nausheenfatma/embeddings/blob/master/gsoc2017-nausheen/contribution_patch.patch ">file</a>.

You can download the 1 million DBpedia dataset for training, and the final DistMult embeddings from <a href="http://tsoru.aksw.org/gsoc2017/dbpedia201604-1M-triples/distmult-embeddings-100dim.zip">here</a>.

<h2>Future Work</h2>

Now that we have predicted the time it would require to train entire DBpedia, we plan to execute the code on entire DBpedia, and officially release the embeddings, and training datasets on the official DBpedia website, where the research community can use it for their own experiments or applications.


