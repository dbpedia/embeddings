<b>Word embeddings</b> has been found to be very useful in the research community in the recent years by bringing semantically similar word closer in the vector space. Word embeddings is being actively used in many applications such as sentiment analysis, recommendation systems, question answering, etc. Knowledge graphs have been popularly used for storing data in the form of graph in the form of entities and relationships. The objective of this project is to find embeddings for knowledge graphs entities and relationships. If we want to find word embedding for a movie like <i><b>“Beauty and the Beast”</b></i>, simple aggregation/averaging of word embeddings for individual word tokens may or may not make great sense , as these words may be scattered far away in the text space. It would be very useful if we can get embeddings of the complete phrase as 1 atomic unit. Since knowledge graphs already stores the data in entities and relationship form, it would be very useful to get embeddings representation for the same.

Read my first blog here : https://nausheenfatma.wordpress.com/2017/05/31/gsoc-2017-knowledge-base-embeddings-for-dbpedia/






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


![alt text](https://github.com/nausheenfatma/embeddings/blob/master/gsoc2017-nausheen/polynomial.PNG)



