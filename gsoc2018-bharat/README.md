# ComplexEmbeddings

This project aims to generate complex word embeddings for Out-Of-Vocabulary entities. After completion, the package will be able to generate pre-trained embeddings, improve them by generating embeddings on-the-fly, evaluate the benchmarks using pre-trained embeddings, and make the same evaluations on the imporoved embeddings.

## Requirements

All the libraries used under this project are included in the file, requirements.txt. To install, just run the command

```shell
$ pip install --upgrade pip
$ pip install -r requirements.txt
```

## Downloading and cleaning wiki dump

Here, you can find the first 1 billion bytes of English Wikipedia.

```shell
$ mkdir data
$ wget -c http://mattmahoney.net/dc/enwik9.zip -P data
$ unzip data/enwik9.zip -d data
```

This is a raw Wikipedia dump and needs to be cleaned because it contains a lot of HTML/XML data. There are two ways to pre-process it. Here, I am using the [wikifil.pl](https://github.com/tramplingWillow/ComplexEmbeddings/blob/master/src/package/wikifil.pl) bundled with FastText (the script was originally developed by Matt Mahoney, and can be found on his [website](http://mattmahoney.net/).) to pre-process it.

```shell
$ perl src/package/wikifil.pl data/enwik9 > data/fil9
```

## Pre-Training and Evaluating Analogy using Google Dataset

The script, [pre-train.py](https://github.com/tramplingWillow/ComplexEmbeddings/blob/master/src/pre-train.py) takes the following arguments:
- Files
  - Input File: Clean wiki dump
  - Output File: Saved model
- Model Hyperparameters
  - Vector Size, *-s*: Defines the Embedding Size
  - Skipgram, *-sg*: Decides whether model uses skipgram or CBOW
  - Loss Function, *-hs*: Loss function used is Hierarchal Softmax or Negative Sampling
  - Epochs, *-e*: Number of epochs

```shell
$ mkdir model
$ python src/pre-train.py -i data/fil9 -o model/pre_wiki -s 300 -sg 1 -hs 1 -e 5
```

Next, we try to see how these pre-trained embeddings perform on the [Google Analogy Task](http://download.tensorflow.org/data/questions-words.txt). For this we have the [analogy.py](https://github.com/tramplingWillow/ComplexEmbeddings/blob/master/src/analogy.py).<br>
*Updates are to be made so that the script evaluates the model for the entire dataset.*

```shell
$ python analogy.py -i data/questions-words.txt -m model/pre_wiki
Question: high is to higher as great is to ?
Answer: greater
Predicted: greater
Question: glendale is to arizona as akron is to ?
Answer: ohio
Predicted: ohio
Question: ethical is to unethical as comfortable is to ?
Answer: uncomfortable
Predicted: comfortably
Question: netherlands is to dutch as brazil is to ?
Answer: brazilian
Predicted: brazilian
Question: free is to freely as happy is to ?
Answer: happily
Predicted: happily
Question: luanda is to angola as monrovia is to ?
Answer: liberia
Predicted: liberia
```
