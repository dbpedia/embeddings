# ComplexEmbeddings

This project aims to generate complex word embeddings for Out-Of-Vocabulary entities. After completion, the package will be able to generate pre-trained embeddings, improve them by generating embeddings on-the-fly, evaluate the benchmarks using pre-trained embeddings, and make the same evaluations on the imporoved embeddings.

### Getting started

Here is how you can start training and testing the model yourself. First, clone the repository on your local machine. I assume you are familiar with Git, and have it installed on your system prior to using this repo.

```shell
$ git clone git@github.com:tramplingWillow/embeddings.git
$ cd embeddings/gsoc2018-bharat
```

### Creating python virtual environment

Next, we need to setup the python environment with all the libraries that are used in this project. This project uses Python3 so make sure you have it installed. Check the installation procedure and download the latest version [here](https://www.python.org/downloads/).

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip
$ pip install -r requirements.txt
```

### Downloading and cleaning wiki dump

Here, you can find the first 1 billion bytes of English Wikipedia.

```shell
$ mkdir data
$ wget -c http://mattmahoney.net/dc/enwik9.zip -P data
$ unzip data/enwik9.zip -d data
```

This is a raw Wikipedia dump and needs to be cleaned because it contains a lot of HTML/XML data. There are two ways to pre-process it. Here, I am using the Wiki Extractor script available [here](https://github.com/attardi/wikiextractor/blob/master/WikiExtractor.py) bundled with FastText to pre-process it.

```shell
$ wget -c https://github.com/attardi/wikiextractor/blob/master/WikiExtractor.py -P src
$ python src/WikiExtractor.py data/enwik9 -l -o data/output
$ python src/WikiExtractor.py data/enwik9 -o data/text
```

Now, we have the extracted text from the XML dump, with and without html links. Next we need to generate surface forms from this and combine the files into one single file for training the FastText model. While doing so, the descriptions for each entity will also be extracted.

```
$ python src/surface_forms.py data/output
$ python src/check_person.py data/text data/Genders.csv
$ python src/mention_extractor data/output data/AnchorDictionary.csv data/Genders.csv
$ python src/combine.py data/output data/text8 data/descriptions.json
```

### Pre-Training using FastText

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
$ python src/pre-train.py -i data/text8 -o model/entity_fasttext_n100 -m fasttext -s 100 -sg 1 -hs 1 -e 10
```

### Training the LSTM model

```
$ python src/train_lstm.py
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
