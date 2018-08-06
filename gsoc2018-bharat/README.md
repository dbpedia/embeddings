# ComplexEmbeddings

This project aims to generate complex word embeddings for Out-Of-Vocabulary entities. After completion, the package will be able to generate pre-trained embeddings, improve them by generating embeddings on-the-fly, evaluate the benchmarks using pre-trained embeddings, and make the same evaluations on the imporoved embeddings.

### Getting started

Here is how you can start training and testing the model yourself. First, clone the repository on your local machine. I assume you are familiar with Git, and have it installed on your system prior to using this repo.

```shell
$ git clone git@github.com:dbpedia/embeddings.git
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

Our model is a Recurrent Neural Network, with two linear layers for input and output with stacked LSTM with RNN that encodes the input description/abstract into a single word vector. That word vector can be combined with the entity for which the description was provided to obtain the embedding. Hyperparameters and the model architecture are not rigid and can be changed before training albeit I have set some defaults that I used while training.
- Files
  - Saved Model ( *-m* )
  - Input file with descriptions ( *-i* )
  - Output file to store the predicted embeddings ( *-v* )
- Model
  - Epochs, *-e*
  - Embedding size / Input Size, *-s*
  - Hidden layer size, *-o*
  - Sequence Length, *-l*
  - Number of layers, *-n*

Here are some possible ways to use the script:
```
$ python src/train_lstm.py
$ python src/train_lstm.py -e 50
$ python src/train_lstm.py -m {saved_model} -e 10 -s 300
```
Execute the command without any additional arguments to run the script with the default values.
