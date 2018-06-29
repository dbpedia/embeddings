import argparse
import logging
from gensim.models.word2vec import LineSentence
from gensim.models import FastText
from gensim.models import Word2Vec
"""
We are using the wrapper for FastText available in the
Gensim package. FastText is an extension to the word2vec
skipgram model, as it uses character n-grams to generate
word embeddings. This allows for the model to create embeddings
for out of vocabulary words with the help of previously
identified n-gram embeddings.
"""
logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO


def train_fasttext(input_file, output_file, skipgram, loss, size, epochs):
    """
    train_fasttext(args**) -> Takes the input file, the
    output file and the model
    hyperparameters as arguments
    and trains the model accordingly.
    The model is saved at the output location.

    Arguments
    ---------
    input_file : Input pre-processed wiki dump
    output_file : Output directory to save the model.
    skipgram : Layers of the model (0 - CBOW, 1 - Skipgram)
    loss : Loss Function (0 - Negative Sampling, 1 - Heirarichal Loss)
    size : Embedding size (100 ~ 300)
    epochs : Number of epochs
    """
    sentence = LineSentence(input_file)

    model = FastText(sentence, sg=skipgram, hs=loss, size=size,
                     alpha=0.05, window=5, min_count=5, min_n=2,
                     max_n=5, workers=3, iter=epochs)

    model.save(output_file)


def train_word2vec(input_file, output_file, skipgram, loss, size, epochs):
    """
    train_word2vec(args**) -> Takes the input file,
    the output file and the model hyperparameters as
    arguments and trains the model accordingly.
    The model is saved at the output location.

    Arguments
    ---------
    input_file : Input pre-processed wiki dump
    output_file : Output directory to save the model.
    skipgram : Layers of the model (0 - CBOW, 1 - Skipgram)
    loss : Loss Function (0 - Negative Sampling, 1 - Heirarichal Loss)
    size : Embedding size (100 ~ 300)
    epochs : Number of epochs
    """
    sentence = LineSentence(input_file)

    model = Word2Vec(sentence, sg=skipgram, hs=loss,
                     size=size, alpha=0.05, window=5,
                     min_count=5, workers=3, iter=epochs)

    model.save(output_file)


def main(args):
    input_file, output_file, mode = args.input, args.output, args.mode
    skipgram, loss, size, epochs = int(args.skipgram), int(args.loss),
    int(args.size), int(args.epochs)
    if mode == "fasttext":
        train_fasttext(input_file, output_file, skipgram, loss, size, epochs)
    else:
        train_word2vec(input_file, output_file, skipgram, loss, size, epochs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    groupF = parser.add_argument_group('Files')
    groupF.add_argument("-i", "--input", default="data/file9",
                        help="Clean wiki dump file with text")
    groupF.add_argument("-o", "--output", default="model/pre_wiki",
                        help="Output directory to save the model")
    groupF.add_argument("-m", "--mode", default="fasttext",
                        help="Word2Vec or FastText")
    groupM = parser.add_argument_group('Model')
    groupM.add_argument("-s", "--size", default="200",
                        help="Embedding size")
    groupM.add_argument("-sg", "--skipgram", default="1",
                        help="Model uses skipgram or CBOW")
    groupM.add_argument("-hs", "--loss", default="1",
                        help="Loss function")
    groupM.add_argument("-e", "--epochs", default="3",
                        help="Number of epochs")

    args = parser.parse_args()

    main(args)
