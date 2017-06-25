<b>Word embeddings</b> has been found to be very useful in the research community in the recent years by bringing semantically similar word closer in the vector space. Word embeddings is being actively used in many applications such as sentiment analysis, recommendation systems, question answering, etc. Knowledge graphs have been popularly used for storing data in the form of graph in the form of entities and relationships. The objective of this project is to find embeddings for knowledge graphs entities and relationships. If we want to find word embedding for a movie like <i><b>“Beauty and the Beast”</b></i>, simple aggregation/averaging of word embeddings for individual word tokens may or may not make great sense , as these words may be scattered far away in the text space. It would be very useful if we can get embeddings of the complete phrase as 1 atomic unit. Since knowledge graphs already stores the data in entities and relationship form, it would be very useful to get embeddings representation for the same.

Read my first blog here : https://nausheenfatma.wordpress.com/2017/05/31/gsoc-2017-knowledge-base-embeddings-for-dbpedia/






<table>
<tr>
   <th>Model</th>
    <th colspan="3">WN11</th>
    <th colspan="3">FB15K</th>
  </tr>
  <tr>
    <th></th>
    <th>MRR (raw)</th>
    <th>MRR (filtered)</th>
    <th>Hits@10 (filtered)</th>
    <th>MRR (raw)</th>
    <th>MRR (filtered)</th>
    <th>Hits@10 (filtered)</th>
  </tr>
  
  
  <tr>
  <td>TransE</td>
  <td>0.431</td>
    <td>0.309</td>
    <td>0.936</td>
    <td>0.374</td>
    <td>0.219</td>
    <td>0.643</td>    
  </tr>
    <tr>
  <td>DistMult</td>
    <td>0.835</td>
    <td>0.561</td>
    <td>0.937</td>
    <td>0.651</td>
        <td>0.237</td>
    <td>0.825</td>
  </tr>
    <tr>
  <td>HolE</td>
    <td>0.62</td>
    <td>0.94</td>
    <td>0.944</td>
    <td></td>
        <td></td>
    <td></td>
  </tr>
    <tr>
  <td>ComplEx</td>
    <td>0.94</td>
    <td>0.581</td>
    <td>0.944</td>
    <td>0.672</td>
        <td>0.235</td>
    <td>0.832</td>
  </tr>
</table>







<table>
<tr>
   <th>Model</th>
   
   <th>Time Complexity </th>
   <th>Space Complexity</th>
    <th >WN11 <br>Training time (in hours)</th>
    <th >FB15K <br>Training time (in hours)</th>
  </tr>

  
  
  <tr>
  <td>TransE</td>
    
    <td>O(K)</td>
    <td>O(K)</td>
    <td>2.68</td>
    <td>6.77</td>    
  </tr>
    <tr>
  <td>DistMult</td>
    <td>O(K)</td>
    <td>O(K)</td>
    <td>3.22</td>
    <td>20.38</td>
  </tr>
    <tr>
  <td>HolE</td>
    <td>O(K log K)</td>
    <td>O(K)</td>
    <td>3.98</td>
    <td></td>
  </tr>
    <tr>
  <td>ComplEx</td>
    <td>O(K)</td>
    <td>O(K)</td>
    <td>9.04</td>
    <td></td>
  </tr>
</table>




